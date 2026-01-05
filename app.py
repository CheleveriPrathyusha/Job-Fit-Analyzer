from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, Response, send_from_directory
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename
import os
import csv
from io import StringIO
from datetime import datetime
import json

# Import custom modules
from config import Config
from resume_parser import parse_resume
from skill_extractor import extract_skills
from matcher import calculate_fit_score, generate_recommendations
from visualizations import create_visualizations

app = Flask(__name__)
app.config.from_object(Config)

# Initialize MongoDB
mongo = PyMongo(app)

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# --- FILE SERVING ROUTE (CRITICAL FOR RESUME VIEWING) ---
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serves the uploaded resume file to the browser"""
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except FileNotFoundError:
        return "File not found", 404

# --- AUTH ROUTES ---
@app.route('/')
def index():
    if 'user_id' in session:
        user_type = session.get('user_type', 'candidate')
        if user_type == 'hr':
            return redirect(url_for('hr_dashboard'))
        else:
            return redirect(url_for('candidate_dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user_type = request.form.get('user_type', 'candidate')
        name = request.form.get('name')
        
        existing_user = mongo.db.users.find_one({'email': email})
        if existing_user:
            flash('Email already registered. Please login.', 'danger')
            return redirect(url_for('login'))
        
        user_data = {
            'email': email,
            'password': password,
            'user_type': user_type,
            'name': name,
            'created_at': datetime.utcnow()
        }
        
        result = mongo.db.users.insert_one(user_data)
        session['user_id'] = str(result.inserted_id)
        session['user_type'] = user_type
        session['name'] = name
        
        flash('Registration successful!', 'success')
        return redirect(url_for('hr_dashboard' if user_type == 'hr' else 'candidate_dashboard'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = mongo.db.users.find_one({'email': email, 'password': password})
        
        if user:
            session['user_id'] = str(user['_id'])
            session['user_type'] = user.get('user_type', 'candidate')
            session['name'] = user.get('name', 'User')
            flash('Login successful!', 'success')
            return redirect(url_for('hr_dashboard' if session['user_type'] == 'hr' else 'candidate_dashboard'))
        else:
            flash('Invalid credentials.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# --- HR ROUTES ---
@app.route('/hr-dashboard')
def hr_dashboard():
    if 'user_id' not in session or session.get('user_type') != 'hr':
        flash('Please login as HR to access this page.', 'danger')
        return redirect(url_for('login'))
    
    # 1. Get all jobs posted by this HR
    jobs = list(mongo.db.jobs.find({'hr_id': ObjectId(session['user_id'])}))
    job_ids = [job['_id'] for job in jobs]
    
    # 2. Get Login History (Last 5 candidates)
    login_history_raw = list(mongo.db.users.find({'user_type': 'candidate'}).sort('created_at', -1).limit(5))
    login_history = [{'username': u.get('name', 'User'), 'timestamp': u['created_at'].strftime('%H:%M %p') if u.get('created_at') else 'N/A'} for u in login_history_raw]

    # 3. Get Eligible Candidates (Score >= 70)
    eligible_raw = list(mongo.db.analyses.find({
        'job_id': {'$in': job_ids}, 
        'fit_score.overall_score': {'$gte': 70}
    }).sort('fit_score.overall_score', -1))
    
    eligible_candidates = []
    for analysis in eligible_raw:
        user = mongo.db.users.find_one({'_id': analysis['user_id']})
        job = mongo.db.jobs.find_one({'_id': analysis['job_id']})
        
        # Prepare dictionary for the template
        eligible_candidates.append({
            'id': str(analysis['_id']),  # For delete route
            'name': user.get('name', 'Candidate') if user else 'Candidate',
            'job_role': job.get('title', 'Job') if job else 'Unknown Job',
            'fit_score': round(analysis['fit_score']['overall_score'], 1),
            'resume': analysis.get('resume_filename'), # Required for View Resume button
            'analysis_id': str(analysis['_id'])        # For View Report button
        })
    
    # Convert ObjectId to string for template
    for job in jobs: 
        job['_id'] = str(job['_id'])
        
    return render_template('hr_dashboard.html', 
                           jobs=jobs, 
                           login_history=login_history, 
                           candidates=eligible_candidates)

@app.route('/create-job', methods=['GET', 'POST'])
def create_job():
    if 'user_id' not in session or session.get('user_type') != 'hr': 
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        job_data = {
            'title': request.form.get('title'),
            'company': request.form.get('company'),
            'location': request.form.get('location'),
            'description': request.form.get('description'),
            'required_skills': [s.strip() for s in request.form.get('required_skills', '').split(',') if s.strip()],
            'required_experience': int(request.form.get('required_experience', 0)),
            'required_education': request.form.get('required_education'),
            'certifications': [c.strip() for c in request.form.get('certifications', '').split(',') if c.strip()],
            'hr_id': ObjectId(session['user_id']),
            'created_at': datetime.utcnow(),
            'active': True
        }
        mongo.db.jobs.insert_one(job_data)
        flash('Job created successfully!', 'success')
        return redirect(url_for('hr_dashboard'))
    return render_template('create_job.html')

@app.route('/edit-job/<job_id>', methods=['GET', 'POST'])
def edit_job(job_id):
    if 'user_id' not in session or session.get('user_type') != 'hr': return redirect(url_for('login'))
    
    job = mongo.db.jobs.find_one({'_id': ObjectId(job_id)})
    if not job: 
        flash('Job not found.', 'danger')
        return redirect(url_for('hr_dashboard'))

    if request.method == 'POST':
        updated_data = {
            'title': request.form.get('title'),
            'company': request.form.get('company'),
            'location': request.form.get('location'),
            'description': request.form.get('description'),
            'required_skills': [s.strip() for s in request.form.get('required_skills', '').split(',') if s.strip()],
            'required_experience': int(request.form.get('required_experience', 0)),
            'required_education': request.form.get('required_education'),
            'certifications': [c.strip() for c in request.form.get('certifications', '').split(',') if c.strip()],
            'hr_id': ObjectId(session['user_id']),
            'created_at': job.get('created_at'),
            'active': True
        }
        mongo.db.jobs.update_one({'_id': ObjectId(job_id)}, {'$set': updated_data})
        flash('Job updated successfully!', 'success')
        return redirect(url_for('hr_dashboard'))
    
    job['_id'] = str(job['_id'])
    return render_template('edit_job.html', job=job)

@app.route('/delete-job/<job_id>', methods=['POST'])
def delete_job(job_id):
    if 'user_id' not in session or session.get('user_type') != 'hr': return redirect(url_for('login'))
    try:
        mongo.db.jobs.delete_one({'_id': ObjectId(job_id)})
        mongo.db.analyses.delete_many({'job_id': ObjectId(job_id)})
        flash('Job deleted successfully.', 'success')
    except Exception as e: flash(f'Error deleting job: {str(e)}', 'danger')
    return redirect(url_for('hr_dashboard'))

@app.route('/delete-candidate/<id>', methods=['POST'])
def delete_candidate(id):
    if 'user_id' not in session or session.get('user_type') != 'hr':
        return redirect(url_for('login'))
    try:
        mongo.db.analyses.delete_one({'_id': ObjectId(id)})
        flash('Candidate application removed from list.', 'success')
    except Exception as e:
        flash(f'Error deleting candidate: {str(e)}', 'danger')
    return redirect(url_for('hr_dashboard'))

@app.route('/export-job-data')
def export_job_data():
    if 'user_id' not in session or session.get('user_type') != 'hr': return redirect(url_for('login'))
    jobs = list(mongo.db.jobs.find({'hr_id': ObjectId(session['user_id'])}))
    si = StringIO(); cw = csv.writer(si)
    cw.writerow(['Title', 'Company', 'Location', 'Experience', 'Status', 'Date'])
    for j in jobs:
        cw.writerow([j.get('title'), j.get('company'), j.get('location'), j.get('required_experience'), "Active" if j.get('active') else "Inactive", j.get('created_at').strftime('%Y-%m-%d') if j.get('created_at') else "N/A"])
    output = Response(si.getvalue(), mimetype='text/csv')
    output.headers["Content-Disposition"] = "attachment; filename=jobs_export.csv"
    return output

@app.route('/view-analytics')
def view_analytics():
    """Exports Candidate Login/Registration History to CSV with Eligibility Status, Role, and Score"""
    if 'user_id' not in session or session.get('user_type') != 'hr':
        return redirect(url_for('login'))
    
    # Get all candidates
    candidates = list(mongo.db.users.find({'user_type': 'candidate'}).sort('created_at', -1))
    
    si = StringIO()
    cw = csv.writer(si)
    
    # Updated Header
    cw.writerow(['Candidate Name', 'Email Address', 'Account Created / Last Login', 'User Type', 'Eligibility Status', 'Eligible For Role(s)', 'Resume Score'])
    
    for candidate in candidates:
        # Find all analyses where the candidate scored >= 70
        eligible_analyses = list(mongo.db.analyses.find({
            'user_id': candidate['_id'],
            'fit_score.overall_score': {'$gte': 70}
        }))
        
        if eligible_analyses:
            status = "Eligible"
            role_names = []
            scores = []
            
            for analysis in eligible_analyses:
                job = mongo.db.jobs.find_one({'_id': analysis['job_id']})
                if job and 'title' in job:
                    role_names.append(job['title'])
                scores.append(str(analysis['fit_score']['overall_score']))
            
            # Remove duplicates for roles, keep scores listed
            eligible_role = ", ".join(list(set(role_names))) if role_names else "Unknown Role"
            resume_score = ", ".join(scores)
        else:
            status = "Not Eligible"
            eligible_role = "N/A"
            resume_score = "N/A"

        cw.writerow([
            candidate.get('name', 'N/A'),
            candidate.get('email', 'N/A'),
            candidate.get('created_at').strftime('%Y-%m-%d %H:%M:%S') if candidate.get('created_at') else 'N/A',
            'Candidate',
            status,
            eligible_role,
            resume_score
        ])
    
    output = Response(si.getvalue(), mimetype='text/csv')
    output.headers["Content-Disposition"] = "attachment; filename=candidate_analytics.csv"
    return output

# --- CANDIDATE ROUTES ---
@app.route('/candidate-dashboard')
def candidate_dashboard():
    if 'user_id' not in session: return redirect(url_for('login'))
    jobs = list(mongo.db.jobs.find({}))
    user_analyses = list(mongo.db.analyses.find({'user_id': ObjectId(session['user_id'])}).sort('analyzed_at', -1).limit(5))
    for job in jobs: job['_id'] = str(job['_id'])
    for analysis in user_analyses: analysis['_id'] = str(analysis['_id']); analysis['job_id'] = str(analysis['job_id'])
    return render_template('candidate_dashboard.html', jobs=jobs, analyses=user_analyses)

@app.route('/analyze/<job_id>', methods=['GET', 'POST'])
def analyze_job(job_id):
    if 'user_id' not in session: return redirect(url_for('login'))
    
    try:
        job = mongo.db.jobs.find_one({'_id': ObjectId(job_id)})
        if not job: return redirect(url_for('candidate_dashboard'))
    except:
        return redirect(url_for('candidate_dashboard'))
    
    if request.method == 'POST':
        file = request.files.get('resume')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                resume_data = parse_resume(filepath)
                resume_skills = extract_skills(resume_data.get('text', ''))
                
                candidate_data = {
                    'skills': resume_skills,
                    'experience': resume_data.get('experience_years', 0),
                    'education': resume_data.get('education', []),
                    'certifications': resume_data.get('certifications', [])
                }
                job_data = {
                    'required_skills': job.get('required_skills', []),
                    'required_experience': job.get('required_experience', 0),
                    'required_education': job.get('required_education', ''),
                    'certifications': job.get('certifications', [])
                }
                
                fit_score = calculate_fit_score(candidate_data, job_data)
                recommendations = generate_recommendations(candidate_data, job_data, fit_score)
                visualizations = create_visualizations(fit_score, candidate_data, job_data)
                
                analysis_data = {
                    'user_id': ObjectId(session['user_id']),
                    'job_id': ObjectId(job_id),
                    'candidate_data': candidate_data,
                    'job_data': job_data,
                    'fit_score': fit_score,
                    'recommendations': recommendations,
                    'visualizations': visualizations,
                    'analyzed_at': datetime.utcnow(),
                    'resume_filename': filename # Saved for HR retrieval
                }
                res = mongo.db.analyses.insert_one(analysis_data)
                
                return redirect(url_for('view_results', analysis_id=str(res.inserted_id)))
                
            except Exception as e:
                flash(f'Error processing resume: {str(e)}', 'danger')
        else:
            flash('Invalid file.', 'danger')
            
    job['_id'] = str(job['_id'])
    return render_template('analyze.html', job=job)

@app.route('/results/<analysis_id>')
def view_results(analysis_id):
    if 'user_id' not in session: return redirect(url_for('login'))
    
    try:
        analysis = mongo.db.analyses.find_one({'_id': ObjectId(analysis_id)})
        if not analysis: return redirect(url_for('candidate_dashboard'))
        
        job = mongo.db.jobs.find_one({'_id': analysis['job_id']})
        analysis['_id'] = str(analysis['_id'])
        if job: job['_id'] = str(job['_id'])
        
        return render_template('results.html', analysis=analysis, job=job)
    except:
        return redirect(url_for('candidate_dashboard'))

@app.route('/api/skills')
def get_skills():
    try:
        with open('skills_database.json', 'r') as f:
            skills_data = json.load(f)
        all_skills = []
        for category in skills_data.values(): all_skills.extend(category)
        return jsonify(all_skills)
    except: return jsonify([])

if __name__ == '__main__':
    import spacy
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        from spacy.cli import download
        download("en_core_web_sm")
    app.run(debug=True, port=5000)
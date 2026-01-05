# # from collections import defaultdict
# # import numpy as np

# # def calculate_skill_match(candidate_skills, required_skills):
# #     """Calculate skill match percentage"""
# #     if not required_skills:
# #         return 0
    
# #     # Flatten candidate skills
# #     candidate_flat = []
# #     for category in candidate_skills.values():
# #         candidate_flat.extend([skill.lower() for skill in category])
    
# #     # Convert required skills to lowercase
# #     required_flat = [skill.lower() for skill in required_skills]
    
# #     # Calculate intersection
# #     matched_skills = set(candidate_flat).intersection(set(required_flat))
    
# #     # Calculate percentage
# #     if len(required_flat) > 0:
# #         return (len(matched_skills) / len(required_flat)) * 100
# #     return 0

# # def calculate_experience_match(candidate_exp, required_exp):
# #     """Calculate experience match percentage"""
# #     if required_exp == 0:
# #         return 100
    
# #     if candidate_exp >= required_exp:
# #         return 100
# #     else:
# #         # Linear scaling for partial match
# #         return (candidate_exp / required_exp) * 100

# # def calculate_education_match(candidate_education, required_education):
# #     """Calculate education match percentage"""
# #     if not required_education:
# #         return 100
    
# #     required_lower = required_education.lower()
    
# #     for education in candidate_education:
# #         if required_lower in education.lower():
# #             return 100
        
# #         # Check for degree types
# #         degree_types = ['bachelor', 'master', 'phd', 'doctorate']
# #         required_degree = None
# #         candidate_degree = None
        
# #         for degree in degree_types:
# #             if degree in required_lower:
# #                 required_degree = degree
# #             if degree in education.lower():
# #                 candidate_degree = degree
        
# #         if required_degree and candidate_degree:
# #             # Simple hierarchy: PhD > Master > Bachelor
# #             hierarchy = {'bachelor': 1, 'master': 2, 'phd': 3, 'doctorate': 3}
# #             if hierarchy.get(candidate_degree, 0) >= hierarchy.get(required_degree, 0):
# #                 return 100
    
# #     return 0

# # def calculate_certification_match(candidate_certs, required_certs):
# #     """Calculate certification match percentage"""
# #     if not required_certs:
# #         return 100
    
# #     # Convert to lowercase for comparison
# #     candidate_lower = [cert.lower() for cert in candidate_certs]
# #     required_lower = [cert.lower() for cert in required_certs]
    
# #     matched = set(candidate_lower).intersection(set(required_lower))
    
# #     if len(required_lower) > 0:
# #         return (len(matched) / len(required_lower)) * 100
# #     return 0

# # def calculate_fit_score(candidate_data, job_data):
# #     """Calculate overall fit score using weighted algorithm"""
    
# #     # Extract data
# #     candidate_skills = candidate_data.get('skills', defaultdict(list))
# #     candidate_exp = candidate_data.get('experience', 0)
# #     candidate_education = candidate_data.get('education', [])
# #     candidate_certs = candidate_data.get('certifications', [])
    
# #     required_skills = job_data.get('required_skills', [])
# #     required_exp = job_data.get('required_experience', 0)
# #     required_education = job_data.get('required_education', '')
# #     required_certs = job_data.get('certifications', [])
    
# #     # Calculate component scores
# #     skill_score = calculate_skill_match(candidate_skills, required_skills)
# #     exp_score = calculate_experience_match(candidate_exp, required_exp)
# #     edu_score = calculate_education_match(candidate_education, required_education)
# #     cert_score = calculate_certification_match(candidate_certs, required_certs)
    
# #     # Calculate weighted overall score
# #     weights = {
# #         'skill': 0.40,
# #         'experience': 0.30,
# #         'education': 0.20,
# #         'certification': 0.10
# #     }
    
# #     overall_score = (
# #         skill_score * weights['skill'] +
# #         exp_score * weights['experience'] +
# #         edu_score * weights['education'] +
# #         cert_score * weights['certification']
# #     )
    
# #     # Round to 2 decimal places
# #     overall_score = round(overall_score, 2)
    
# #     # Determine eligibility
# #     if overall_score >= 80:
# #         eligibility = "Eligible"
# #     elif overall_score >= 50:
# #         eligibility = "Partially Eligible"
# #     else:
# #         eligibility = "Not Eligible"
    
# #     # Prepare component scores for visualization
# #     component_scores = {
# #         'skill': round(skill_score, 2),
# #         'experience': round(exp_score, 2),
# #         'education': round(edu_score, 2),
# #         'certification': round(cert_score, 2)
# #     }
    
# #     # Find missing skills
# #     candidate_flat = []
# #     for category in candidate_skills.values():
# #         candidate_flat.extend([skill.lower() for skill in category])
    
# #     required_flat = [skill.lower() for skill in required_skills]
# #     missing_skills = list(set(required_flat) - set(candidate_flat))
    
# #     return {
# #         'overall_score': overall_score,
# #         'component_scores': component_scores,
# #         'eligibility': eligibility,
# #         'missing_skills': missing_skills,
# #         'matched_skills_count': len(set(candidate_flat).intersection(set(required_flat))),
# #         'required_skills_count': len(required_flat)
# #     }

# # def generate_recommendations(candidate_data, job_data, fit_results):
# #     """Generate career recommendations based on gaps"""
# #     recommendations = []
    
# #     overall_score = fit_results['overall_score']
# #     missing_skills = fit_results['missing_skills']
    
# #     # Score-based recommendations
# #     if overall_score >= 80:
# #         recommendations.append({
# #             'type': 'success',
# #             'message': 'You are highly qualified for this position!'
# #         })
# #         recommendations.append({
# #             'type': 'info',
# #             'message': 'Prepare for behavioral interview questions'
# #         })
# #     elif overall_score >= 50:
# #         recommendations.append({
# #             'type': 'warning',
# #             'message': 'You have potential but need to address some gaps'
# #         })
# #     else:
# #         recommendations.append({
# #             'type': 'danger',
# #             'message': 'Consider gaining more experience or developing required skills'
# #         })
    
# #     # Skill-based recommendations
# #     if missing_skills:
# #         recommendations.append({
# #             'type': 'skill_gap',
# #             'message': f'Develop these skills: {", ".join(missing_skills[:5])}'
# #         })
        
# #         if len(missing_skills) > 0:
# #             recommendations.append({
# #                 'type': 'learning',
# #                 'message': 'Consider online courses on platforms like Coursera or Udemy'
# #             })
    
# #     # Experience-based recommendations
# #     candidate_exp = candidate_data.get('experience', 0)
# #     required_exp = job_data.get('required_experience', 0)
    
# #     if candidate_exp < required_exp:
# #         years_needed = required_exp - candidate_exp
# #         recommendations.append({
# #             'type': 'experience',
# #             'message': f'Gain {years_needed} more years of relevant experience'
# #         })
    
# #     # Certification recommendations
# #     candidate_certs = candidate_data.get('certifications', [])
# #     required_certs = job_data.get('certifications', [])
    
# #     missing_certs = set([c.lower() for c in required_certs]) - set([c.lower() for c in candidate_certs])
# #     if missing_certs:
# #         recommendations.append({
# #             'type': 'certification',
# #             'message': f'Obtain these certifications: {", ".join(missing_certs)}'
# #         })
    
# #     # General recommendations
# #     recommendations.append({
# #         'type': 'general',
# #         'message': 'Tailor your resume to highlight relevant experience'
# #     })
    
# #     recommendations.append({
# #         'type': 'general',
# #         'message': 'Network with professionals in the industry'
# #     })
    
# #     return recommendations
# from collections import defaultdict
# import numpy as np

# def calculate_skill_match(candidate_skills, required_skills):
#     if not required_skills: return 0
#     candidate_flat = []
#     for category in candidate_skills.values():
#         candidate_flat.extend([skill.lower() for skill in category])
#     required_flat = [skill.lower() for skill in required_skills]
#     matched_skills = set(candidate_flat).intersection(set(required_flat))
#     if len(required_flat) > 0:
#         return (len(matched_skills) / len(required_flat)) * 100
#     return 0

# def calculate_experience_match(candidate_exp, required_exp):
#     if required_exp == 0: return 100
#     if candidate_exp >= required_exp: return 100
#     return (candidate_exp / required_exp) * 100

# def calculate_education_match(candidate_education, required_education):
#     if not required_education: return 100
#     required_lower = required_education.lower()
#     for education in candidate_education:
#         if required_lower in education.lower(): return 100
#         degree_types = ['bachelor', 'master', 'phd', 'doctorate']
#         required_degree = next((d for d in degree_types if d in required_lower), None)
#         candidate_degree = next((d for d in degree_types if d in education.lower()), None)
#         if required_degree and candidate_degree:
#             hierarchy = {'bachelor': 1, 'master': 2, 'phd': 3, 'doctorate': 3}
#             if hierarchy.get(candidate_degree, 0) >= hierarchy.get(required_degree, 0):
#                 return 100
#     return 0

# def calculate_certification_match(candidate_certs, required_certs):
#     if not required_certs: return 100
#     candidate_lower = [cert.lower() for cert in candidate_certs]
#     required_lower = [cert.lower() for cert in required_certs]
#     matched = set(candidate_lower).intersection(set(required_lower))
#     if len(required_lower) > 0:
#         return (len(matched) / len(required_lower)) * 100
#     return 0

# def calculate_fit_score(candidate_data, job_data):
#     candidate_skills = candidate_data.get('skills', defaultdict(list))
#     candidate_exp = candidate_data.get('experience', 0)
#     candidate_education = candidate_data.get('education', [])
#     candidate_certs = candidate_data.get('certifications', [])
    
#     required_skills = job_data.get('required_skills', [])
#     required_exp = job_data.get('required_experience', 0)
#     required_education = job_data.get('required_education', '')
#     required_certs = job_data.get('certifications', [])
    
#     skill_score = calculate_skill_match(candidate_skills, required_skills)
#     exp_score = calculate_experience_match(candidate_exp, required_exp)
#     edu_score = calculate_education_match(candidate_education, required_education)
#     cert_score = calculate_certification_match(candidate_certs, required_certs)
    
#     weights = {'skill': 0.40, 'experience': 0.30, 'education': 0.20, 'certification': 0.10}
#     overall_score = round(
#         skill_score * weights['skill'] +
#         exp_score * weights['experience'] +
#         edu_score * weights['education'] +
#         cert_score * weights['certification'], 2
#     )
    
#     if overall_score >= 70: eligibility = "Eligible"
#     elif overall_score >= 50: eligibility = "Partially Eligible"
#     else: eligibility = "Not Eligible"
    
#     # REQUIRED for your new dashboard:
#     component_scores = {
#         'skill': round(skill_score, 2),
#         'experience': round(exp_score, 2),
#         'education': round(edu_score, 2),
#         'certification': round(cert_score, 2)
#     }
    
#     candidate_flat = []
#     for category in candidate_skills.values():
#         candidate_flat.extend([skill.lower() for skill in category])
#     required_flat = [skill.lower() for skill in required_skills]
    
#     return {
#         'overall_score': overall_score,
#         'component_scores': component_scores, # HTML uses this
#         'eligibility': eligibility,
#         'missing_skills': list(set(required_flat) - set(candidate_flat)),
#         'matched_skills_count': len(set(candidate_flat).intersection(set(required_flat))), # Visualizations use this
#         'required_skills_count': len(required_flat) # Visualizations use this
#     }

# def generate_recommendations(candidate_data, job_data, fit_results):
#     recommendations = []
#     overall_score = fit_results['overall_score']
#     missing_skills = fit_results['missing_skills']
    
#     if overall_score >= 70:
#         recommendations.append({'type': 'success', 'message': 'You are highly qualified for this position!'})
#         recommendations.append({'type': 'info', 'message': 'Prepare for behavioral interview questions'})
#     elif overall_score >= 50:
#         recommendations.append({'type': 'warning', 'message': 'You have potential but need to address some gaps'})
#     else:
#         recommendations.append({'type': 'danger', 'message': 'Consider gaining more experience or developing required skills'})
    
#     if missing_skills:
#         recommendations.append({'type': 'skill_gap', 'message': f'Develop these skills: {", ".join(missing_skills[:5])}'})
#         if len(missing_skills) > 0:
#             recommendations.append({'type': 'learning', 'message': 'Consider online courses on platforms like Coursera or Udemy'})
    
#     if candidate_data.get('experience', 0) < job_data.get('required_experience', 0):
#         recommendations.append({'type': 'experience', 'message': f"Gain {job_data.get('required_experience', 0) - candidate_data.get('experience', 0)} more years of relevant experience"})
    
#     return recommendations
# from collections import defaultdict
# import numpy as np

# def calculate_skill_match(candidate_skills, required_skills):
#     if not required_skills: return 0
#     candidate_flat = []
#     for category in candidate_skills.values():
#         candidate_flat.extend([skill.lower() for skill in category])
#     required_flat = [skill.lower() for skill in required_skills]
#     matched_skills = set(candidate_flat).intersection(set(required_flat))
#     if len(required_flat) > 0:
#         return (len(matched_skills) / len(required_flat)) * 100
#     return 0

# def calculate_experience_match(candidate_exp, required_exp):
#     if required_exp == 0: return 100
#     if candidate_exp >= required_exp: return 100
#     return (candidate_exp / required_exp) * 100

# def calculate_education_match(candidate_education, required_education):
#     if not required_education: return 100
#     required_lower = required_education.lower()
#     for education in candidate_education:
#         if required_lower in education.lower(): return 100
#         degree_types = ['bachelor', 'master', 'phd', 'doctorate']
#         required_degree = next((d for d in degree_types if d in required_lower), None)
#         candidate_degree = next((d for d in degree_types if d in education.lower()), None)
#         if required_degree and candidate_degree:
#             hierarchy = {'bachelor': 1, 'master': 2, 'phd': 3, 'doctorate': 3}
#             if hierarchy.get(candidate_degree, 0) >= hierarchy.get(required_degree, 0):
#                 return 100
#     return 0

# def calculate_certification_match(candidate_certs, required_certs):
#     if not required_certs: return 100
#     candidate_lower = [cert.lower() for cert in candidate_certs]
#     required_lower = [cert.lower() for cert in required_certs]
#     matched = set(candidate_lower).intersection(set(required_lower))
#     if len(required_lower) > 0:
#         return (len(matched) / len(required_lower)) * 100
#     return 0

# def calculate_fit_score(candidate_data, job_data):
#     candidate_skills = candidate_data.get('skills', defaultdict(list))
#     candidate_exp = candidate_data.get('experience', 0)
#     candidate_education = candidate_data.get('education', [])
#     candidate_certs = candidate_data.get('certifications', [])
    
#     required_skills = job_data.get('required_skills', [])
#     required_exp = job_data.get('required_experience', 0)
#     required_education = job_data.get('required_education', '')
#     required_certs = job_data.get('certifications', [])
    
#     skill_score = calculate_skill_match(candidate_skills, required_skills)
#     exp_score = calculate_experience_match(candidate_exp, required_exp)
#     edu_score = calculate_education_match(candidate_education, required_education)
#     cert_score = calculate_certification_match(candidate_certs, required_certs)
    
#     weights = {'skill': 0.40, 'experience': 0.30, 'education': 0.20, 'certification': 0.10}
#     overall_score = round(
#         skill_score * weights['skill'] +
#         exp_score * weights['experience'] +
#         edu_score * weights['education'] +
#         cert_score * weights['certification'], 2
#     )
    
#     if overall_score >= 70: eligibility = "Eligible"
#     elif overall_score >= 50: eligibility = "Partially Eligible"
#     else: eligibility = "Not Eligible"
    
#     # REQUIRED for your new dashboard:
#     component_scores = {
#         'skill': round(skill_score, 2),
#         'experience': round(exp_score, 2),
#         'education': round(edu_score, 2),
#         'certification': round(cert_score, 2)
#     }
    
#     candidate_flat = []
#     for category in candidate_skills.values():
#         candidate_flat.extend([skill.lower() for skill in category])
#     required_flat = [skill.lower() for skill in required_skills]
    
#     return {
#         'overall_score': overall_score,
#         'component_scores': component_scores, # HTML uses this
#         'eligibility': eligibility,
#         'missing_skills': list(set(required_flat) - set(candidate_flat)),
#         'matched_skills_count': len(set(candidate_flat).intersection(set(required_flat))), # Visualizations use this
#         'required_skills_count': len(required_flat) # Visualizations use this
#     }

# def generate_recommendations(candidate_data, job_data, fit_results):
#     recommendations = []
#     overall_score = fit_results['overall_score']
#     missing_skills = fit_results['missing_skills']
    
#     if overall_score >= 70:
#         recommendations.append({'type': 'success', 'message': 'You are highly qualified for this position!'})
#         recommendations.append({'type': 'info', 'message': 'Prepare for behavioral interview questions'})
#     elif overall_score >= 50:
#         recommendations.append({'type': 'warning', 'message': 'You have potential but need to address some gaps'})
#     else:
#         recommendations.append({'type': 'danger', 'message': 'Consider gaining more experience or developing required skills'})
    
#     if missing_skills:
#         recommendations.append({'type': 'skill_gap', 'message': f'Develop these skills: {", ".join(missing_skills[:5])}'})
#         if len(missing_skills) > 0:
#             recommendations.append({'type': 'learning', 'message': 'Consider online courses on platforms like Coursera or Udemy'})
    
#     if candidate_data.get('experience', 0) < job_data.get('required_experience', 0):
#         recommendations.append({'type': 'experience', 'message': f"Gain {job_data.get('required_experience', 0) - candidate_data.get('experience', 0)} more years of relevant experience"})
    
#     return recommendations

from collections import defaultdict
import numpy as np

def calculate_skill_match(candidate_skills, required_skills):
    """
    Calculate skill match percentage based on intersection of sets.
    Returns 0-100.
    """
    if not required_skills:
        return 0
    
    # Flatten candidate skills from categories into one list
    candidate_flat = []
    for category in candidate_skills.values():
        candidate_flat.extend([skill.lower() for skill in category])
    
    # Prepare required skills
    required_flat = [skill.lower() for skill in required_skills]
    
    # Find intersection
    matched_skills = set(candidate_flat).intersection(set(required_flat))
    
    if len(required_flat) > 0:
        return (len(matched_skills) / len(required_flat)) * 100
    return 0

def calculate_experience_match(candidate_exp, required_exp):
    """
    Calculate experience match percentage.
    - If required is 0, match is 100%.
    - If candidate has >= required, match is 100%.
    - Otherwise, returns percentage of required years.
    """
    if required_exp == 0:
        return 100
    
    if candidate_exp >= required_exp:
        return 100
    
    # Linear scaling for partial match
    return (candidate_exp / required_exp) * 100

def calculate_education_match(candidate_education, required_education):
    """
    Calculate education match based on degree hierarchy.
    PhD > Master > Bachelor
    """
    if not required_education:
        return 100
    
    required_lower = required_education.lower()
    
    # Check if any of the candidate's education entries match or exceed the requirement
    for education in candidate_education:
        education_lower = education.lower()
        
        # Direct string match
        if required_lower in education_lower:
            return 100
        
        # Hierarchy check
        degree_types = ['bachelor', 'master', 'phd', 'doctorate']
        
        # Find the degree level in the requirement
        required_degree = next((d for d in degree_types if d in required_lower), None)
        
        # Find the degree level in this specific education entry
        candidate_degree = next((d for d in degree_types if d in education_lower), None)
        
        if required_degree and candidate_degree:
            # Hierarchy: Bachelor=1, Master=2, PhD/Doctorate=3
            hierarchy = {'bachelor': 1, 'master': 2, 'phd': 3, 'doctorate': 3}
            
            if hierarchy.get(candidate_degree, 0) >= hierarchy.get(required_degree, 0):
                return 100
    
    return 0

def calculate_certification_match(candidate_certs, required_certs):
    """
    Calculate certification match percentage.
    """
    if not required_certs:
        return 100
    
    candidate_lower = [cert.lower() for cert in candidate_certs]
    required_lower = [cert.lower() for cert in required_certs]
    
    matched = set(candidate_lower).intersection(set(required_lower))
    
    if len(required_lower) > 0:
        return (len(matched) / len(required_lower)) * 100
    return 0

def calculate_fit_score(candidate_data, job_data):
    """
    Calculate overall fit score based ONLY on credentials (Exp, Edu, Certs).
    """
    # Extract Data
    candidate_skills = candidate_data.get('skills', defaultdict(list))
    candidate_exp = candidate_data.get('experience', 0)
    candidate_education = candidate_data.get('education', [])
    candidate_certs = candidate_data.get('certifications', [])
    
    required_skills = job_data.get('required_skills', [])
    required_exp = job_data.get('required_experience', 0)
    required_education = job_data.get('required_education', '')
    required_certs = job_data.get('certifications', [])
    
    # Calculate Component Scores
    skill_score = calculate_skill_match(candidate_skills, required_skills)
    exp_score = calculate_experience_match(candidate_exp, required_exp)
    edu_score = calculate_education_match(candidate_education, required_education)
    cert_score = calculate_certification_match(candidate_certs, required_certs)
    
    # --- UPDATED WEIGHTS ---
    # Skills are removed from the calculation (0.00)
    # Weights redistributed to Experience, Education, and Certifications
    weights = {
        'skill': 0.00,       # Excluded from scoring
        'experience': 0.50,  # 50% importance
        'education': 0.30,   # 30% importance
        'certification': 0.20 # 20% importance
    }
    
    overall_score = round(
        skill_score * weights['skill'] +
        exp_score * weights['experience'] +
        edu_score * weights['education'] +
        cert_score * weights['certification'], 2
    )
    
    # Determine Eligibility
    if overall_score >= 70:
        eligibility = "Eligible"
    elif overall_score >= 50:
        eligibility = "Partially Eligible"
    else:
        eligibility = "Not Eligible"
    
    # Prepare data for return (and visualization)
    component_scores = {
        'skill': round(skill_score, 2), # Still returning this so the UI can show the % even if it doesn't count
        'experience': round(exp_score, 2),
        'education': round(edu_score, 2),
        'certification': round(cert_score, 2)
    }
    
    # Helper for skill gap analysis
    candidate_flat = []
    for category in candidate_skills.values():
        candidate_flat.extend([skill.lower() for skill in category])
    required_flat = [skill.lower() for skill in required_skills]
    
    return {
        'overall_score': overall_score,
        'component_scores': component_scores,
        'eligibility': eligibility,
        'missing_skills': list(set(required_flat) - set(candidate_flat)),
        'matched_skills_count': len(set(candidate_flat).intersection(set(required_flat))),
        'required_skills_count': len(required_flat)
    }

def generate_recommendations(candidate_data, job_data, fit_results):
    """
    Generate text recommendations based on score and gaps.
    """
    recommendations = []
    overall_score = fit_results['overall_score']
    missing_skills = fit_results['missing_skills']
    
    # Score-based Feedback
    if overall_score >= 70:
        recommendations.append({'type': 'success', 'message': 'You are highly qualified for this position based on your credentials!'})
        recommendations.append({'type': 'info', 'message': 'Prepare for behavioral interview questions.'})
    elif overall_score >= 50:
        recommendations.append({'type': 'warning', 'message': 'You meet some credentials but have gaps to address.'})
    else:
        recommendations.append({'type': 'danger', 'message': 'Your credentials (experience/education) do not fully match the requirements.'})
    
    # Experience Feedback
    if candidate_data.get('experience', 0) < job_data.get('required_experience', 0):
        diff = job_data.get('required_experience', 0) - candidate_data.get('experience', 0)
        recommendations.append({'type': 'experience', 'message': f"This job requires {diff} more year(s) of relevant experience."})
    
    # Certification Feedback
    # Check if certifications were required but score was < 100
    if job_data.get('certifications') and fit_results['component_scores']['certification'] < 100:
        recommendations.append({'type': 'certification', 'message': 'You are missing some required certifications.'})
    
    # Skill Feedback (Still useful to show even if not scored)
    if missing_skills:
        recommendations.append({'type': 'skill_gap', 'message': f'Note: You are missing these skills: {", ".join(missing_skills[:5])}'})
    
    return recommendations
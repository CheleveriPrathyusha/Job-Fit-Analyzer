import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json

def create_gauge_chart(score):
    """Create a gauge chart for overall score"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Overall Fit Score", 'font': {'size': 24}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#2563eb"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': "#fee2e2"},  # Red
                {'range': [50, 70], 'color': "#fef3c7"}, # Yellow
                {'range': [70, 100], 'color': "#dcfce7"} # Green
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))
    fig.update_layout(height=350, margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig.to_json()

def create_skill_distribution_chart(candidate_skills):
    """Pie chart of candidate's skill categories"""
    categories = []
    counts = []
    
    if isinstance(candidate_skills, dict):
        for category, skills in candidate_skills.items():
            if skills:
                categories.append(category.replace('_', ' ').capitalize())
                counts.append(len(skills))
    
    if not categories:
        categories = ['No Skills Detected']
        counts = [1]
    
    fig = go.Figure(data=[go.Pie(
        labels=categories, 
        values=counts, 
        hole=.4,
        marker_colors=px.colors.qualitative.Prism
    )])
    fig.update_layout(
        title="Your Skill Profile",
        height=350,
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    return fig.to_json()

def create_comparison_chart(candidate_count, job_count):
    """NEW: Bar chart comparing Candidate Skill Count vs Job Requirement Count"""
    fig = go.Figure(data=[
        go.Bar(
            name='You Have', 
            x=['Skills Count'], 
            y=[candidate_count],
            marker_color='#22c55e', # Green
            text=[candidate_count],
            textposition='auto'
        ),
        go.Bar(
            name='Job Requires', 
            x=['Skills Count'], 
            y=[job_count],
            marker_color='#3b82f6', # Blue
            text=[job_count],
            textposition='auto'
        )
    ])
    fig.update_layout(
        title="Skill Gap Analysis (Count)",
        barmode='group',
        height=350,
        margin=dict(l=20, r=20, t=50, b=20),
        yaxis=dict(title="Number of Skills"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig.to_json()

def create_missing_skills_chart(missing_skills):
    """Horizontal bar chart for missing skills"""
    if not missing_skills:
        fig = go.Figure()
        fig.update_layout(
            title="No Missing Skills! Great Job!",
            height=200,
            xaxis={'visible': False},
            yaxis={'visible': False}
        )
        return fig.to_json()
    
    # Limit to top 10
    display_skills = missing_skills[:10]
    
    fig = go.Figure(data=[go.Bar(
        x=[100] * len(display_skills), 
        y=display_skills, 
        orientation='h', 
        marker_color='#ef4444', # Red
        text=display_skills,
        textposition='inside',
        insidetextanchor='middle'
    )])
    
    fig.update_layout(
        title="Top Missing Required Skills",
        xaxis_title="", 
        yaxis_title="", 
        xaxis=dict(showticklabels=False, range=[0, 100]),
        yaxis=dict(showticklabels=False),
        height=max(250, len(display_skills) * 40),
        margin=dict(l=20, r=20, t=50, b=20)
    )
    return fig.to_json()

def create_visualizations(fit_results, candidate_data, job_data):
    # Calculate counts for the comparison chart
    candidate_skill_count = fit_results.get('matched_skills_count', 0)
    job_req_count = fit_results.get('required_skills_count', 0)
    
    # Create all charts including the new comparison_chart
    return {
        'gauge_chart': create_gauge_chart(fit_results['overall_score']),
        'skill_distribution': create_skill_distribution_chart(candidate_data.get('skills', {})),
        'comparison_chart': create_comparison_chart(candidate_skill_count, job_req_count),
        'missing_skills': create_missing_skills_chart(fit_results.get('missing_skills', []))
    }
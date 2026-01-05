import os
from datetime import timedelta

class Config:
    # MongoDB Configuration
    MONGO_URI = "mongodb://localhost:27017/job_fit_analyzer"
    
    # File Upload Configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}
    
    # Secret Key for Sessions
    SECRET_KEY = 'your-secret-key-here-change-in-production'
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # NLP Model
    SPACY_MODEL = "en_core_web_sm"
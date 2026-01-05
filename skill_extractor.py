import json
import spacy
import re
from collections import defaultdict

class SkillExtractor:
    def __init__(self):
        # Load spaCy model
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            print("Warning: spaCy model not found. Run: python -m spacy download en_core_web_sm")
            self.nlp = None
        
        # Load skills database
        self.skills_db = self._load_skills_database()
    
    def _load_skills_database(self):
        """Load skills from JSON database"""
        try:
            with open('skills_database.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("Warning: skills_database.json not found. Using default skills.")
            return self._create_default_skills()
    
    def _create_default_skills(self):
        """Create a default skills database if file doesn't exist"""
        return {
            "technical": [
                "Python", "JavaScript", "Java", "C++", "C#", "PHP", "Ruby", "Go", "Swift", "Kotlin",
                "React", "Angular", "Vue.js", "Node.js", "Django", "Flask", "Spring", "Laravel",
                "MySQL", "PostgreSQL", "MongoDB", "Redis", "Oracle", "SQLite",
                "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Jenkins", "Git", "CI/CD",
                "Machine Learning", "Deep Learning", "Data Science", "NLP", "Computer Vision",
                "TensorFlow", "PyTorch", "Scikit-learn", "Pandas", "NumPy", "Tableau", "Power BI"
            ],
            "soft": [
                "Communication", "Leadership", "Teamwork", "Problem Solving", "Critical Thinking",
                "Time Management", "Adaptability", "Creativity", "Work Ethic", "Attention to Detail",
                "Interpersonal Skills", "Conflict Resolution", "Decision Making", "Strategic Planning",
                "Emotional Intelligence", "Negotiation", "Presentation Skills"
            ],
            "tools": [
                "Git", "Jira", "Confluence", "Slack", "Microsoft Office", "Google Workspace",
                "VS Code", "IntelliJ", "Eclipse", "PyCharm", "Postman", "Docker", "Kubernetes",
                "AWS Console", "Azure Portal", "Google Cloud Console", "Jenkins", "Travis CI",
                "GitLab CI", "CircleCI", "Ansible", "Terraform"
            ]
        }
    
    def extract_skills(self, text):
        """Extract skills from text using dictionary matching"""
        if not text:
            return defaultdict(list)
        
        text_lower = text.lower()
        found_skills = defaultdict(list)
        
        # Check each category
        for category, skills in self.skills_db.items():
            for skill in skills:
                # Create a regex pattern that matches the skill as a whole word
                pattern = r'\b' + re.escape(skill.lower()) + r'\b'
                if re.search(pattern, text_lower):
                    found_skills[category].append(skill)
        
        # Use spaCy for additional skill extraction if available
        if self.nlp:
            doc = self.nlp(text)
            
            # Extract noun chunks that might be skills
            for chunk in doc.noun_chunks:
                chunk_text = chunk.text.strip()
                if len(chunk_text.split()) <= 3:  # Limit to 3-word phrases
                    # Check if it's already in our found skills
                    found = False
                    for category_skills in found_skills.values():
                        if chunk_text in category_skills:
                            found = True
                            break
                    
                    if not found:
                        # Add to technical skills as potential new skill
                        found_skills['technical'].append(chunk_text)
        
        # Remove duplicates while preserving order
        for category in found_skills:
            found_skills[category] = list(dict.fromkeys(found_skills[category]))
        
        return found_skills

# Global instance
skill_extractor = SkillExtractor()

def extract_skills(text):
    """Convenience function to extract skills"""
    return skill_extractor.extract_skills(text)
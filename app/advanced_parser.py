import re
import spacy
from collections import Counter
from typing import List, Dict
import json

# Try to load spacy model, if not available use basic extraction
try:
    nlp = spacy.load("en_core_web_sm")
    SPACY_AVAILABLE = True
except OSError:
    SPACY_AVAILABLE = False
    nlp = None

# Comprehensive skills database
TECHNICAL_SKILLS = {
    'programming_languages': [
        'python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'kotlin',
        'swift', 'typescript', 'scala', 'r', 'matlab', 'perl', 'sql', 'html', 'css'
    ],
    'frameworks': [
        'react', 'angular', 'vue', 'django', 'flask', 'spring', 'express', 'laravel',
        'rails', 'asp.net', 'bootstrap', 'jquery', 'node.js', 'next.js', 'nuxt'
    ],
    'databases': [
        'mysql', 'postgresql', 'mongodb', 'sqlite', 'oracle', 'sql server', 'redis',
        'elasticsearch', 'cassandra', 'dynamodb', 'firebase', 'mariadb'
    ],
    'cloud_platforms': [
        'aws', 'azure', 'google cloud', 'gcp', 'docker', 'kubernetes', 'terraform',
        'jenkins', 'gitlab', 'github actions', 'circleci', 'travis ci'
    ],
    'data_science': [
        'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'scikit-learn',
        'pandas', 'numpy', 'matplotlib', 'seaborn', 'jupyter', 'tableau', 'power bi',
        'apache spark', 'hadoop', 'kafka', 'airflow'
    ],
    'tools': [
        'git', 'linux', 'bash', 'powershell', 'vim', 'vscode', 'intellij', 'eclipse',
        'postman', 'swagger', 'jira', 'confluence', 'slack', 'notion'
    ]
}

SOFT_SKILLS = [
    'leadership', 'communication', 'teamwork', 'problem solving', 'analytical thinking',
    'project management', 'time management', 'adaptability', 'creativity', 'critical thinking',
    'collaboration', 'presentation', 'negotiation', 'customer service', 'mentoring',
    'strategic planning', 'innovation', 'decision making', 'conflict resolution'
]

def extract_skills(resume_text: str, job_text: str = "") -> List[str]:
    """Extract skills from resume text, prioritizing those mentioned in job description"""
    resume_lower = resume_text.lower()
    job_lower = job_text.lower() if job_text else ""
    
    found_skills = set()
    
    # Extract technical skills
    for category, skills_list in TECHNICAL_SKILLS.items():
        for skill in skills_list:
            if skill in resume_lower:
                found_skills.add(skill.title())
    
    # Extract soft skills
    for skill in SOFT_SKILLS:
        if skill in resume_lower:
            found_skills.add(skill.title())
    
    # Use spaCy for better skill extraction if available
    if SPACY_AVAILABLE and nlp:
        doc = nlp(resume_text)
        for ent in doc.ents:
            if ent.label_ in ['ORG', 'PRODUCT', 'SKILL']:  # Organizations and products often indicate skills
                skill_candidate = ent.text.lower().strip()
                if len(skill_candidate) > 2 and skill_candidate.isalpha():
                    found_skills.add(ent.text.title())
    
    skills_list = list(found_skills)
    
    # Prioritize skills mentioned in job description
    if job_text:
        job_skills = []
        other_skills = []
        
        for skill in skills_list:
            if skill.lower() in job_lower:
                job_skills.append(skill)
            else:
                other_skills.append(skill)
        
        return job_skills + other_skills
    
    return sorted(skills_list)

def extract_experience(resume_text: str) -> int:
    """Extract years of experience from resume text"""
    text = resume_text.lower()
    
    # Common patterns for experience
    patterns = [
        r'(\d+)\+?\s*years?\s*(?:of\s*)?(?:professional\s*)?experience',
        r'(\d+)\+?\s*years?\s*(?:in|with|of)',
        r'experience\s*[:\-]\s*(\d+)\+?\s*years?',
        r'(\d+)\+?\s*yrs?\s*(?:of\s*)?(?:professional\s*)?experience',
        r'over\s*(\d+)\s*years?',
        r'more than\s*(\d+)\s*years?',
        r'(\d+)\+\s*years?'
    ]
    
    max_years = 0
    
    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            try:
                years = int(match)
                max_years = max(max_years, years)
            except ValueError:
                continue
    
    # Alternative approach: count job positions and estimate
    if max_years == 0:
        job_patterns = [
            r'(\d{4})\s*[-–—]\s*(\d{4}|\bpresent\b|\bcurrent\b)',
            r'(\d{4})\s*[-–—]\s*(\d{4})'
        ]
        
        total_months = 0
        for pattern in job_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for start_year, end_year in matches:
                try:
                    start = int(start_year)
                    if end_year.lower() in ['present', 'current']:
                        end = 2024  # Current year
                    else:
                        end = int(end_year)
                    
                    if end >= start:
                        total_months += (end - start) * 12
                except ValueError:
                    continue
        
        max_years = total_months // 12
    
    return min(max_years, 50)  # Cap at 50 years

def extract_education(resume_text: str) -> str:
    """Extract education information from resume text"""
    text = resume_text.lower()
    
    # Education levels
    education_levels = [
        ('phd', 'Ph.D.'),
        ('doctorate', 'Doctorate'),
        ('master', 'Master\'s Degree'),
        ('mba', 'MBA'),
        ('bachelor', 'Bachelor\'s Degree'),
        ('associate', 'Associate Degree'),
        ('diploma', 'Diploma'),
        ('certificate', 'Certificate'),
        ('high school', 'High School')
    ]
    
    found_education = []
    
    for keyword, formal_name in education_levels:
        if keyword in text:
            found_education.append(formal_name)
    
    # Extract degree fields
    degree_fields = [
        'computer science', 'engineering', 'business', 'marketing', 'finance',
        'economics', 'mathematics', 'statistics', 'physics', 'chemistry',
        'biology', 'psychology', 'sociology', 'english', 'literature',
        'history', 'philosophy', 'law', 'medicine', 'nursing'
    ]
    
    for field in degree_fields:
        if field in text:
            found_education.append(f"in {field.title()}")
    
    # Extract university names (basic pattern)
    university_patterns = [
        r'university of ([a-z\s]+)',
        r'([a-z\s]+) university',
        r'([a-z\s]+) institute of technology',
        r'([a-z\s]+) college'
    ]
    
    for pattern in university_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            if len(match.strip()) > 3:
                found_education.append(f"from {match.strip().title()}")
    
    if found_education:
        return "; ".join(found_education[:3])  # Limit to top 3
    else:
        return "Not specified"

def extract_certifications(resume_text: str) -> List[str]:
    """Extract professional certifications"""
    text = resume_text.lower()
    
    common_certs = [
        'aws certified', 'azure certified', 'google cloud certified',
        'cissp', 'cisa', 'cism', 'comptia', 'ccna', 'ccnp', 'ccie',
        'pmp', 'prince2', 'scrum master', 'agile', 'itil',
        'cpa', 'cfa', 'frm', 'cma', 'cia'
    ]
    
    found_certs = []
    
    for cert in common_certs:
        if cert in text:
            found_certs.append(cert.title())
    
    # Look for certification patterns
    cert_patterns = [
        r'certified\s+([a-z\s]+)',
        r'([a-z\s]+)\s+certified',
        r'certification\s*[:\-]\s*([a-z\s]+)'
    ]
    
    for pattern in cert_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            if len(match.strip()) > 2:
                found_certs.append(match.strip().title())
    
    return list(set(found_certs))[:5]  # Return unique certifications, max 5

def analyze_resume_sections(resume_text: str) -> Dict:
    """Analyze different sections of a resume"""
    text_lower = resume_text.lower()
    
    sections = {
        'has_summary': any(keyword in text_lower for keyword in ['summary', 'objective', 'profile']),
        'has_experience': any(keyword in text_lower for keyword in ['experience', 'work history', 'employment']),
        'has_education': any(keyword in text_lower for keyword in ['education', 'degree', 'university', 'college']),
        'has_skills': any(keyword in text_lower for keyword in ['skills', 'technical skills', 'competencies']),
        'has_projects': any(keyword in text_lower for keyword in ['projects', 'portfolio', 'github']),
        'has_certifications': any(keyword in text_lower for keyword in ['certification', 'certified', 'license']),
        'contact_info': extract_contact_info(resume_text)
    }
    
    return sections

def extract_contact_info(resume_text: str) -> Dict:
    """Extract contact information from resume"""
    contact = {
        'email': None,
        'phone': None,
        'linkedin': None,
        'github': None
    }
    
    # Email pattern
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, resume_text)
    if emails:
        contact['email'] = emails[0]
    
    # Phone pattern
    phone_pattern = r'[\+]?[1-9]?[0-9]{7,14}'
    phones = re.findall(phone_pattern, resume_text)
    if phones:
        contact['phone'] = phones[0]
    
    # LinkedIn pattern
    linkedin_pattern = r'linkedin\.com/in/([a-zA-Z0-9\-]+)'
    linkedin_matches = re.findall(linkedin_pattern, resume_text.lower())
    if linkedin_matches:
        contact['linkedin'] = f"linkedin.com/in/{linkedin_matches[0]}"
    
    # GitHub pattern
    github_pattern = r'github\.com/([a-zA-Z0-9\-]+)'
    github_matches = re.findall(github_pattern, resume_text.lower())
    if github_matches:
        contact['github'] = f"github.com/{github_matches[0]}"
    
    return contact

def calculate_resume_score(resume_text: str, job_text: str) -> Dict:
    """Calculate comprehensive resume score"""
    sections = analyze_resume_sections(resume_text)
    
    score_breakdown = {
        'content_completeness': 0,
        'keyword_relevance': 0,
        'experience_relevance': 0,
        'skill_match': 0,
        'total_score': 0
    }
    
    # Content completeness (40 points max)
    completeness_score = 0
    if sections['has_summary']: completeness_score += 5
    if sections['has_experience']: completeness_score += 15
    if sections['has_education']: completeness_score += 10
    if sections['has_skills']: completeness_score += 10
    
    score_breakdown['content_completeness'] = completeness_score
    
    # Keyword relevance (30 points max)
    job_keywords = set(re.findall(r'\b\w+\b', job_text.lower()))
    resume_keywords = set(re.findall(r'\b\w+\b', resume_text.lower()))
    
    # Remove common words
    common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    job_keywords -= common_words
    resume_keywords -= common_words
    
    if job_keywords:
        keyword_match_ratio = len(job_keywords.intersection(resume_keywords)) / len(job_keywords)
        score_breakdown['keyword_relevance'] = min(30, keyword_match_ratio * 30)
    
    # Calculate total score
    score_breakdown['total_score'] = sum([
        score_breakdown['content_completeness'],
        score_breakdown['keyword_relevance']
    ])
    
    return score_breakdown

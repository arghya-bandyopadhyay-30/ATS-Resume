import json
import pandas as pd
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def _normalize_skill(skill: str) -> str:
    """Normalize skill name for comparison."""
    return skill.lower().replace('_', ' ').strip()

def _is_skill_match(candidate_skill: str, jd_skill: str) -> bool:
    """Check if candidate skill matches JD skill, considering partial matches."""
    candidate_norm = _normalize_skill(candidate_skill)
    jd_norm = _normalize_skill(jd_skill)
    
    # Exact match
    if candidate_norm == jd_norm:
        return True
        
    # Check if JD skill is contained in candidate skill
    if jd_norm in candidate_norm:
        return True
        
    # Check if candidate skill is contained in JD skill
    if candidate_norm in jd_norm:
        return True
        
    # Check for common variations
    variations = {
        'programming_languages': ['python', 'java', 'javascript', 'typescript', 'c#', 'c++', 'ruby', 'go', 'rust'],
        'frameworks_tools': ['react', 'angular', 'vue', 'django', 'flask', 'spring', 'express', 'node.js'],
        'databases': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'cassandra', 'dynamodb'],
        'cloud_platforms': ['aws', 'azure', 'gcp', 'cloud', 'kubernetes', 'docker', 'terraform'],
        'methodologies': ['agile', 'scrum', 'waterfall', 'devops', 'ci_cd', 'tdd', 'bdd']
    }
    
    for category, skills in variations.items():
        if candidate_norm == category and jd_norm in skills:
            return True
        if jd_norm == category and candidate_norm in skills:
            return True
            
    return False

def build_candidate_profiles(csv_path: str, jd_weights_path: str) -> List[Dict]:
    """
    Build candidate profiles from parsed resume data and JD weights.

    Args:
        csv_path: Path to the parsed resume skills CSV file
        jd_weights_path: Path to the JD weights JSON file

    Returns:
        List of candidate profile dictionaries with skill scores
    """
    # Load JD weights
    logger.info("Loading JD weights...")
    with open(jd_weights_path, 'r') as f:
        jd_weights = json.load(f)
    logger.info(f"Loaded JD weights with {len(jd_weights)} skills")

    # Load and group CSV data by candidate
    logger.info("Loading and processing resume data...")
    df = pd.read_csv(csv_path)
    candidate_groups = df.groupby('candidate_name')

    candidate_profiles = []

    # Process each candidate
    for candidate_name, group in candidate_groups:
        logger.info(f"Processing candidate: {candidate_name}")

        # Initialize candidate profile
        profile = {
            "name": candidate_name,
            "summary": group['summary'].iloc[0],
            "languages": group['languages'].iloc[0],
            "certifications": group['certifications'].iloc[0],
            "role": group['role'].iloc[0]
        }

        # Calculate scores for each JD skill
        for skill, weight in jd_weights.items():
            # Find matching skills in candidate's data
            matching_skills = group[group['skill'].apply(lambda x: _is_skill_match(x, skill))]
            
            if not matching_skills.empty:
                # Get the best matching skill's metrics
                best_skill = matching_skills.iloc[0]
                experience_years = float(best_skill['skill_experience_years'])
                count = float(best_skill['skill_count'])
                age = float(best_skill['skill_age'])

                # Calculate age normalization
                age_normalized = min(age / 24, 1.0) if age > 0 else 0.0

                # Calculate skill score with adjusted weights
                score = (0.4 * experience_years) + (0.3 * count) + (0.3 * (1 - age_normalized))
            else:
                # Check if skill is in summary/languages/certifications
                text_fields = [
                    str(profile['summary']).lower(),
                    str(profile['languages']).lower(),
                    str(profile['certifications']).lower()
                ]

                # Check for partial matches in text fields
                score = 0.0
                for field in text_fields:
                    if _normalize_skill(skill) in field:
                        score = 0.5  # Give partial credit for mentions in text
                        break

            profile[skill] = score

        candidate_profiles.append(profile)
        logger.info(f"Completed processing candidate: {candidate_name}")

    logger.info(f"Successfully processed {len(candidate_profiles)} candidates")
    return candidate_profiles

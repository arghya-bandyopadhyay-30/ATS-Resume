import json
import pandas as pd
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
            "certifications": group['certifications'].iloc[0]
        }

        # Calculate scores for each JD skill
        for skill, weight in jd_weights.items():
            # Check if skill exists in candidate's data
            skill_data = group[group['skill'].str.lower() == skill.lower()]

            if not skill_data.empty:
                # Get skill metrics
                experience_years = float(skill_data['skill_experience_years'].iloc[0])
                count = float(skill_data['skill_count'].iloc[0])
                age = float(skill_data['skill_age'].iloc[0])

                # Calculate age normalization
                age_normalized = min(age / 24, 1.0) if age > 0 else 0.0

                # Calculate skill score
                score = (0.4 * experience_years) + (0.3 * count) + (0.3 * (1 - age_normalized))
            else:
                # Check if skill is in summary/languages/certifications
                text_fields = [
                    str(profile['summary']).lower(),
                    str(profile['languages']).lower(),
                    str(profile['certifications']).lower()
                ]

                score = 1.0 if any(skill.lower() in field for field in text_fields) else 0.0

            profile[skill] = score

        candidate_profiles.append(profile)
        logger.info(f"Completed processing candidate: {candidate_name}")

    logger.info(f"Successfully processed {len(candidate_profiles)} candidates")
    return candidate_profiles

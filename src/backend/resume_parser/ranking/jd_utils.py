import json
import csv
import os
from typing import Dict
from src.backend.resume_parser.ranking.jd_analyzer import generate_weights_from_jd
from src.backend.resume_parser.config_models import ResumeParserConfig

def analyze_jd_text(jd_text: str, base_dir: str, config: ResumeParserConfig, csv_output_path: str) -> Dict[str, float]:
    """
    Analyze job description text and generate skill weights.
    
    Args:
        jd_text: The job description text to analyze
        base_dir: Base directory for the resume parser
        config: ResumeParserConfig instance
        csv_output_path: Path to the parsed resume skills CSV
        
    Returns:
        Dictionary of skill weights
    """
    try:
        # Extract distinct skills from CSV
        with open(csv_output_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            skills = {row['skill'].strip().lower() for row in reader if row.get('skill')}
            keywords = sorted(skills)
        print(f"[INFO] Extracted {len(keywords)} distinct skill keywords: {keywords}")

        # Format skills list for the prompt
        skills_list = "\n".join(f"- {skill}" for skill in keywords)

        # Generate weights
        jd_prompt_path = os.path.join(base_dir, 'prompt', 'jd_prompt.txt')
        weights = generate_weights_from_jd(jd_text, jd_prompt_path, config.llm, skills_list)
        print("[SUCCESS] Generated JD weights")

        # Save weights JSON
        weights_path = os.path.join(base_dir, 'output', 'jd_weights.json')
        with open(weights_path, 'w', encoding='utf-8') as file:
            json.dump(weights, file, indent=2, ensure_ascii=False)
        print(f"[SUCCESS] Saved JD weights to {weights_path}")

        return weights

    except Exception as e:
        print(f"[ERROR] JD analysis failed: {e}")
        raise 
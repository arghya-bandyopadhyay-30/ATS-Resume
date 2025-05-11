import csv
import json
import os

import yaml

from src.backend.resume_parser.config_models import ResumeParserConfig, LLMConfig
from src.backend.resume_parser.parser.extractor import extract_resume_json, extract_skill_entries
from src.backend.resume_parser.parser.reader import extract_text_from_docx
from src.backend.resume_parser.parser.writer import write_skill_entries_to_csv
from src.backend.resume_parser.ranking.jd_analyzer import generate_weights_from_jd
from src.backend.resume_parser.ranking.scorer import build_candidate_profiles
from src.backend.resume_parser.ranking.ranker import rank_candidates


def load_config(config_path: str) -> ResumeParserConfig:
    with open(config_path, 'r') as file:
        config_dict = yaml.safe_load(file)

    llm_cfg = config_dict['llm']
    return ResumeParserConfig(
        data_folder=config_dict['data_folder'],
        resume_extension=config_dict['resume_extension'],
        llm=LLMConfig(
            provider=llm_cfg['provider'],
            model_name=llm_cfg['model_name'],
            endpoint=llm_cfg['endpoint'],
            api_key=llm_cfg['api_key'] or os.getenv("GROQ_API_KEY"),
            temperature=llm_cfg.get('temperature', 0.0),
            max_tokens=llm_cfg.get('max_tokens', 4096)
        )
    )


def _setup_output_directories(base_dir: str, parsed_json_dir: str, csv_output_path: str) -> None:
    """Create necessary output directories if they don't exist."""
    os.makedirs(parsed_json_dir, exist_ok=True)
    os.makedirs(os.path.dirname(csv_output_path), exist_ok=True)


def _parse_single_resume(file_path: str, filename: str, prompt_path: str, llm_config: LLMConfig) -> tuple[dict, list]:
    """Parse a single resume file and extract its JSON and skill entries."""
    try:
        resume_text = extract_text_from_docx(file_path)
        print(f"[INFO] Extracted text from {filename}")
    except Exception as e:
        print(f"[ERROR] Could not read {filename}: {e}")
        return None, []

    try:
        parsed_json = extract_resume_json(resume_text, prompt_path, llm_config)
        print(f"[SUCCESS] Parsed JSON for {filename}")
    except Exception as e:
        print(f"[ERROR] Failed to extract JSON from {filename}: {e}")
        return None, []

    entries = extract_skill_entries(parsed_json)
    return parsed_json, entries


def _save_parsed_json(parsed_json: dict, parsed_json_dir: str, filename: str) -> None:
    """Save parsed JSON to file."""
    base_name, _ = os.path.splitext(filename)
    json_path = os.path.join(parsed_json_dir, f"parsed_{base_name}.json")
    try:
        with open(json_path, 'w', encoding='utf-8') as file:
            json.dump(parsed_json, file, indent=2, ensure_ascii=False)
        print(f"[SUCCESS] Saved parsed JSON to {json_path}")
    except Exception as e:
        print(f"[ERROR] Failed to save JSON for {filename}: {e}")


def _process_resumes(resumes_dir: str, parsed_json_dir: str, prompt_path: str, llm_config: LLMConfig, resume_extension: str) -> list:
    """Process all resumes in the directory and return all skill entries."""
    all_skill_entries = []
    
    for filename in os.listdir(resumes_dir):
        if not filename.lower().endswith(resume_extension.lower()):
            continue

        file_path = os.path.join(resumes_dir, filename)
        parsed_json, entries = _parse_single_resume(file_path, filename, prompt_path, llm_config)
        
        if parsed_json:
            _save_parsed_json(parsed_json, parsed_json_dir, filename)
            all_skill_entries.extend(entries)
    
    return all_skill_entries


def _analyze_job_description(base_dir: str, config: ResumeParserConfig, csv_output_path: str) -> None:
    """Analyze job description and generate weights."""
    try:
        # Load job description
        jd_path = os.path.join(base_dir, config.data_folder, 'job_description.txt')
        with open(jd_path, 'r', encoding='utf-8') as f:
            jd_text = f.read()
        print("[INFO] Loaded job description")

        # Extract distinct skills from CSV
        with open(csv_output_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            skills = {row['skill'].strip().lower() for row in reader if row.get('skill')}
            keywords = sorted(skills)
        print(f"[INFO] Extracted {len(keywords)} distinct skill keywords: {keywords}")

        # Generate weights
        jd_prompt_path = os.path.join(base_dir, 'prompt', 'jd_prompt.txt')
        weights = generate_weights_from_jd(jd_text, jd_prompt_path, config.llm)
        print("[SUCCESS] Generated JD weights")

        # Save weights JSON
        weights_path = os.path.join(base_dir, 'output', 'jd_weights.json')
        with open(weights_path, 'w', encoding='utf-8') as file:
            json.dump(weights, file, indent=2, ensure_ascii=False)
        print(f"[SUCCESS] Saved JD weights to {weights_path}")

    except Exception as e:
        print(f"[ERROR] JD analysis failed: {e}")


def main():
    base_dir = os.path.dirname(__file__)
    config = load_config(os.path.join(base_dir, 'config.yaml'))

    # Resumes directory
    resumes_dir = os.path.join(base_dir, config.data_folder, 'resumes')
    if not os.path.isdir(resumes_dir):
        raise FileNotFoundError(f"Resumes folder not found: {resumes_dir}")

    # Output paths
    parsed_json_dir = os.path.join(base_dir, 'output', 'parsed_resumes')
    csv_output_path = os.path.join(base_dir, 'output', 'parsed_resume_skills.csv')

    _setup_output_directories(base_dir, parsed_json_dir, csv_output_path)

    prompt_path = os.path.join(base_dir, 'prompt', 'resume_prompt.txt')

    # Process all resumes and collect skill entries
    all_skill_entries = _process_resumes(resumes_dir, parsed_json_dir, prompt_path, config.llm, config.resume_extension)

    # Write CSV of skills
    write_skill_entries_to_csv(all_skill_entries, csv_output_path)
    print(f"[SUCCESS] Wrote enriched CSV to {csv_output_path}")

    # Analyze job description and generate weights
    _analyze_job_description(base_dir, config, csv_output_path)

    # Build candidate profiles
    from_path = os.path.join(base_dir, 'output', 'parsed_resume_skills.csv')
    weights_path = os.path.join(base_dir, 'output', 'jd_weights.json')
    candidate_profiles = build_candidate_profiles(from_path, weights_path)
    print(f"[SUCCESS] Built {len(candidate_profiles)} candidate profiles for ranking")

    # Save candidate profiles to JSON for verification
    profiles_path = os.path.join(base_dir, 'output', 'candidate_profiles.json')
    with open(profiles_path, 'w', encoding='utf-8') as f:
        json.dump(candidate_profiles, f, indent=2, ensure_ascii=False)
    print(f"[SUCCESS] Saved candidate profiles to {profiles_path}")

    # Generate final ranking
    rank_candidates()
    print("[SUCCESS] Generated final candidate ranking")


if __name__ == '__main__':
    main()

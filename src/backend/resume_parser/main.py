import os
import yaml
import json
import csv
from dataclasses import dataclass
from parser.reader import extract_text_from_docx
from parser.extractor import extract_resume_json, extract_skill_entries
from parser.writer import write_skill_entries_to_csv
from ranking.jd_analyzer import generate_weights_from_jd

@dataclass
class LLMConfig:
    provider: str
    model_name: str
    endpoint: str
    api_key: str
    temperature: float = 0.0
    max_tokens: int = 4096

@dataclass
class ResumeParserConfig:
    data_folder: str
    resume_extension: str
    llm: LLMConfig


def load_config(config_path: str) -> ResumeParserConfig:
    with open(config_path, 'r') as file:
        config_dict = yaml.safe_load(file)

    if not config_dict:
        raise ValueError("Config file is empty or invalid.")

    required_keys = ['data_folder', 'resume_extension', 'llm']
    if not all(k in config_dict for k in required_keys):
        raise ValueError(f"Missing one of the required config keys: {required_keys}")

    llm_cfg = config_dict['llm']
    for key in ['provider', 'model_name', 'endpoint', 'api_key']:
        if key not in llm_cfg:
            raise ValueError(f"Missing required LLM config key: '{key}'")

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


def main():
    base_dir = os.path.dirname(__file__)
    config = load_config(os.path.join(base_dir, 'config.yaml'))

    # Resumes directory
    resumes_dir = os.path.join(base_dir, config.data_folder, 'resumes')
    if not os.path.isdir(resumes_dir):
        raise FileNotFoundError(f"Resumes folder not found: {resumes_dir}")

    # Output paths
    parsed_json_dir = os.path.join(base_dir, 'output', 'parsed_resumes')
    jd_weights_dir = os.path.join(base_dir, 'output', 'jd_weights')
    csv_output_path = os.path.join(base_dir, 'output', 'parsed_resume_skills.csv')

    os.makedirs(parsed_json_dir, exist_ok=True)
    os.makedirs(jd_weights_dir, exist_ok=True)
    os.makedirs(os.path.dirname(csv_output_path), exist_ok=True)

    prompt_path = os.path.join(base_dir, 'prompt', 'resume_prompt.txt')
    all_skill_entries = []

    # Parse each resume
    for filename in os.listdir(resumes_dir):
        if not filename.lower().endswith(config.resume_extension.lower()):
            continue

        file_path = os.path.join(resumes_dir, filename)
        try:
            resume_text = extract_text_from_docx(file_path)
            print(f"[INFO] Extracted text from {filename}")
        except Exception as e:
            print(f"[ERROR] Could not read {filename}: {e}")
            continue

        try:
            parsed_json = extract_resume_json(resume_text, prompt_path, config.llm)
            print(f"[SUCCESS] Parsed JSON for {filename}")
        except Exception as e:
            print(f"[ERROR] Failed to extract JSON from {filename}: {e}")
            continue

        base_name, _ = os.path.splitext(filename)
        json_path = os.path.join(parsed_json_dir, f"parsed_{base_name}.json")
        try:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(parsed_json, f, indent=2, ensure_ascii=False)
            print(f"[SUCCESS] Saved parsed JSON to {json_path}")
        except Exception as e:
            print(f"[ERROR] Failed to save JSON for {filename}: {e}")

        # collect skill entries
        entries = extract_skill_entries(parsed_json)
        all_skill_entries.extend(entries)

    # Write CSV of skills
    write_skill_entries_to_csv(all_skill_entries, csv_output_path)
    print(f"[SUCCESS] Wrote enriched CSV to {csv_output_path}")

    # JD Analysis
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
        weights = generate_weights_from_jd(jd_text, keywords, jd_prompt_path, config.llm)
        print("[SUCCESS] Generated JD weights")

        # Save weights JSON
        weights_path = os.path.join(jd_weights_dir, 'jd_weights.json')
        with open(weights_path, 'w', encoding='utf-8') as f:
            json.dump(weights, f, indent=2, ensure_ascii=False)
        print(f"[SUCCESS] Saved JD weights to {weights_path}")

    except Exception as e:
        print(f"[ERROR] JD analysis failed: {e}")

if __name__ == "__main__":
    main()

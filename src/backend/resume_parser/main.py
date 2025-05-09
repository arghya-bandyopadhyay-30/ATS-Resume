import os
import yaml
import json
from dataclasses import dataclass
from parser.reader import extract_text_from_docx
from parser.extractor import extract_resume_json, extract_skill_entries
from parser.writer import write_skill_entries_to_csv


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

    llm_config = config_dict['llm']
    for key in ['provider', 'model_name', 'endpoint', 'api_key']:
        if key not in llm_config:
            raise ValueError(f"Missing required LLM config key: '{key}'")

    return ResumeParserConfig(
        data_folder=config_dict['data_folder'],
        resume_extension=config_dict['resume_extension'],
        llm=LLMConfig(
            provider=llm_config['provider'],
            model_name=llm_config['model_name'],
            endpoint=llm_config['endpoint'],
            api_key=llm_config['api_key'] or os.getenv("GROQ_API_KEY"),
            temperature=llm_config.get('temperature', 0.0),
            max_tokens=llm_config.get('max_tokens', 4096)
        )
    )


def main():
    base_dir = os.path.dirname(__file__)
    config = load_config(os.path.join(base_dir, 'config.yaml'))
    data_dir = os.path.join(base_dir, config.data_folder)
    prompt_path = os.path.join(base_dir, 'prompt', 'resume_prompt.txt')
    output_json_dir = os.path.join(base_dir, 'output')
    os.makedirs(output_json_dir, exist_ok=True)

    all_skill_entries = []

    for filename in os.listdir(data_dir):
        if not filename.lower().endswith(config.resume_extension.lower()):
            continue

        file_path = os.path.join(data_dir, filename)
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

        # Save JSON
        base_name, _ = os.path.splitext(filename)
        json_path = os.path.join(output_json_dir, f"parsed_{base_name}.json")
        try:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(parsed_json, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[ERROR] Failed to save JSON for {filename}: {e}")

        # Extract and collect skill entries
        skill_entries = extract_skill_entries(parsed_json)
        all_skill_entries.extend(skill_entries)

    # Write to final CSV
    output_csv_path = os.path.join(base_dir, 'output', 'parsed_resume_skills.csv')
    write_skill_entries_to_csv(all_skill_entries, output_csv_path)
    print(f"[SUCCESS] Wrote enriched CSV to {output_csv_path}")


if __name__ == "__main__":
    main()

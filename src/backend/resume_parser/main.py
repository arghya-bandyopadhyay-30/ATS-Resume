import os
import yaml
import json
from dataclasses import dataclass
from parser.reader import extract_text_from_docx
from parser.extractor import extract_resume_json


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
    print(f"[DEBUG] Loaded config_dict: {config_dict} (type: {type(config_dict)})")
    if not config_dict:
        raise ValueError("Config file is empty or could not be parsed. Please check config.yaml.")
    if 'data_folder' not in config_dict or 'resume_extension' not in config_dict or 'llm' not in config_dict:
        raise ValueError("Missing required config keys: 'data_folder', 'resume_extension', or 'llm'")

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
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    config = load_config(config_path)
    data_dir = os.path.join(os.path.dirname(__file__), config.data_folder)

    if not os.path.isdir(data_dir):
        raise FileNotFoundError(f"Directory '{config.data_folder}' not found at path: {data_dir}")

    resume_texts = []
    for filename in os.listdir(data_dir):
        if filename.lower().endswith(config.resume_extension.lower()):
            try:
                file_path = os.path.join(data_dir, filename)
                resume_text = extract_text_from_docx(file_path)
                resume_texts.append((filename, resume_text))
            except Exception as e:
                print(f"[ERROR] Skipping {filename}: {e}")

    for filename, resume_text in resume_texts:
        print(f"\n----- START OF {filename} -----\n{resume_text}\n----- END OF {filename} -----")

        prompt_path = os.path.join(os.path.dirname(__file__), 'prompt', 'resume_prompt.txt')
        try:
            parsed_json = extract_resume_json(
                resume_text=resume_text,
                prompt_path=prompt_path,
                llm_config=config.llm
            )
            print(f"[SUCCESS] Extracted JSON for {filename}")
        except Exception as e:
            print(f"[ERROR] Failed to extract JSON for {filename}: {e}")
            continue

        output_dir = os.path.join(os.path.dirname(__file__), 'output')
        os.makedirs(output_dir, exist_ok=True)
        base_name, _ = os.path.splitext(filename)
        output_file = os.path.join(output_dir, f"parsed_{base_name}.json")

        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(parsed_json, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[ERROR] Could not save JSON for {filename}: {e}")


if __name__ == "__main__":
    main()

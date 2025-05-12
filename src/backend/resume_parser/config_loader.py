import os
import yaml
from pathlib import Path
from dotenv import load_dotenv
from src.backend.resume_parser.config_models import ResumeParserConfig, LLMConfig

def load_config(config_path: str) -> ResumeParserConfig:
    load_dotenv()

    # Read & expand ${VAR} using os.path.expandvars
    with open(config_path, 'r') as file:
        raw_yaml = file.read()
        expanded_yaml = os.path.expandvars(raw_yaml)
        config_dict = yaml.safe_load(expanded_yaml)

    if "data_folder" not in config_dict:
        raise ValueError("Missing 'data_folder' in the configuration file.")
    if "resume_extension" not in config_dict:
        raise ValueError("Missing 'resume_extension' in the configuration file.")
    if "llm" not in config_dict:
        raise ValueError("Missing 'llm' in the configuration file.")

    llm_cfg = config_dict['llm']

    if "provider" not in llm_cfg:
        raise ValueError("Missing 'provider' in the LLM configuration.")
    if "model_name" not in llm_cfg:
        raise ValueError("Missing 'model_name' in the LLM configuration.")
    if "endpoint" not in llm_cfg:
        raise ValueError("Missing 'endpoint' in the LLM configuration.")
    if "api_key" not in llm_cfg:
        raise ValueError("Missing 'api_key' in the LLM configuration.")


    return ResumeParserConfig(
        data_folder=config_dict['data_folder'],
        resume_extension=config_dict['resume_extension'],
        llm=LLMConfig(
            provider=llm_cfg['provider'],
            model_name=llm_cfg['model_name'],
            endpoint=llm_cfg['endpoint'],
            api_key=llm_cfg['api_key'],
            temperature=llm_cfg.get('temperature', 0.0),
            max_tokens=llm_cfg.get('max_tokens', 4096)
        )
    )

from dataclasses import dataclass


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
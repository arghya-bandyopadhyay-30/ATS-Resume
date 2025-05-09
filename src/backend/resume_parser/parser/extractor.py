import json
import requests
from typing import Dict


class GroqAPIError(Exception):
    """Custom error for Groq-related failures."""


def extract_resume_json(
    resume_text: str,
    prompt_path: str,
    llm_config
) -> Dict:
    """
    Extract structured JSON from resume text using Groq LLM API.

    Args:
        resume_text (str): Resume plain text.
        prompt_path (str): Prompt template path with '{{resume_text}}'.
        llm_config: LLMConfig dataclass with model_name, endpoint, api_key, temperature.

    Returns:
        Dict: Parsed JSON structure.

    Raises:
        GroqAPIError: If API call or parsing fails.
    """
    try:
        with open(prompt_path, 'r', encoding='utf-8') as f:
            prompt_template = f.read()
    except Exception as e:
        raise GroqAPIError(f"Failed to read prompt: {e}")

    prompt = prompt_template.replace("{{resume_text}}", resume_text)

    headers = {
        "Authorization": f"Bearer {llm_config.api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": llm_config.model_name,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": llm_config.temperature,
        "max_tokens": llm_config.max_tokens
    }

    try:
        response = requests.post(llm_config.endpoint, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        resp_json = response.json()

        if (
            "choices" not in resp_json or
            not resp_json["choices"] or
            "message" not in resp_json["choices"][0] or
            "content" not in resp_json["choices"][0]["message"]
        ):
            raise GroqAPIError(f"Unexpected response structure from Groq: {resp_json}")
        
        content = resp_json["choices"][0]["message"]["content"].strip()

        if not content:
            raise GroqAPIError(f"Empty content in Groq response: {resp_json}")
        
        if content.startswith('```'):
            lines = content.split('\n')
            if lines[0].startswith('```'):
                lines = lines[1:]
            if lines and lines[-1].strip() == '```':
                lines = lines[:-1]
            content = '\n'.join(lines).strip()
        
        try:
            return json.loads(content)
        except Exception as parse_err:
            raise GroqAPIError(f"Failed to parse JSON from Groq content: {content}\nError: {parse_err}")
    except Exception as e:
        raise GroqAPIError(f"Failed to get or parse response from Groq: {e}")

import json
import requests
from typing import List, Dict
from dataclasses import dataclass
import re

class JDAnalyzerError(Exception):
    """Custom exception for JD analyzer errors."""
    pass

@dataclass
class LLMConfig:
    provider: str
    model_name: str
    endpoint: str
    api_key: str
    temperature: float = 0.0
    max_tokens: int = 4096

def _clean_json_response(response_text: str) -> str:
    """Clean the LLM response to extract valid JSON."""
    # 1. Strip out any ``` or ```json fenced code blocks
    code_block = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', response_text)
    if code_block:
        response_text = code_block.group(1)
    # 2. Trim whitespace/newlines
    response_text = response_text.strip()
    # 3. Remove wrapping quotes if present
    if (response_text.startswith('"') and response_text.endswith('"')) or \
       (response_text.startswith("'") and response_text.endswith("'")):
        response_text = response_text[1:-1].strip()
    return response_text

def _parse_weights_response(response_text: str) -> Dict[str, float]:
    """Parse the LLM response into a dictionary of weights."""
    cleaned = _clean_json_response(response_text)
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as e:
        # no fallback to literal_eval—require valid JSON
        raise JDAnalyzerError(f"Invalid JSON response: {e}\nCleaned text: {cleaned}")

    # support both list-of-objects and single-object formats
    items = data if isinstance(data, list) else [data] if isinstance(data, dict) else None
    if items is None:
        raise JDAnalyzerError(f"Unexpected JSON structure: {type(data).__name__}")

    weights: Dict[str, float] = {}
    for i, obj in enumerate(items):
        if not isinstance(obj, dict):
            raise JDAnalyzerError(f"Item {i} is not an object: {repr(obj)}")

        # Find the keyword field (case-insensitive)
        key_field = next(
            (k for k in obj if k.strip().strip('"\'' ).lower() == 'keyword'),
            None
        )
        if key_field is None:
            raise JDAnalyzerError(f"Missing 'keyword' field in item {i}: keys={list(obj.keys())}")
        raw_key = obj[key_field]
        keyword = str(raw_key).strip()

        # Find the weight field
        wt_field = next(
            (k for k in obj if k.strip().strip('"\'' ).lower() == 'weight'),
            None
        )
        if wt_field is None:
            raise JDAnalyzerError(f"Missing 'weight' field in item {i}: keys={list(obj.keys())}")
        raw_wt = obj[wt_field]

        # Allow numeric strings or numbers
        if isinstance(raw_wt, str):
            try:
                weight = float(raw_wt.strip())
            except ValueError:
                raise JDAnalyzerError(f"Cannot parse weight '{raw_wt}' at item {i}")
        elif isinstance(raw_wt, (int, float)):
            weight = float(raw_wt)
        else:
            raise JDAnalyzerError(f"Invalid weight type {type(raw_wt).__name__} in item {i}")

        weights[keyword] = weight

    total = sum(weights.values())
    if total <= 0:
        raise JDAnalyzerError(f"Sum of weights must be positive, got {total:.4f}")

    # Normalize weights to sum to 1.0
    if abs(total - 1.0) > 0.01:  # Allow for small floating point differences
        normalized_weights = {k: v/total for k, v in weights.items()}
        print(f"Warning: Normalized weights from sum {total:.4f} to 1.0")
        return normalized_weights

    return weights

def generate_weights_from_jd(
    jd_text: str,
    keywords: List[str],
    prompt_path: str,
    llm_config: LLMConfig
) -> Dict[str, float]:
    """
    Generate keyword weights from a job description using LLM.
    """
    # Load the prompt template
    try:
        prompt_template = open(prompt_path, 'r', encoding='utf-8').read()
    except FileNotFoundError:
        raise JDAnalyzerError(f"Prompt not found at {prompt_path}")

    prompt = prompt_template.format(
        JOB_DESCRIPTION=jd_text,
        KEYWORDS=', '.join(keywords)
    )

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
        resp = requests.post(llm_config.endpoint, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        llm_response = resp.json()["choices"][0]["message"]["content"]
        return _parse_weights_response(llm_response)
    except JDAnalyzerError:
        # parsing or validation error—bubble up
        raise
    except requests.RequestException as e:
        raise JDAnalyzerError(f"API request failed: {e}")
    except Exception as e:
        raise JDAnalyzerError(f"Unexpected error: {e}")

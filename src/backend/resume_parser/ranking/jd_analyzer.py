import json
import re
import time
from typing import Dict
import requests
from requests.exceptions import RequestException

from src.backend.resume_parser.config_models import LLMConfig


class JDAnalyzerError(Exception):
    """Custom exception for JD analyzer errors."""
    pass

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
    """Parse the LLM response into a dictionary of skill weights."""
    try:
        # Clean and parse JSON
        cleaned_text = _clean_json_response(response_text)
        weights = json.loads(cleaned_text)
        
        if not isinstance(weights, dict):
            raise JDAnalyzerError("Response is not a dictionary")
            
        # Validate and normalize weights
        total = sum(weights.values())
        if total <= 0:
            raise JDAnalyzerError(f"Sum of weights must be positive, got {total:.4f}")
            
        # Normalize weights to sum to 1.0
        if abs(total - 1.0) > 0.01:  # Allow for small floating point differences
            weights = {k: v/total for k, v in weights.items()}
            print(f"Warning: Normalized weights from sum {total:.4f} to 1.0")
            
        return weights
        
    except json.JSONDecodeError as e:
        raise JDAnalyzerError(f"Invalid JSON response: {e}\nCleaned text: {cleaned_text}")
    except Exception as e:
        raise JDAnalyzerError(f"Error parsing weights: {e}")

def generate_weights_from_jd(
    jd_text: str,
    prompt_path: str,
    llm_config: LLMConfig,
    skills_list: str,
    max_retries: int = 3,
    initial_delay: float = 1.0
) -> Dict[str, float]:
    """
    Generate keyword weights from a job description using LLM.
    
    Args:
        jd_text: The job description text
        prompt_path: Path to the prompt template file
        llm_config: LLM configuration
        skills_list: List of skills to consider
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay between retries in seconds
        
    Returns:
        Dictionary of skill weights
    """
    # Load the prompt template
    try:
        prompt_template = open(prompt_path, 'r', encoding='utf-8').read()
    except FileNotFoundError:
        raise JDAnalyzerError(f"Prompt not found at {prompt_path}")

    # Use a safer string formatting approach
    prompt = prompt_template.replace('{JOB_DESCRIPTION}', jd_text)
    prompt = prompt.replace('{SKILLS_LIST}', skills_list)

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

    retry_count = 0
    delay = initial_delay

    while retry_count <= max_retries:
        try:
            resp = requests.post(llm_config.endpoint, headers=headers, json=payload, timeout=30)
            
            # If we get a rate limit error, retry with exponential backoff
            if resp.status_code == 429:
                if retry_count == max_retries:
                    raise JDAnalyzerError(f"Rate limit exceeded after {max_retries} retries")
                
                print(f"Rate limit hit, retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
                retry_count += 1
                continue
                
            resp.raise_for_status()
            llm_response = resp.json()["choices"][0]["message"]["content"]
            return _parse_weights_response(llm_response)
            
        except JDAnalyzerError:
            # parsing or validation error—bubble up
            raise
        except RequestException as e:
            if retry_count == max_retries:
                raise JDAnalyzerError(f"API request failed after {max_retries} retries: {e}")
            print(f"Request failed, retrying in {delay} seconds...")
            time.sleep(delay)
            delay *= 2  # Exponential backoff
            retry_count += 1
        except Exception as e:
            raise JDAnalyzerError(f"Unexpected error: {e}")

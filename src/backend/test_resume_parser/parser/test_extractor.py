import pytest
import json
from dataclasses import asdict
from unittest.mock import patch, MagicMock

from src.backend.resume_parser.parser.extractor import (
    extract_resume_json,
    extract_skill_entries,
    GroqAPIError,
    SkillEntry
)

class DummyLLM:
    provider = "test"
    model_name = "m"
    endpoint = "http://fake"
    api_key = "key"
    temperature = 0.0
    max_tokens = 10

PROMPT_CONTENT = "Parse this: {{resume_text}}"

def test_extract_resume_json_success(tmp_path):
    # write a fake prompt
    prompt_path = tmp_path / "prompt.txt"
    prompt_path.write_text(PROMPT_CONTENT)

    # fake requests.post
    fake_response = MagicMock()
    fake_response.raise_for_status.return_value = None
    # wrap JSON in fences to test stripping logic
    fake_response.json.return_value = {
        "choices": [{
            "message": {
                "content": "```json\n{\"foo\": \"bar\"}\n```"
            }
        }]
    }

    with patch("requests.post", return_value=fake_response) as mock_post:
        out = extract_resume_json("XYZ", str(prompt_path), DummyLLM)
        assert out == {"foo": "bar"}
        mock_post.assert_called_once()

def test_extract_resume_json_prompt_not_found():
    with pytest.raises(GroqAPIError) as exc:
        extract_resume_json("TXT", "no_such_file", DummyLLM)
    assert "Failed to read prompt" in str(exc.value)

def test_extract_skill_entries_minimal():
    # craft a minimal resume_json
    resume = {
        "personal_information": {
            "full_name": "Alice",
            "contact": {"email": "a@b.com"}
        },
        "professional_summary": "Sum",
        "education": [{"degree": "BSc", "end_date": "2020"}],
        "certifications": [{"name":"Cert"}],
        "projects": [{"title":"P"}],
        "languages": {"en":"fluent"},
        "awards": [],
        "interests": [],
        "references": [],
        "skills": {
            "Python": {"count": 2, "age": 0, "experience_years": 3.5},
            "BadSkill": "not-a-dict"
        }
    }
    entries = extract_skill_entries(resume)
    assert len(entries) == 1
    e = entries[0]
    assert isinstance(e, SkillEntry)
    d = asdict(e)
    assert d["candidate_name"] == "Alice"
    assert d["email"] == "a@b.com"
    assert d["skill"] == "Python"
    assert d["skill_count"] == 2
    assert d["skill_age"] == 0
    assert d["skill_experience_years"] == 3.5
    # highest_degree chosen by length
    assert d["highest_degree"] == "BSc"
    assert d["graduation_year"] == 2020

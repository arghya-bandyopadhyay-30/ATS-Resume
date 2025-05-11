import json
import re
from dataclasses import dataclass
from typing import Optional, List, Dict

import requests


class GroqAPIError(Exception):
    """Custom error for Groq-related failures."""


@dataclass
class SkillEntry:
    candidate_name: str
    email: str
    summary: str
    skill: str
    skill_count: Optional[int]
    skill_age: Optional[int]
    skill_experience_years: Optional[float]
    highest_degree: str
    graduation_year: Optional[int]
    certifications: str
    projects: str
    languages: str
    awards: str
    interests: str
    references: str
    role: Optional[str] = None  # ✅ NEW FIELD


def extract_resume_json(
    resume_text: str,
    prompt_path: str,
    llm_config
) -> Dict:
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
        content = response.json()["choices"][0]["message"]["content"].strip()

        if content.startswith('```'):
            lines = content.split('\n')[1:-1] if content.endswith('```') else content.split('\n')[1:]
            content = '\n'.join(lines).strip()

        return json.loads(content)
    except Exception as e:
        raise GroqAPIError(f"Failed to parse response from Groq: {e}")


def extract_skill_entries(resume_json: dict) -> List[SkillEntry]:
    personal_info = resume_json.get("personal_information", {})
    contact = personal_info.get("contact", {}) or {}

    name = personal_info.get("full_name", "")
    email = contact.get("email", "")
    summary = resume_json.get("professional_summary", "")

    # ✅ Extract role from summary
    role_match = re.search(
        r"\bserves\s+\S+\s+as\s+(an?\s+)?(?P<role>[\w\s\-]+?)([.,]| with| and| where| who|$)",
        summary,
        re.IGNORECASE
    )
    role = role_match.group("role").strip() if role_match else "N/A"

    education_list = resume_json.get("education", [])
    highest_degree = max((e.get("degree", "") for e in education_list), key=len, default="") if education_list else ""
    graduation_year = max(
        [int(e.get("end_date")) for e in education_list if str(e.get("end_date")).isdigit()],
        default=0
    )

    certifications = json.dumps(resume_json.get("certifications", []), ensure_ascii=False)
    projects = json.dumps(resume_json.get("projects", []), ensure_ascii=False)
    languages = json.dumps(resume_json.get("languages", {}), ensure_ascii=False)
    awards = json.dumps(resume_json.get("awards", []), ensure_ascii=False)
    interests = json.dumps(resume_json.get("interests", []), ensure_ascii=False)
    references = json.dumps(resume_json.get("references", []), ensure_ascii=False)

    skills = resume_json.get("skills", {})
    entries = []

    for skill, meta in skills.items():
        if not isinstance(meta, dict):
            continue

        entry = SkillEntry(
            candidate_name=name,
            email=email,
            summary=summary,
            skill=skill,
            skill_count=meta.get("count", ""),
            skill_age=meta.get("age", ""),
            skill_experience_years=meta.get("experience_years", ""),
            highest_degree=highest_degree,
            graduation_year=graduation_year,
            certifications=certifications,
            projects=projects,
            languages=languages,
            awards=awards,
            interests=interests,
            references=references,
            role=role
        )
        entries.append(entry)

    # ✅ If no skills were extracted, still include one fallback row with role
    if not entries:
        entries.append(SkillEntry(
            candidate_name=name,
            email=email,
            summary=summary,
            skill="N/A",
            skill_count=None,
            skill_age=None,
            skill_experience_years=None,
            highest_degree=highest_degree,
            graduation_year=graduation_year,
            certifications=certifications,
            projects=projects,
            languages=languages,
            awards=awards,
            interests=interests,
            references=references,
            role=role
        ))

    return entries

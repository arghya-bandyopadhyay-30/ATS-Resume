import unittest
from dataclasses import asdict
from pathlib import Path
from tempfile import TemporaryDirectory
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


class TestExtractor(unittest.TestCase):

    def setUp(self):
        self.prompt_content = "Parse this: {{resume_text}}"

    def test_extract_resume_json_success(self):
        with TemporaryDirectory() as tmpdir:
            prompt_path = Path(tmpdir) / "prompt.txt"
            prompt_path.write_text(self.prompt_content)

            fake_response = MagicMock()
            fake_response.raise_for_status.return_value = None
            fake_response.json.return_value = {
                "choices": [{
                    "message": {
                        "content": "```json\n{\"foo\": \"bar\"}\n```"
                    }
                }]
            }

            with patch("requests.post", return_value=fake_response) as mock_post:
                result = extract_resume_json("XYZ", str(prompt_path), DummyLLM)
                self.assertEqual(result, {"foo": "bar"})
                mock_post.assert_called_once()

    def test_extract_resume_json_prompt_not_found(self):
        with self.assertRaises(GroqAPIError) as ctx:
            extract_resume_json("TXT", "no_such_file.txt", DummyLLM)
        self.assertIn("Failed to read prompt", str(ctx.exception))

    def test_extract_skill_entries_minimal(self):
        resume = {
            "personal_information": {
                "full_name": "Alice",
                "contact": {"email": "a@b.com"}
            },
            "professional_summary": "Sum",
            "education": [{"degree": "BSc", "end_date": "2020"}],
            "certifications": [{"name": "Cert"}],
            "projects": [{"title": "P"}],
            "languages": {"en": "fluent"},
            "awards": [],
            "interests": [],
            "references": [],
            "skills": {
                "Python": {"count": 2, "age": 0, "experience_years": 3.5},
                "BadSkill": "not-a-dict"
            }
        }

        entries = extract_skill_entries(resume)
        self.assertEqual(len(entries), 1)

        entry = entries[0]
        self.assertIsInstance(entry, SkillEntry)
        data = asdict(entry)

        self.assertEqual(data["candidate_name"], "Alice")
        self.assertEqual(data["email"], "a@b.com")
        self.assertEqual(data["skill"], "Python")
        self.assertEqual(data["skill_count"], 2)
        self.assertEqual(data["skill_age"], 0)
        self.assertEqual(data["skill_experience_years"], 3.5)
        self.assertEqual(data["highest_degree"], "BSc")
        self.assertEqual(data["graduation_year"], 2020)


if __name__ == "__main__":
    unittest.main()

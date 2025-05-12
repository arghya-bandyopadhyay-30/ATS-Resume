import unittest
from unittest.mock import patch, mock_open, MagicMock
from src.backend.resume_parser.ranking.jd_analyzer import generate_weights_from_jd, JDAnalyzerError
from src.backend.resume_parser.config_models import LLMConfig

class TestJDAnalyzer(unittest.TestCase):

    def setUp(self):
        self.prompt_template = "Analyze JD: {JOB_DESCRIPTION}\nSkills: {SKILLS_LIST}"
        self.jd_text = "We are looking for a Python and ML engineer."
        self.skills_list = "Python,Machine Learning,Data Science"

        self.llm_config = LLMConfig(
            provider="OpenAI",
            model_name="gpt-3.5-turbo",
            api_key="fake-api-key",
            endpoint="https://fake-endpoint.com",
            temperature=0.3,
            max_tokens=500
        )

        self.mock_response_content = {
            "choices": [{
                "message": {
                    "content": '{ "Python": 0.5, "Machine Learning": 0.3, "Data Science": 0.2 }'
                }
            }]
        }

    @patch("builtins.open", new_callable=mock_open, read_data="Analyze JD: {JOB_DESCRIPTION}\nSkills: {SKILLS_LIST}")
    @patch("requests.post")
    def test_generate_weights_success(self, mock_post, mock_file):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = self.mock_response_content
        mock_post.return_value = mock_resp

        result = generate_weights_from_jd(
            jd_text=self.jd_text,
            prompt_path="fake_prompt_path.txt",
            llm_config=self.llm_config,
            skills_list=self.skills_list
        )

        expected = {
            "Python": 0.5,
            "Machine Learning": 0.3,
            "Data Science": 0.2
        }
        self.assertEqual(result, expected)

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_prompt_file_not_found(self, mock_file):
        with self.assertRaises(JDAnalyzerError) as ctx:
            generate_weights_from_jd(
                jd_text=self.jd_text,
                prompt_path="missing.txt",
                llm_config=self.llm_config,
                skills_list=self.skills_list
            )
        self.assertIn("Prompt not found", str(ctx.exception))

    @patch("builtins.open", new_callable=mock_open, read_data="Analyze JD: {JOB_DESCRIPTION}\nSkills: {SKILLS_LIST}")
    @patch("requests.post")
    def test_invalid_json_response(self, mock_post, mock_file):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "choices": [{
                "message": {
                    "content": 'not a json'
                }
            }]
        }
        mock_post.return_value = mock_resp

        with self.assertRaises(JDAnalyzerError) as ctx:
            generate_weights_from_jd(
                jd_text=self.jd_text,
                prompt_path="fake_prompt_path.txt",
                llm_config=self.llm_config,
                skills_list=self.skills_list
            )
        self.assertIn("Invalid JSON response", str(ctx.exception))

if __name__ == '__main__':
    unittest.main()

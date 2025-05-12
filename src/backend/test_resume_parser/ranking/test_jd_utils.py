import unittest
from unittest.mock import patch, mock_open, MagicMock
import io
from src.backend.resume_parser.config_models import LLMConfig, ResumeParserConfig
from src.backend.resume_parser.ranking.jd_utils import analyze_jd_text


class TestAnalyzeJDText(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open)
    @patch("src.backend.resume_parser.ranking.jd_utils.generate_weights_from_jd")
    def test_analyze_jd_text_success(self, mock_generate_weights, mock_file):
        # Mock resume CSV reader output
        resume_csv_content = (
            "candidate_name,skill,skill_experience_years,skill_count,skill_age\n"
            "Alice,Python,3,10,12\n"
            "Alice,Machine Learning,2,8,6\n"
        )
        mock_file.side_effect = [
            io.StringIO(resume_csv_content),                        # read CSV
            io.StringIO("prompt: use this JD and skills..."),       # read prompt
            MagicMock()                                             # write weights.json
        ]

        # Setup fake config and expected output
        llm_cfg = LLMConfig(
            provider="mock",
            model_name="gpt",
            api_key="test",
            endpoint="http://mock.llm",
            temperature=0.3,
            max_tokens=1000
        )
        config = ResumeParserConfig(data_folder=".", resume_extension=".pdf", llm=llm_cfg)

        expected_weights = {
            "python": 0.6,
            "machine learning": 0.4
        }
        mock_generate_weights.return_value = expected_weights

        # Call function
        weights = analyze_jd_text(
            jd_text="Looking for a Python ML developer",
            base_dir="/fake/dir",
            config=config,
            csv_output_path="/fake/dir/output/parsed_resume_skills.csv"
        )

        # Assert weights returned
        self.assertEqual(weights, expected_weights)
        mock_generate_weights.assert_called_once()

        # Verify skill list formatting passed to prompt
        passed_skills = mock_generate_weights.call_args[0][3]
        self.assertIn("- python", passed_skills)
        self.assertIn("- machine learning", passed_skills)

if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import patch, mock_open
import pandas as pd
import json
import io

from src.backend.resume_parser.ranking.scorer import build_candidate_profiles


class TestScoreCandidateProfiles(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open)
    @patch("pandas.read_csv")
    def test_build_candidate_profiles_with_matching_skills(self, mock_read_csv, mock_open_file):
        # Mock JD weights
        jd_weights = {
            "Python": 0.5,
            "Machine Learning": 0.5
        }
        mock_open_file.return_value.__enter__.return_value = io.StringIO(json.dumps(jd_weights))

        # Sample candidate skill data
        data = {
            'candidate_name': ['Alice', 'Alice'],
            'summary': ['Experienced in Python and ML'] * 2,
            'languages': ['Python, Java'] * 2,
            'certifications': ['ML Specialization'] * 2,
            'role': ['Data Scientist'] * 2,
            'skill': ['Python', 'Machine Learning'],
            'skill_experience_years': [3, 2],
            'skill_count': [10, 8],
            'skill_age': [12, 6]
        }

        df = pd.DataFrame(data)
        mock_read_csv.return_value = df

        # Call the function
        profiles = build_candidate_profiles('fake.csv', 'fake_weights.json')

        # Assertions
        self.assertEqual(len(profiles), 1)
        profile = profiles[0]
        self.assertEqual(profile['name'], 'Alice')
        self.assertIn('Python', profile)
        self.assertIn('Machine Learning', profile)

        # Validate score logic (approximate)
        python_score = (0.4 * 3) + (0.3 * 10) + (0.3 * (1 - min(12/24, 1)))
        ml_score = (0.4 * 2) + (0.3 * 8) + (0.3 * (1 - min(6/24, 1)))

        self.assertAlmostEqual(profile['Python'], python_score, places=2)
        self.assertAlmostEqual(profile['Machine Learning'], ml_score, places=2)

if __name__ == "__main__":
    unittest.main()

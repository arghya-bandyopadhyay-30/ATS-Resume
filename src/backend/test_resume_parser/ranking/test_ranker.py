import unittest
from unittest.mock import patch, MagicMock
import json
import io
import csv

from src.backend.resume_parser.ranking.ranker import rank_candidates

class TestRankCandidatesWithMock(unittest.TestCase):

    @patch("src.backend.resume_parser.ranking.ranker.open")
    @patch("src.backend.resume_parser.ranking.ranker.os.path.dirname")
    def test_rank_candidates_with_mocked_files(self, mock_dirname, mock_open_fn):
        # Mock base_dir to avoid real file system dependencies
        mock_dirname.return_value = "/fake/base/dir"

        # Candidate and JD weight mock data
        mock_candidate_profiles = [
            {"name": "Alice", "role": "Data Scientist", "Python": 0.9, "ML": 0.8},   # score = 0.86 → 86
            {"name": "Bob", "role": "ML Engineer", "Python": 0.6, "ML": 0.5},       # score = 0.56 → 56
            {"name": "Charlie", "role": "Analyst", "Python": 0.3, "ML": 0.2}        # score = 0.26 → 26
        ]
        mock_jd_weights = {"Python": 0.6, "ML": 0.4}

        # Simulated file reads
        profile_json = io.StringIO(json.dumps(mock_candidate_profiles))
        weights_json = io.StringIO(json.dumps(mock_jd_weights))

        # Simulated file write
        mock_csv_writer = MagicMock()
        mock_csv_writer.__enter__.return_value = mock_csv_writer
        mock_csv_writer.__exit__.return_value = None
        mock_csv_writer.write = MagicMock()

        def open_side_effect(file, mode='r', *args, **kwargs):
            if "candidate_profiles.json" in file:
                return profile_json
            elif "jd_weights.json" in file:
                return weights_json
            elif "final_ranking.csv" in file and 'w' in mode:
                return mock_csv_writer
            else:
                raise FileNotFoundError(file)

        mock_open_fn.side_effect = open_side_effect

        # Run the function
        rank_candidates()

        # Capture written CSV output
        written = "".join(call.args[0] for call in mock_csv_writer.write.call_args_list)
        reader = list(csv.DictReader(io.StringIO(written)))

        # Check result count and contents
        self.assertEqual(len(reader), 3)
        self.assertEqual(reader[0]['candidate_name'], 'Alice')
        self.assertEqual(reader[0]['recommendation_label'], 'Well-Suited for the Role')  # 86
        self.assertEqual(reader[1]['candidate_name'], 'Bob')
        self.assertEqual(reader[1]['recommendation_label'], 'May Require Further Evaluation')  # 56
        self.assertEqual(reader[2]['candidate_name'], 'Charlie')
        self.assertEqual(reader[2]['recommendation_label'], 'May Require Further Evaluation')  # 26

if __name__ == "__main__":
    unittest.main()

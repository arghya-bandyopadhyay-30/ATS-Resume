import unittest
from unittest.mock import patch, mock_open, MagicMock
from resume_parser.parser.writer import write_skill_entries_to_csv
from resume_parser.parser.extractor import SkillEntry

class TestWriteSkillEntriesToCsv(unittest.TestCase):
    @patch('resume_parser.parser.writer.open', new_callable=mock_open)
    @patch('resume_parser.parser.writer.csv.DictWriter')
    def test_write_skill_entries_to_csv_success(self, mock_dict_writer, mock_file):
        entry = SkillEntry(
            candidate_name='John', email='john@example.com', summary='summary', skill='Python',
            skill_count=1, skill_age=2, skill_experience_years=3.0, highest_degree='MSc',
            graduation_year=2022, certifications='[]', projects='[]', languages='{}',
            awards='[]', interests='[]', references='[]'
        )
        mock_writer = MagicMock()
        mock_dict_writer.return_value = mock_writer
        write_skill_entries_to_csv([entry], 'fake.csv')
        mock_dict_writer.assert_called_once()
        mock_writer.writeheader.assert_called_once()
        mock_writer.writerow.assert_called()

    @patch('resume_parser.parser.writer.open', new_callable=mock_open)
    @patch('resume_parser.parser.writer.csv.DictWriter')
    def test_write_skill_entries_to_csv_empty(self, mock_dict_writer, mock_file):
        with patch('builtins.print') as mock_print:
            write_skill_entries_to_csv([], 'fake.csv')
            mock_print.assert_called_with('[WARN] No skill entries to write.')
        mock_dict_writer.assert_not_called()

if __name__ == '__main__':
    unittest.main() 
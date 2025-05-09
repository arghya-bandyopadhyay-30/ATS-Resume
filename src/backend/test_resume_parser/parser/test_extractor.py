import unittest
from unittest.mock import patch, mock_open, MagicMock
from resume_parser.parser.extractor import extract_resume_json, extract_skill_entries, GroqAPIError, SkillEntry

class DummyConfig:
    api_key = 'key'
    model_name = 'model'
    endpoint = 'http://fake-endpoint'
    temperature = 0.0
    max_tokens = 10

class TestExtractResumeJson(unittest.TestCase):
    @patch('resume_parser.parser.extractor.open', new_callable=mock_open, read_data='prompt {{resume_text}}')
    @patch('resume_parser.parser.extractor.requests.post')
    def test_extract_resume_json_success(self, mock_post, mock_file):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            'choices': [{
                'message': {'content': '{"foo": "bar"}'}
            }]
        }
        mock_post.return_value = mock_response
        result = extract_resume_json('resume', 'prompt.txt', DummyConfig())
        self.assertEqual(result, {'foo': 'bar'})

    @patch('resume_parser.parser.extractor.open', side_effect=Exception('fail'))
    def test_extract_resume_json_file_error(self, mock_file):
        with self.assertRaises(GroqAPIError) as cm:
            extract_resume_json('resume', 'prompt.txt', DummyConfig())
        self.assertIn('Failed to read prompt', str(cm.exception))

    @patch('resume_parser.parser.extractor.open', new_callable=mock_open, read_data='prompt {{resume_text}}')
    @patch('resume_parser.parser.extractor.requests.post', side_effect=Exception('fail'))
    def test_extract_resume_json_network_error(self, mock_post, mock_file):
        with self.assertRaises(GroqAPIError) as cm:
            extract_resume_json('resume', 'prompt.txt', DummyConfig())
        self.assertIn('Failed to parse response from Groq', str(cm.exception))

    @patch('resume_parser.parser.extractor.open', new_callable=mock_open, read_data='prompt {{resume_text}}')
    @patch('resume_parser.parser.extractor.requests.post')
    def test_extract_resume_json_codeblock(self, mock_post, mock_file):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            'choices': [{
                'message': {'content': '```\n{"foo": "bar"}\n```'}
            }]
        }
        mock_post.return_value = mock_response
        result = extract_resume_json('resume', 'prompt.txt', DummyConfig())
        self.assertEqual(result, {'foo': 'bar'})

class TestExtractSkillEntries(unittest.TestCase):
    def test_extract_skill_entries_empty(self):
        self.assertEqual(extract_skill_entries({}), [])

    def test_extract_skill_entries_full(self):
        resume_json = {
            'personal_information': {
                'full_name': 'John',
                'contact': {'email': 'john@example.com'}
            },
            'professional_summary': 'summary',
            'education': [
                {'degree': 'BSc', 'end_date': '2020'},
                {'degree': 'MSc', 'end_date': '2022'}
            ],
            'certifications': ['cert1'],
            'projects': ['proj1'],
            'languages': {'en': 'English'},
            'awards': ['award1'],
            'interests': ['interest1'],
            'references': ['ref1'],
            'skills': {
                'Python': {'count': 3, 'age': 2, 'experience_years': 1.5},
                'Java': {'count': 1, 'age': 1, 'experience_years': 0.5}
            }
        }
        entries = extract_skill_entries(resume_json)
        self.assertEqual(len(entries), 2)
        self.assertTrue(all(isinstance(e, SkillEntry) for e in entries))
        self.assertEqual(entries[0].candidate_name, 'John')
        self.assertEqual(entries[0].email, 'john@example.com')
        self.assertEqual(entries[0].highest_degree, 'BSc')
        self.assertEqual(entries[0].graduation_year, 2022)

    def test_extract_skill_entries_skills_not_dict(self):
        resume_json = {
            'personal_information': {'full_name': 'John', 'contact': {'email': 'john@example.com'}},
            'skills': {'Python': 'notadict'}
        }
        entries = extract_skill_entries(resume_json)
        self.assertEqual(entries, [])

if __name__ == '__main__':
    unittest.main() 
import unittest
import csv
import os
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from src.backend.resume_parser.parser.writer import write_skill_entries_to_csv
from src.backend.resume_parser.parser.extractor import SkillEntry


def make_entry(name, skill, count, age, yrs):
    return SkillEntry(
        candidate_name=name,
        email=f"{name.lower()}@x.com",
        summary="S",
        skill=skill,
        skill_count=count,
        skill_age=age,
        skill_experience_years=yrs,
        highest_degree="BSc",
        graduation_year=2020,
        certifications="[]",
        projects="[]",
        languages="{}",
        awards="[]",
        interests="[]",
        references="[]"
    )


class TestSkillEntryWriter(unittest.TestCase):

    def test_write_skill_entries_success(self):
        entries = [
            make_entry("A", "python", 1, 0, 1.0),
            make_entry("B", "aws", 2, 12, 0.5)
        ]
        with TemporaryDirectory() as tmpdir:
            out_path = Path(tmpdir) / "out.csv"
            write_skill_entries_to_csv(entries, str(out_path))

            self.assertTrue(out_path.exists())

            with open(out_path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)

            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["candidate_name"], "A")
            self.assertEqual(rows[0]["skill"], "python")
            self.assertEqual(rows[1]["skill"], "aws")
            self.assertEqual(rows[1]["skill_experience_years"], "0.5")
            self.assertIn("skill_count", reader.fieldnames)

    @patch("sys.stdout", new_callable=StringIO)
    def test_write_empty_entries_logs_warning(self, mock_stdout):
        with TemporaryDirectory() as tmpdir:
            out_path = Path(tmpdir) / "empty.csv"
            write_skill_entries_to_csv([], str(out_path))

            output = mock_stdout.getvalue()
            self.assertIn("[WARN] No skill entries to write.", output)
            self.assertFalse(out_path.exists())


if __name__ == "__main__":
    unittest.main()

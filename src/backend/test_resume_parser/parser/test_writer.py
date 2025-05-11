import pytest
import csv
import os
from tempfile import NamedTemporaryFile
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

def test_write_skill_entries(tmp_path):
    entries = [
        make_entry("A", "python", 1, 0, 1.0),
        make_entry("B", "aws", 2, 12, 0.5)
    ]
    out = tmp_path / "out.csv"
    write_skill_entries_to_csv(entries, str(out))

    # Read back and verify
    with open(out, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert len(rows) == 2
    # Check columns
    assert set(reader.fieldnames) >= {"candidate_name", "skill", "skill_count", "skill_age", "skill_experience_years"}
    # Row values
    assert rows[0]["candidate_name"] == "A"
    assert rows[0]["skill"] == "python"
    assert rows[0]["skill_count"] == "1"
    assert rows[1]["skill"] == "aws"
    assert rows[1]["skill_experience_years"] == "0.5"

def test_write_empty_list(capfd, tmp_path):
    out = tmp_path / "empty.csv"
    write_skill_entries_to_csv([], str(out))
    captured = capfd.readouterr()
    # Should warn but not error
    assert "[WARN] No skill entries to write." in captured.out
    assert not out.exists()

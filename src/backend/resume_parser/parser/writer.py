import csv
from typing import List

from .extractor import SkillEntry


def write_skill_entries_to_csv(skill_entries: List[SkillEntry], output_path: str):
    if not skill_entries:
        print("[WARN] No skill entries to write.")
        return

    headers = [
        "candidate_name", "email", "summary", "skill", "skill_count", "skill_age", "skill_experience_years",
        "highest_degree", "graduation_year", "certifications", "projects", "languages",
        "awards", "interests", "references"
    ]

    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for entry in skill_entries:
            row = {field: (getattr(entry, field) if getattr(entry, field) is not None else "") for field in headers}
            writer.writerow(row)

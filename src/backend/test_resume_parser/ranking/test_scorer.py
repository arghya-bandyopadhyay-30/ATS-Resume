import pytest
import json
import pandas as pd
from src.backend.resume_parser.ranking.scorer import build_candidate_profiles

def test_build_candidate_profiles(tmp_path):
    # Create test CSV file
    csv_data = pd.DataFrame([
        {
            'candidate_name': 'Alice',
            'skill': 'python',
            'skill_count': 2,
            'skill_age': 0,
            'skill_experience_years': 1.5,
            'summary': '',
            'languages': 'en',
            'certifications': ''
        },
        {
            'candidate_name': 'Alice',
            'skill': 'aws',
            'skill_count': 1,
            'skill_age': 12,
            'skill_experience_years': 0.5,
            'summary': '',
            'languages': '',
            'certifications': ''
        },
        {
            'candidate_name': 'Bob',
            'skill': 'python',
            'skill_count': 1,
            'skill_age': 24,
            'skill_experience_years': 1.0,
            'summary': '',
            'languages': '',
            'certifications': ''
        },
        {
            'candidate_name': 'Bob',
            'skill': 'docker',
            'skill_count': 3,
            'skill_age': 6,
            'skill_experience_years': 0.2,
            'summary': '',
            'languages': '',
            'certifications': ''
        }
    ])
    csv_path = tmp_path / "resumes.csv"
    csv_data.to_csv(csv_path, index=False)

    # Create JD weights file
    jd_weights = {
        "python": 0.5,
        "aws": 0.3,
        "docker": 0.2
    }
    jd_weights_path = tmp_path / "jd_weights.json"
    with open(jd_weights_path, 'w') as f:
        json.dump(jd_weights, f)

    # Build profiles
    profiles = build_candidate_profiles(str(csv_path), str(jd_weights_path))

    # Verify results
    assert len(profiles) == 2

    # Find Alice's profile
    alice_profile = next(p for p in profiles if p['name'] == 'Alice')
    assert alice_profile['python'] == pytest.approx(1.5)  # 0.4*1.5 + 0.3*2 + 0.3*(1-0)
    assert alice_profile['aws'] == pytest.approx(0.65)    # 0.4*0.5 + 0.3*1 + 0.3*(1-0.5)
    assert alice_profile['docker'] == 0.0  # Not in Alice's skills

    # Find Bob's profile
    bob_profile = next(p for p in profiles if p['name'] == 'Bob')
    assert bob_profile['python'] == pytest.approx(0.7)    # 0.4*1.0 + 0.3*1 + 0.3*(1-1.0)
    assert bob_profile['docker'] == pytest.approx(1.205)   # 0.4*0.2 + 0.3*3 + 0.3*(1-0.25)
    assert bob_profile['aws'] == 0.0  # Not in Bob's skills 
import json
import csv
import os
import pytest

from src.backend.resume_parser.ranking.ranker import rank_candidates
import src.backend.resume_parser.ranking.ranker as ranker_module

def test_rank_candidates_writes_csv(tmp_path, monkeypatch):
    # 1) Create an "output" folder under tmp_path and write our test files there
    output_dir = tmp_path / "output"
    output_dir.mkdir()

    # 2) candidate_profiles.json
    profiles = [
        {"name": "A", "python": 1.0, "aws": 0.0},
        {"name": "B", "python": 0.5, "aws": 0.5}
    ]
    (output_dir / "candidate_profiles.json").write_text(json.dumps(profiles))

    # 3) jd_weights.json
    weights = {"python": 0.6, "aws": 0.4}
    (output_dir / "jd_weights.json").write_text(json.dumps(weights))

    # 4) Stub ranker_module.__file__ so that
    #    dirname(dirname(__file__)) == tmp_path
    fake_ranker = tmp_path / "fake" / "ranker.py"
    fake_ranker.parent.mkdir(parents=True)
    fake_ranker.write_text("")  # just create the file
    monkeypatch.setattr(ranker_module, "__file__", str(fake_ranker))

    # 5) Run the ranking
    rank_candidates()

    # 6) Verify final_ranking.csv
    final_csv = output_dir / "final_ranking.csv"
    assert final_csv.exists(), "Expected final_ranking.csv to be created"

    with open(final_csv, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        assert header == ["candidate_name", "score"]

        rows = list(reader)
        # A: 1.0*0.6 + 0*0.4 = 0.6
        # B: 0.5*0.6 + 0.5*0.4 = 0.5
        assert rows == [
            ["A", "0.6"],
            ["B", "0.5"]
        ]

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import csv
from pathlib import Path
import uvicorn
import os
import sys
import json
import yaml
from pydantic import BaseModel
from typing import Dict, List

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.backend.resume_parser.config_models import ResumeParserConfig, LLMConfig
from src.backend.resume_parser.main import main as process_resumes
from src.backend.resume_parser.ranking.jd_utils import analyze_jd_text
from src.backend.resume_parser.ranking.scorer import build_candidate_profiles
from src.backend.resume_parser.ranking.ranker import rank_candidates

def load_config() -> ResumeParserConfig:
    config_path = Path(__file__).parent / "resume_parser" / "config.yaml"
    try:
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f)
            
        llm_config = LLMConfig(**config_data['llm'])
        return ResumeParserConfig(
            data_folder=config_data['data_folder'],
            resume_extension=config_data['resume_extension'],
            llm=llm_config
        )
    except Exception as e:
        print(f"Error loading config: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to load configuration"
        )

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class JobDescription(BaseModel):
    jd_text: str

@app.get("/rankings")
async def get_rankings():
    csv_path = Path("resume_parser/output/final_ranking.csv")
    if not csv_path.exists():
        return []
        
    rankings = []
    try:
        with open(csv_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                rankings.append({
                    "candidate_name": row["candidate_name"],
                    "score": float(row["score"])
                })
    except Exception as e:
        print(f"Error reading rankings: {e}")
        return []
    
    return rankings

@app.post("/analyze-jd")
async def analyze_jd(jd: JobDescription):
    try:
        base_dir = Path(__file__).parent / "resume_parser"
        config = load_config()

        # Step 1: Ensure resumes have been processed already
        try:
            process_resumes(skip_jd_analysis=True)
        except Exception as e:
            print(f"Error processing resumes: {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to process resumes. Please ensure resume files are present in the data folder."
            )

        # Step 2: Analyze the JD
        csv_output_path = base_dir / "output" / "parsed_resume_skills.csv"
        if not csv_output_path.exists():
            raise HTTPException(
                status_code=500,
                detail="Resume processing failed. No skills data available."
            )

        try:
            weights = analyze_jd_text(jd.jd_text, str(base_dir), config, str(csv_output_path))
        except Exception as e:
            print(f"Error analyzing JD: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to analyze job description: {str(e)}"
            )

        # Step 3: Rebuild candidate profiles & rankings with updated weights
        try:
            candidate_profiles = build_candidate_profiles(
                str(csv_output_path),
                str(base_dir / "output" / "jd_weights.json")
            )

            profiles_path = base_dir / "output" / "candidate_profiles.json"
            with open(profiles_path, 'w', encoding='utf-8') as f:
                json.dump(candidate_profiles, f, indent=2, ensure_ascii=False)

            rank_candidates()

        except Exception as e:
            print(f"Error generating rankings: {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to update candidate rankings with new weights."
            )

        return {
            "message": "Job description analyzed and candidates ranked successfully",
            "weights": weights
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

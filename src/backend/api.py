from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import csv
from pathlib import Path
import uvicorn
import os
import sys
from pydantic import BaseModel
from typing import Dict, List

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.backend.resume_parser.config_models import ResumeParserConfig, LLMConfig
from src.backend.resume_parser.main import main as process_resumes
from src.backend.resume_parser.ranking.jd_utils import analyze_jd_text

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
        # Get the base directory and load config
        base_dir = Path(__file__).parent / "resume_parser"
        config = ResumeParserConfig(
            data_folder="data",
            resume_extension=".docx",
            llm=LLMConfig(
                provider="groq",
                model_name="gemma2-9b-it",
                endpoint="https://api.groq.com/openai/v1/chat/completions",
                api_key="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",
                temperature=0.0,
                max_tokens=4096
            )
        )
        
        # First, process resumes to ensure we have the CSV file
        try:
            # Process resumes without JD analysis
            process_resumes(skip_jd_analysis=True)
        except Exception as e:
            print(f"Error processing resumes: {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to process resumes. Please ensure resume files are present in the data folder."
            )
        
        # Path to the parsed resume skills CSV
        csv_output_path = base_dir / "output" / "parsed_resume_skills.csv"
        if not csv_output_path.exists():
            raise HTTPException(
                status_code=500,
                detail="Resume processing failed. No skills data available."
            )
        
        # Analyze the JD text and generate weights
        try:
            weights = analyze_jd_text(jd.jd_text, str(base_dir), config, str(csv_output_path))
        except Exception as e:
            print(f"Error analyzing JD: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to analyze job description: {str(e)}"
            )
        
        # Process resumes again with the new weights
        try:
            # This time we don't skip JD analysis since we have weights
            process_resumes(skip_jd_analysis=False)
        except Exception as e:
            print(f"Error processing resumes with new weights: {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to update rankings with new weights."
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
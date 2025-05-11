from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import csv
from pathlib import Path
import uvicorn


app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/rankings")
async def get_rankings():
    csv_path = Path("resume_parser/output/final_ranking.csv")
    rankings = []
    
    with open(csv_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            rankings.append({
                "candidate_name": row["candidate_name"],
                "score": float(row["score"])
            })
    
    return rankings

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 
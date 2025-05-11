import json
import csv
import os

def rank_candidates():
    # Get base directory (src/backend/resume_parser)
    base_dir = os.path.dirname(os.path.dirname(__file__))
    
    # Load candidate profiles
    profiles_path = os.path.join(base_dir, 'output', 'candidate_profiles.json')
    with open(profiles_path, 'r', encoding='utf-8') as f:
        profiles = json.load(f)
    
    # Load JD weights
    weights_path = os.path.join(base_dir, 'output', 'jd_weights.json')
    with open(weights_path, 'r', encoding='utf-8') as f:
        jd_weights = json.load(f)
    
    # Calculate scores for each candidate
    ranked_candidates = []
    for profile in profiles:
        name = profile.get('name', '<unknown>')
        score = sum(
            profile.get(skill, 0.0) * weight
            for skill, weight in jd_weights.items()
        )
        ranked_candidates.append((name, round(score, 4)))
    
    # Sort by descending score
    ranked_candidates.sort(key=lambda x: x[1], reverse=True)
    
    # Write to CSV
    output_path = os.path.join(base_dir, 'output', 'final_ranking.csv')
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['candidate_name', 'score'])
        writer.writerows(ranked_candidates)

if __name__ == '__main__':
    rank_candidates()


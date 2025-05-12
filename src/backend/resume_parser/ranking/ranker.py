import json
import csv
import os

def get_recommendation_label(score: int) -> str:
    """Get recommendation label based on candidate score."""
    if score >= 90:
        return "Highly Recommended"
    elif score >= 75:
        return "Well-Suited for the Role"
    elif score >= 60:
        return "Good Potential"
    else:
        return "May Require Further Evaluation"

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
        raw = sum(
            profile.get(skill, 0.0) * weight
            for skill, weight in jd_weights.items()
        )
        percent = round(raw * 100)
        ranked_candidates.append((name, percent))

    # Sort by descending score
    ranked_candidates.sort(key=lambda x: x[1], reverse=True)
    
    # Write to CSV with rank
    output_path = os.path.join(base_dir, 'output', 'final_ranking.csv')
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['rank', 'candidate_name', 'role', 'score', 'recommendation_label'])
        writer.writeheader()
        for rank, (name, score) in enumerate(ranked_candidates, start=1):
            matching_profile = next((p for p in profiles if p['name'] == name), {})
            writer.writerow({
                'rank': rank,
                'candidate_name': name,
                'role': matching_profile.get('role', 'Employer'),
                'score': score,
                'recommendation_label': get_recommendation_label(score)
            })

if __name__ == '__main__':
    rank_candidates()

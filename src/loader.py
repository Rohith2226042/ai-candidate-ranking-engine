import json
from pathlib import Path


def load_candidates(file_path):
    candidates = []
    invalid_rows = 0

    file_path = Path(file_path)

    if not file_path.exists():
        print(f"File not found: {file_path}")
        return []

    with open(file_path, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            try:
                candidate = json.loads(line.strip())
                candidates.append(candidate)
            except json.JSONDecodeError:
                invalid_rows += 1
                print(f"Invalid JSON at line {line_number}")

    print("\n===== DATA LOAD SUMMARY =====")
    print(f"Total candidates loaded: {len(candidates)}")
    print(f"Invalid rows skipped: {invalid_rows}")

    return candidates


def preview_candidates(candidates, limit=3):
    print("\n===== PREVIEW =====")

    for i, candidate in enumerate(candidates[:limit], start=1):
        profile = candidate.get("profile", {})
        print(f"\nCandidate {i}")
        print(f"ID: {candidate.get('candidate_id')}")
        print(f"Name: {profile.get('anonymized_name')}")
        print(f"Title: {profile.get('current_title')}")
        print(f"Experience: {profile.get('years_of_experience')} years")
        print(f"Location: {profile.get('location')}")


if __name__ == "__main__":
    file_path = "data/candidates.jsonl"

    candidates = load_candidates(file_path)
    preview_candidates(candidates)
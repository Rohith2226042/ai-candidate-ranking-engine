from src.loader import load_candidates
from src.parser import (
    extract_profile,
    extract_skills,
    extract_career_history,
    extract_redrob_signals
)

from src.refiner import refine_top_candidates

from src.feature_engine import (
    calculate_experience_score,
    calculate_skill_score,
    calculate_behavior_score,
    calculate_company_prestige
)

from src.semantic_ranker import (
    generate_candidate_text,
    calculate_batch_semantic_scores
)

from src.trap_detector import (
    calculate_trap_score,
    is_honeypot
)

from src.scorer import calculate_final_score
from src.exporter import export_top_candidates
from src.reasoning_generator import generate_reasoning


job_description = """
Senior AI / ML Engineer.
Architect and own LLM-powered AI solutions end-to-end.
Build RAG pipelines, fine-tune models, optimize inference,
manage GPU fleets, and scale systems for millions of users.
"""


# Load candidates
candidates = load_candidates("data/candidates.jsonl")

candidate_data = []
candidate_texts = []


# Prepare candidate text for semantic scoring
for candidate in candidates:
    profile = extract_profile(candidate)
    skills = extract_skills(candidate)
    career_history = extract_career_history(candidate)
    signals = extract_redrob_signals(candidate)

    candidate_text = generate_candidate_text(
        profile,
        skills,
        career_history
    )

    candidate_data.append({
        "profile": profile,
        "skills": skills,
        "career_history": career_history,
        "signals": signals
    })

    candidate_texts.append(candidate_text)


# Batch semantic scoring
print("\nGenerating semantic scores...")
semantic_scores = calculate_batch_semantic_scores(
    job_description,
    candidate_texts
)


ranked_candidates = []


# Final scoring loop
for idx, candidate_info in enumerate(candidate_data):
    profile = candidate_info["profile"]
    skills = candidate_info["skills"]
    career_history = candidate_info["career_history"]
    signals = candidate_info["signals"]

    # Hard honeypot filter
    if is_honeypot(profile, skills, career_history):
        continue

    experience_score = calculate_experience_score(
        profile["experience"]
    )

    skill_score = calculate_skill_score(skills)

    behavior_score = calculate_behavior_score(signals)

    prestige_score = calculate_company_prestige(
        profile,
        career_history
    )

    trap_score = calculate_trap_score(
        profile,
        skills,
        career_history
    )

    final_score = calculate_final_score(
        experience_score,
        skill_score,
        semantic_scores[idx],
        behavior_score,
        trap_score,
        prestige_score
    )

    ranked_candidates.append({
        "candidate_id": profile["candidate_id"],
        "name": profile["name"],
        "score": final_score,
        "profile": profile,
        "skills": skills,
        "career_history": career_history
    })


# Sort by score descending + tie-break by candidate_id
ranked_candidates.sort(
    key=lambda x: (-x["score"], x["candidate_id"])
)


# Refine top candidates
refined_candidates = refine_top_candidates(
    ranked_candidates
)


# Generate reasoning AFTER refinement
for candidate in refined_candidates:
    candidate["reasoning"] = generate_reasoning(
        candidate["profile"],
        candidate["skills"],
        candidate["career_history"]
    )


# Quick top 10 preview
print("\n===== TOP 10 CANDIDATES =====")

for rank, candidate in enumerate(refined_candidates[:10], start=1):
    print(
        rank,
        candidate["candidate_id"],
        candidate["name"],
        candidate["score"]
    )


# Export submission
export_top_candidates(refined_candidates)
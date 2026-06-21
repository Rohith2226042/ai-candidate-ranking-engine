from fastapi import FastAPI, UploadFile, File, Form
import json
import tempfile

from src.loader import load_candidates
from src.parser import (
    extract_profile,
    extract_skills,
    extract_career_history,
    extract_redrob_signals
)

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


app = FastAPI(
    title="AI Candidate Ranking Engine"
)


@app.post("/rank")
async def rank_candidates(
    job_description: str = Form(...),
    file: UploadFile = File(...)
):
    contents = await file.read()

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".jsonl"
    ) as temp_file:
        temp_file.write(contents)
        temp_path = temp_file.name

    candidates = load_candidates(temp_path)

    candidate_data = []
    candidate_texts = []

    for candidate in candidates:
        profile = extract_profile(candidate)
        skills = extract_skills(candidate)
        career_history = extract_career_history(candidate)
        signals = extract_redrob_signals(candidate)

        if is_honeypot(profile, skills, career_history):
            continue

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

    semantic_scores = calculate_batch_semantic_scores(
        job_description,
        candidate_texts
    )

    ranked_candidates = []

    for idx, candidate_info in enumerate(candidate_data):
        profile = candidate_info["profile"]
        skills = candidate_info["skills"]
        career_history = candidate_info["career_history"]
        signals = candidate_info["signals"]

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
            "score": final_score
        })

    ranked_candidates.sort(
        key=lambda x: (-x["score"], x["candidate_id"])
    )

    return {
        "top_candidates": ranked_candidates[:100]
    }
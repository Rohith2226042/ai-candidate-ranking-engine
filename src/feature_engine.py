import math


# -----------------------------
# Experience Score
# -----------------------------
def calculate_experience_score(years):
    if years is None:
        return 0

    if 5 <= years <= 9:
        return 10
    elif 3 <= years < 5:
        return 7
    elif 9 < years <= 12:
        return 8
    elif years < 3:
        return 3
    else:
        return 5


# -----------------------------
# Skill Score
# -----------------------------
REQUIRED_SKILLS = {
    "llm",
    "fine-tuning llms",
    "lora",
    "qlora",
    "prompt engineering",
    "hugging face transformers",

    "rag",
    "embeddings",
    "retrieval",
    "faiss",
    "weaviate",
    "pinecone",
    "milvus",
    "pgvector",
    "opensearch",

    "langchain",
    "haystack",
    "bentoml",

    "kubernetes",
    "docker",
    "mlflow",
    "kubeflow",

    "machine learning",
    "deep learning",
    "nlp",
    "recommendation systems"
}


def calculate_skill_score(skills):
    if not skills:
        return 0

    matched = 0

    for skill in skills:
        skill_name = skill["name"].lower()

        if skill_name in REQUIRED_SKILLS:
            matched += 1

    return min((matched / 8) * 10, 10)


# -----------------------------
# Skill Depth Score
# -----------------------------
PROFICIENCY_WEIGHTS = {
    "beginner": 1,
    "intermediate": 2,
    "advanced": 3,
    "expert": 4
}


def calculate_skill_depth(skills):
    total_depth = 0

    for skill in skills:
        proficiency = skill.get("proficiency", "beginner").lower()
        duration = skill.get("duration_months", 1)
        endorsements = skill.get("endorsements", 0)

        prof_weight = PROFICIENCY_WEIGHTS.get(proficiency, 1)

        depth = prof_weight * math.log(duration + 1) * (1 + endorsements / 50)

        total_depth += depth

    return round(total_depth, 2)


# -----------------------------
# Behavior Score
# -----------------------------
def calculate_behavior_score(signals):
    score = 0

    if signals.get("open_to_work"):
        score += 2

    score += signals.get("recruiter_response_rate", 0) * 3
    score += signals.get("interview_completion_rate", 0) * 3

    score += min(
        signals.get("saved_by_recruiters", 0),
        20
    ) * 0.15

    github_score = signals.get("github_activity_score", 0)
    score += github_score * 0.03

    completeness = signals.get("profile_completeness", 0)
    score += completeness * 0.02

    notice_days = signals.get("notice_period_days", 0)

    if notice_days > 90:
        score -= 1

    if not signals.get("last_active_date"):
        score -= 1

    return round(score, 2)

    PRESTIGE_COMPANIES = {
    "openai": 3,
    "anthropic": 3,
    "google": 3,
    "meta": 3,
    "amazon": 2,
    "microsoft": 2,
    "nvidia": 3,
    "hugging face": 2,
    "scale ai": 2,
    "databricks": 2,
    "snowflake": 2
}


def calculate_company_prestige(profile, career_history):
    prestige_score = 0

    # Current company
    current_company = (
        profile.get("current_company", "")
        .lower()
    )

    if current_company in PRESTIGE_COMPANIES:
        prestige_score += PRESTIGE_COMPANIES[current_company]

    # Past companies
    for job in career_history:
        company = job.get("company", "").lower()

        if company in PRESTIGE_COMPANIES:
            prestige_score += PRESTIGE_COMPANIES[company] * 0.5

    return round(prestige_score, 2)
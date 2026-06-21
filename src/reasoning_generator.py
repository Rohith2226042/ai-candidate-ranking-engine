def generate_reasoning(profile, skills, career_history):
    reasons = []

    skill_names = [skill["name"].lower() for skill in skills]

    # AI skills
    important_ai_skills = [
        "lora",
        "qlora",
        "fine-tuning llms",
        "faiss",
        "weaviate",
        "pinecone",
        "milvus",
        "embeddings",
        "langchain"
    ]

    matched_skills = [
        skill for skill in important_ai_skills
        if skill in skill_names
    ]

    if matched_skills:
        reasons.append(
            f"Strong AI stack: {', '.join(matched_skills[:4])}"
        )

    # Experience
    years = profile.get("experience", 0)
    if years >= 5:
        reasons.append(
            f"{years} years of relevant experience"
        )

    # Production signals
    for job in career_history:
        description = job.get("description", "").lower()

        if "production" in description:
            reasons.append("Production ML deployment experience")
            break

        if "retrieval" in description:
            reasons.append("Built retrieval/ranking systems")
            break

        if "fine-tuned" in description:
            reasons.append("Hands-on LLM fine-tuning")
            break

    if not reasons:
        reasons.append("Moderate technical fit")

    return " | ".join(reasons[:3])
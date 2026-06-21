from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_candidate_text(profile, skills, career_history):
    skill_names = [skill["name"] for skill in skills]
    job_descriptions = [job["description"] for job in career_history]

    combined_text = " ".join([
        profile.get("headline", ""),
        profile.get("summary", ""),
        " ".join(skill_names),
        " ".join(job_descriptions)
    ])

    return combined_text


def calculate_batch_semantic_scores(job_description, candidate_texts):
    jd_embedding = model.encode([job_description])

    candidate_embeddings = model.encode(
        candidate_texts,
        batch_size=64,
        show_progress_bar=True
    )

    similarities = cosine_similarity(
        jd_embedding,
        candidate_embeddings
    )[0]

    scores = [round(float(sim) * 10, 2) for sim in similarities]

    return scores
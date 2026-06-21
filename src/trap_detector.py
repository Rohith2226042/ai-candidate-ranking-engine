def detect_fake_ai_curiosity(summary):
    suspicious_phrases = [
        "curious about ai",
        "experimented with chatgpt",
        "building competence",
        "learning ai",
        "exploring ai"
    ]

    summary = summary.lower()

    for phrase in suspicious_phrases:
        if phrase in summary:
            return True

    return False


def detect_title_description_mismatch(career_history):
    mismatch_count = 0

    for job in career_history:
        title = job.get("title", "").lower()
        description = job.get("description", "").lower()

        if title and description:
            if title not in description:
                mismatch_count += 1

    return mismatch_count


def detect_random_skill_soup(skills):
    unrelated_clusters = [
        {"accounting", "tailwind", "seo"},
        {"photoshop", "kubernetes", "marketing"},
        {"excel", "react", "feature engineering"}
    ]

    skill_names = {
        skill.get("name", "").lower()
        for skill in skills
    }

    for cluster in unrelated_clusters:
        if len(skill_names.intersection(cluster)) >= 2:
            return True

    return False


def detect_experience_authenticity(profile, career_history):
    total_career_months = sum(
        job.get("duration_months", 0)
        for job in career_history
    )

    profile_years = profile.get("experience", 0)
    profile_months = profile_years * 12

    # If career history exceeds profile by too much
    if total_career_months > profile_months + 24:
        return False

    return True


def calculate_trap_score(profile, skills, career_history):
    trap_score = 0

    if detect_fake_ai_curiosity(profile.get("summary", "")):
        trap_score += 3

    trap_score += detect_title_description_mismatch(career_history)

    if detect_random_skill_soup(skills):
        trap_score += 2

    if not detect_experience_authenticity(profile, career_history):
        trap_score += 3

    return trap_score


def is_honeypot(profile, skills, career_history):
    trap_score = calculate_trap_score(
        profile,
        skills,
        career_history
    )

    # Hard reject conditions
    if trap_score >= 6:
        return True

    if profile.get("experience", 0) < 2:
        return True

    if len(skills) < 3:
        return True

    if not detect_experience_authenticity(
        profile,
        career_history
    ):
        return True

    return False
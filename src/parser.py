def extract_profile(candidate):
    profile = candidate.get("profile", {})

    return {
        "candidate_id": candidate.get("candidate_id"),
        "name": profile.get("anonymized_name"),
        "headline": profile.get("headline"),
        "summary": profile.get("summary"),
        "location": profile.get("location"),
        "country": profile.get("country"),
        "experience": profile.get("years_of_experience"),
        "current_title": profile.get("current_title"),
        "current_company": profile.get("current_company"),
        "industry": profile.get("current_industry"),
    }


def extract_skills(candidate):
    skills = candidate.get("skills", [])

    return [
        {
            "name": skill.get("name"),
            "proficiency": skill.get("proficiency"),
            "endorsements": skill.get("endorsements"),
            "duration_months": skill.get("duration_months")
        }
        for skill in skills
    ]


def extract_career_history(candidate):
    history = candidate.get("career_history", [])

    return [
        {
            "company": job.get("company"),
            "title": job.get("title"),
            "duration_months": job.get("duration_months"),
            "description": job.get("description"),
            "industry": job.get("industry")
        }
        for job in history
    ]


def extract_redrob_signals(candidate):
    signals = candidate.get("redrob_signals", {})

    return {
        "profile_completeness": signals.get("profile_completeness_score"),
        "recruiter_response_rate": signals.get("recruiter_response_rate"),
        "github_activity_score": signals.get("github_activity_score"),
        "interview_completion_rate": signals.get("interview_completion_rate"),
        "saved_by_recruiters": signals.get("saved_by_recruiters_30d"),
        "open_to_work": signals.get("open_to_work_flag"),
        "notice_period_days": signals.get("notice_period_days"),
        "last_active_date": signals.get("last_active_date")
    }
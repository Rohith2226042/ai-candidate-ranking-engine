def refine_top_candidates(ranked_candidates, top_n=100):
    refined = []
    seen_companies = {}
    seen_titles = {}

    for candidate in ranked_candidates:
        profile = candidate.get("profile", {})

        company = profile.get("current_company", "Unknown")
        title = profile.get("current_title", "Unknown")

        # Limit same company repetition
        if seen_companies.get(company, 0) >= 5:
            continue

        # Limit same title repetition
        if seen_titles.get(title, 0) >= 10:
            continue

        refined.append(candidate)

        seen_companies[company] = seen_companies.get(company, 0) + 1
        seen_titles[title] = seen_titles.get(title, 0) + 1

        if len(refined) >= top_n:
            break

    return refined
def calculate_final_score(
    experience_score,
    skill_score,
    semantic_score,
    behavior_score,
    trap_score
):
    # Dynamic weights
    semantic_weight = 0.35
    skill_weight = 0.25
    experience_weight = 0.20
    behavior_weight = 0.20

    # If semantic fit is low, reduce trust
    if semantic_score < 4:
        semantic_weight = 0.25
        skill_weight = 0.30

    # If experience is weak, reduce experience weight
    if experience_score < 5:
        experience_weight = 0.10
        semantic_weight += 0.05

    final_score = (
        (experience_score * experience_weight) +
        (skill_score * skill_weight) +
        (semantic_score * semantic_weight) +
        (behavior_score * behavior_weight)
    )

    # Trap penalty
    final_score -= (trap_score * 0.15)

    return round(final_score, 2)
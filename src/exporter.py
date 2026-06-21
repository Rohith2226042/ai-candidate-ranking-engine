import csv


def export_top_candidates(
    ranked_candidates,
    output_file="outputs/submission.csv"
):
    top_100 = ranked_candidates[:100]

    seen_candidate_ids = set()

    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:
        writer = csv.writer(
            file,
            quoting=csv.QUOTE_ALL
        )

        # Exact validator format
        writer.writerow([
            "candidate_id",
            "rank",
            "score",
            "reasoning"
        ])

        for rank, candidate in enumerate(top_100, start=1):
            candidate_id = candidate["candidate_id"]

            if candidate_id in seen_candidate_ids:
                continue

            reasoning = candidate.get(
                "reasoning",
                "Strong technical fit"
            )

            # Safety trim
            reasoning = reasoning[:200]

            writer.writerow([
                candidate_id,
                rank,
                round(candidate["score"], 2),
                reasoning
            ])

            seen_candidate_ids.add(candidate_id)

    print(
        f"\nSubmission file created successfully: {output_file}"
    )
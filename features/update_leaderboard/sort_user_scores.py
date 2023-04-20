def sort_user_scores(user_scores): # overall
    overall_scores = {}
    for user_id, scores in user_scores.items():
        overall_correct = sum([s["correct"] for s in scores.values()])
        overall_incorrect = sum([s["incorrect"] for s in scores.values()])
        overall_scores[user_id] = {
            "correct": overall_correct,
            "incorrect": overall_incorrect
        }

    sorted_user_scores = sorted(overall_scores.items(), key=lambda x: (
        x[1]["correct"], x[1]["incorrect"]), reverse=True)

    return sorted_user_scores

def create_user_scores_by_quiz_data(user_scores, question_dict_mapping):
    user_scores_by_quiz_data = {p: {} for p in question_dict_mapping}
    for user_id, scores in user_scores.items():
        for prefix, score in scores.items():
            user_scores_by_quiz_data[prefix][user_id] = {
                "correct": score["correct"], "incorrect": score["incorrect"]}
    return user_scores_by_quiz_data

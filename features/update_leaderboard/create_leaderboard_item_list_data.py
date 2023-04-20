async def create_leaderboard_item_list_data(question_dict_mapping, user_scores):
    prefix_scores = {p: {} for p in question_dict_mapping}
    for user_id, scores in user_scores.items():
        for prefix, score in scores.items():
            prefix_scores[prefix][user_id] = {
                "correct": score["correct"], "incorrect": score["incorrect"]}

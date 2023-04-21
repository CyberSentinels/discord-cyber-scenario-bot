def create_quiz_leaderboard_str(sorted_users_by_quiz, member_dict):
    prefix_leaderboard_desc = ""
    rank = 1
    for user_id, user_scores_for_quiz in sorted_users_by_quiz:
        member = member_dict.get(int(user_id))
        if member is not None:
            username = member.display_name
        else:
            username = f"Unknown User ({user_id})"
        correct = user_scores_for_quiz["correct"]
        incorrect = user_scores_for_quiz["incorrect"]
        prefix_leaderboard_desc += f"{rank}. **{username}**: {correct} correct, {incorrect} incorrect\n"
        rank += 1
        if rank > 5:
            break
    return prefix_leaderboard_desc

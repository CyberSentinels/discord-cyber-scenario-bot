def create_overall_leaderboard_str(sorted_user_scores, member_dict):
    overall_leaderboard_desc = ""
    rank = 1
    for user_id, scores in sorted_user_scores:
        member = member_dict.get(user_id)
        if member is not None:
            username = member.display_name
        else:
            username = f"Unknown User ({user_id})"
        correct = scores["correct"]
        incorrect = scores["incorrect"]
        overall_leaderboard_desc += f"{rank}. **{username}**: {correct} correct, {incorrect} incorrect\n"
        rank += 1
        if rank > 5:
            break
    return overall_leaderboard_desc

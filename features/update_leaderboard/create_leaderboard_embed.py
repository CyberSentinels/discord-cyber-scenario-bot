import base64
import json
from discord import Embed
from features.update_leaderboard.create_leaderboard_item_list_data import create_leaderboard_item_list_data

from features.update_leaderboard.create_overall_leaderboard_str import create_overall_leaderboard_str
from features.update_leaderboard.create_quiz_leaderboard_str import create_quiz_leaderboard_str
from features.update_leaderboard.sort_user_scores import sort_user_scores


def create_leaderboard_embed(user_scores, question_dict_mapping, member_dict):
    leaderboard_embed = Embed(
        title="Quiz Commands Leaderboard", color=0x006400)

    # leaderboard embed: overall
    sorted_overall_user_scores = sort_user_scores(user_scores)
    overall_leaderboard_str = create_overall_leaderboard_str(
        sorted_overall_user_scores, member_dict)
    leaderboard_embed.add_field(
        name="Overall", value=overall_leaderboard_str, inline=False)

    # leaderboard embed: each quiz leaderboard
    user_scores_by_quiz = create_leaderboard_item_list_data(
        question_dict_mapping, user_scores)
    for prefix, scores in user_scores_by_quiz.items():
        sorted_users_by_quiz = sorted(scores.items(), key=lambda x: (
            x[1]["correct"], x[1]["incorrect"]), reverse=True)
        prefix_leaderboard_desc = create_quiz_leaderboard_str(
            sorted_users_by_quiz, member_dict)
        leaderboard_embed.add_field(
            name=prefix.upper(), value=prefix_leaderboard_desc, inline=False)

    # leaderboard embed: base64 encoded user_scores
    user_scores_json = json.dumps(user_scores)
    user_scores_base64 = base64.b64encode(user_scores_json.encode()).decode()
    leaderboard_embed.add_field(
        name="Parity", value=f"```{user_scores_base64}```", inline=False)

    # leaderboard embed: footer
    leaderboard_embed.set_footer(
        text="Note: The leaderboard is updated once per hour. \n To learn more about the quiz commands, run `/commands` in #bot-commands")

    return leaderboard_embed

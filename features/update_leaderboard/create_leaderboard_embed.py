import base64
import json
from discord import Embed

from features.update_leaderboard.create_overall_leaderboard_str import create_overall_leaderboard_str
from features.update_leaderboard.create_user_scores_by_quiz_data import create_user_scores_by_quiz_data
from features.update_leaderboard.create_quiz_leaderboard_str import create_quiz_leaderboard_str
from features.update_leaderboard.sort_overall_user_scores import sort_overall_user_scores


async def create_leaderboard_embed(user_scores, question_dict_mapping, member_dict):
    leaderboard = Embed(
        title="Quiz Commands Leaderboard", color=0x006400)

    # leaderboard embed: overall
    sorted_overall_user_scores = sort_overall_user_scores(user_scores)
    overall_leaderboard_str = create_overall_leaderboard_str(
        sorted_overall_user_scores, member_dict)
    leaderboard.add_field(
        name="Overall", value=overall_leaderboard_str, inline=False)

    # leaderboard embed: each quiz leaderboard
    user_scores_by_quiz = create_user_scores_by_quiz_data(
        user_scores, question_dict_mapping)
    for prefix, scores in user_scores_by_quiz.items():
        sorted_users_by_quiz = sorted(scores.items(), key=lambda x: (
            x[1]["correct"], x[1]["incorrect"]), reverse=True)
        prefix_leaderboard_desc = create_quiz_leaderboard_str(
            sorted_users_by_quiz, member_dict)
        leaderboard.add_field(
            name=prefix.upper(), value=prefix_leaderboard_desc, inline=False)

    # leaderboard embed: footer
    leaderboard.set_footer(
        text="Note: The leaderboard is updated once per hour. \n To learn more about the quiz commands, run `/commands` in #bot-commands")

    return leaderboard

async def create_leaderboard_persistance_embed(user_scores):
    # leaderboard embed: base64 encoded user_scores
    leaderboard_persistence = Embed(
        title="Leaderboard Persistance", color=0x006400)
    user_scores_json = json.dumps(user_scores)
    user_scores_base64 = base64.b64encode(user_scores_json.encode()).decode()

    encoded_score_chunks = split_by_1000_chars(user_scores_base64)

    for i, chunk in enumerate(encoded_score_chunks):
        leaderboard_persistence.add_field(
            name="chunk:" + str(i), value=f"```{chunk}```", inline=False)
        
    return leaderboard_persistence


def split_by_1000_chars(base64_user_scores):
    chunks = []
    chunks_len = 0
    while chunks_len != len(base64_user_scores):
        new_chunk = base64_user_scores[0:1000]
        chunks.append(new_chunk)
        chunks_len += len(new_chunk)
    return chunks

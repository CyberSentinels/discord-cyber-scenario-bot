from discord import Embed
import os

from features.update_leaderboard.create_overall_leaderboard_str import (
    create_overall_leaderboard_str,
)
from features.update_leaderboard.create_user_scores_by_quiz_data import (
    create_user_scores_by_quiz_data,
)
from features.update_leaderboard.create_quiz_leaderboard_str import (
    create_quiz_leaderboard_str,
)
from features.update_leaderboard.sort_overall_user_scores import (
    sort_overall_user_scores,
)
from services.create_leaderboard_persistance_embed_field_list import (
    create_leaderboard_persistance_embed_field_list,
)


async def create_leaderboard_embed(user_scores, question_dict_mapping, member_dict):
    leaderboard = Embed(title="Quiz Commands Leaderboard", color=0x006400)

    # leaderboard embed: overall
    sorted_overall_user_scores = sort_overall_user_scores(user_scores)
    overall_leaderboard_str = create_overall_leaderboard_str(
        sorted_overall_user_scores, member_dict
    )
    leaderboard.add_field(name="Overall", value=overall_leaderboard_str, inline=False)

    # leaderboard embed: each quiz leaderboard
    user_scores_by_quiz = create_user_scores_by_quiz_data(
        user_scores, question_dict_mapping
    )
    for prefix, scores in user_scores_by_quiz.items():
        sorted_users_by_quiz = sorted(
            scores.items(),
            key=lambda x: (x[1]["correct"], x[1]["incorrect"]),
            reverse=True,
        )
        prefix_leaderboard_desc = create_quiz_leaderboard_str(
            sorted_users_by_quiz, member_dict
        )
        leaderboard.add_field(
            name=prefix.upper(), value=prefix_leaderboard_desc, inline=False
        )

    # leaderboard embed: footer
    leaderboard.set_footer(
        text="Note: The leaderboard is updated once per hour. \n To learn more about the quiz commands, run `/commands` in #bot-commands"
    )

    return leaderboard

async def create_leaderboard_persistance_embed(user_scores):
    try:
        leaderboard_messages = []
        field_list = await create_leaderboard_persistance_embed_field_list(user_scores)
        for index, field in enumerate(field_list):
            title = f"Leaderboard Persistence {index}"
            message = Embed(title=title, color=0x006400)
            message.add_field(
                name=field["name"], value=field["value"], inline=False
            )
        return leaderboard_messages
    except Exception as e:
        # Handle any errors that occur during the process
        raise ValueError(f"Error creating leaderboard persistence embed: {str(e)}")

def get_encoded_user_scores_from_embeds(leaderboard_message):
    if leaderboard_message is not None:
        for embed in leaderboard_message.embeds:
            for field in embed.fields:
                if field.name == "Parity":
                    return field.value.strip('```')

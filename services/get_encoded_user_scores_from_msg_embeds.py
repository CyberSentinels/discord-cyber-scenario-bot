def get_encoded_user_scores_from_msg_embeds(leaderboard_message):
    chunks = []
    if leaderboard_message is not None:
        for embed in leaderboard_message.embeds:
            for field in embed.fields:
                if field.name[0:6] == "chunk:":
                    chunks.append(field.value.strip("```"))
    chunks_str = "".join(chunks)
    return chunks_str


def test_get_encoded_user_scores_from_embeds():
    from services.__fixtures__.mocks import (
        MOCK_DISCORD_LEADERBOARD_MESSAGE,
        MOCK_ENCODED_STR,
    )

    result = get_encoded_user_scores_from_msg_embeds(MOCK_DISCORD_LEADERBOARD_MESSAGE)
    assert result == MOCK_ENCODED_STR

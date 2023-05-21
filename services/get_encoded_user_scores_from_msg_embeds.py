def get_encoded_user_scores_from_msg_embeds(leaderboard_messages):
    chunks = []
    try:
        for message in leaderboard_messages:
            for embed in message.embeds:
                for field in embed.fields:
                    if field.name.startswith("chunk:"):
                        chunks.append(field.value.strip("```"))
    except Exception as e:
        raise ValueError(f"Error occurred while processing leaderboard messages: {str(e)}")
    chunks_str = "".join(chunks)
    return chunks_str


def test_get_encoded_user_scores_from_embeds():
    from services.__fixtures__.mocks import (
        MOCK_DISCORD_LEADERBOARD_MESSAGE,
        MOCK_ENCODED_STR,
    )

    result = get_encoded_user_scores_from_msg_embeds(MOCK_DISCORD_LEADERBOARD_MESSAGE)
    assert result == MOCK_ENCODED_STR

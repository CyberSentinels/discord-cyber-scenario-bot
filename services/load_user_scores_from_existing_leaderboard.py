from services.get_encoded_user_scores_from_msg_embeds import (
    get_encoded_user_scores_from_msg_embeds,
)
from services.try_decode_base64_json import try_decode_base64_json

async def load_user_scores_from_existing_leaderboard(leaderboard_channel, client):
    leaderboard_messages = []
    try:
        async for message in leaderboard_channel.history():
            if message.author == client.user:
                leaderboard_messages.append(message)
    except Exception as e:
        raise ValueError(f"Error occurred while fetching leaderboard messages: {str(e)}")
    if not leaderboard_messages:
        raise ValueError("ERROR: no leaderboard messages found in leaderboard channel")
    try:
        user_scores_base64 = get_encoded_user_scores_from_msg_embeds(leaderboard_messages)
    except Exception as e:
        raise ValueError(f"Error occurred while processing leaderboard messages: {str(e)}")
    try:
        return try_decode_base64_json(user_scores_base64)
    except Exception as e:
        raise ValueError(f"Error occurred while decoding user scores: {str(e)}")

async def test_load_user_scores_from_existing_leaderboard():
    from services.__fixtures__.mocks import (
        MOCK_DISCORD_CHANNEL,
        MOCK_DISCORD_CLIENT,
        MOCK_USER_SCORES
    )

    user_scores = await load_user_scores_from_existing_leaderboard(
        MOCK_DISCORD_CHANNEL, MOCK_DISCORD_CLIENT
    )

    assert user_scores == MOCK_USER_SCORES

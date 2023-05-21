from services.get_encoded_user_scores_from_msg_embeds import (
    get_encoded_user_scores_from_msg_embeds,
)
from services.try_decode_base64_json import try_decode_base64_json


async def load_user_scores_from_existing_leaderboard(leaderboard_channel, client):
    leaderboard_message = None
    async for message in leaderboard_channel.history():
        if message.author == client.user:
            leaderboard_message = message
            break
    if leaderboard_message is None:
        raise ValueError("ERROR: no leaderboard message found in leaderboard channel")
    user_scores_base64 = get_encoded_user_scores_from_msg_embeds(leaderboard_message)
    return try_decode_base64_json(user_scores_base64)


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

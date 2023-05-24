from services.get_encoded_user_scores_from_msg_embeds import (
    get_encoded_user_scores_from_msg_embeds,
)
from services.try_decode_base64_json import try_decode_base64_json

async def load_user_scores_from_existing_leaderboard(leaderboard_channel, client):
    leaderboard_messages = []
    user_scores_base64_list = []
    async for message in leaderboard_channel.history():
        if message.author == client.user:
            leaderboard_messages.append(message)
    for leaderboard_message in leaderboard_messages:
        user_scores_base64 = get_encoded_user_scores_from_msg_embeds(leaderboard_message)
        user_scores_base64_list.append(user_scores_base64)
    combined_base64 = "".join(user_scores_base64_list)
    decoded_user_scores = try_decode_base64_json(combined_base64)
    if not decoded_user_scores:
        raise ValueError("ERROR: no leaderboard message found in leaderboard channel")
    return decoded_user_scores

async def test_load_user_scores_from_existing_leaderboard():
    from services.__fixtures__.mocks import (
        MOCK_DISCORD_CHANNEL,
        MOCK_DISCORD_CLIENT,
        MOCK_USER_SCORES,
    )

    user_scores = await load_user_scores_from_existing_leaderboard(
        MOCK_DISCORD_CHANNEL, MOCK_DISCORD_CLIENT
    )

    assert user_scores == MOCK_USER_SCORES

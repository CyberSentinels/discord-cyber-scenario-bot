import base64
import json

from services.attribute_dict import AttributeDict


async def load_user_scores_from_existing_leaderboard(leaderboard_channel, client):
    user_scores = {}  # default
    leaderboard_message = None
    async for message in leaderboard_channel.history():
        if message.author == client.user:
            leaderboard_message = message
            break
    user_scores_base64 = get_encoded_user_scores_from_embeds(leaderboard_message)
    try:
        user_scores_json = base64.b64decode(user_scores_base64.encode()).decode()
        user_scores = json.loads(user_scores_json)
    except Exception as e:
        print(f"Error decoding base64 user_scores: {e}")
    return user_scores


def get_encoded_user_scores_from_embeds(leaderboard_message):
    chunks = []
    if leaderboard_message is not None:
        for embed in leaderboard_message.embeds:
            for field in embed.fields:
                if field.name[0:6] == "chunk:":
                    chunks.append(field.value.strip("```"))
    chunks_str = "".join(chunks)
    return chunks_str


def test_get_encoded_user_scores_from_embeds():
    MOCK_ENCODED_STR_CHUNKS = [
        "eyIxMDE1MjQ5NzE1MTExMTQ5NTc4IjogeyJjaXNzcCI6IHsiY29ycmVjdCI6IDAsICJpbmNvcnJlY3QiOiAwfSwgImNlaCI6IHsiY29ycmVjdCI6IDAsICJpbmNvcnJlY3QiOiAwfSwgImNjbmEiOiB7ImNvcnJlY3QiOiAwLCAiaW5jb3JyZWN0IjogMH0sICJhcGx1cyI6IHsiY29ycmVjdCI6IDAsICJpbmNvcnJlY3QiOiAx",
        "fSwgIm5ldHBsdXMiOiB7ImNvcnJlY3QiOiAwLCAiaW5jb3JyZWN0IjogMH0sICJsaW51eHBsdXMiOiB7ImNvcnJlY3QiOiAwLCAiaW5jb3JyZWN0IjogMH0sICJzZWNwbHVzIjogeyJjb3JyZWN0IjogMCwgImluY29ycmVjdCI6IDB9LCAicXVpeiI6IHsiY29ycmVjdCI6IDAsICJpbmNvcnJlY3QiOiAwfX0sICIxMDM2NzY2NTQ1NDAzMTk5NTM4Ijogey",
        "JjaXNzcCI6IHsiY29ycmVjdCI6IDAsICJpbmNvcnJlY3QiOiAwfSwgImNlaCI6IHsiY29ycmVjdCI6IDAsICJpbmNvcnJlY3QiOiAwfSwgImNjbmEiOiB7ImNvcnJlY3QiOiAwLCAiaW5jb3JyZWN0IjogMH0sICJhcGx1cyI6IHsiY29ycmVjdCI6IDEsICJpbmNvcnJlY3QiOiAwfSwgIm5ldHBsdXMiOiB7ImNvcnJlY3QiOiAwLCAiaW5jb3JyZWN0IjogMH0sICJsaW51eHBsdXMiOiB7ImNvcnJlY3QiOiAwLCAiaW5jb3JyZWN0IjogMH0sICJzZWNwbHVzIjogeyJjb3JyZWN0IjogMCwgImluY29ycmVjdCI6IDB9LCAicXVpeiI6IHsiY29ycmVjdCI6IDAsICJpbmNvcnJlY3QiOiAwfX19",
    ]

    EXPECTED_MOCK_STR = "".join(MOCK_ENCODED_STR_CHUNKS)

    leaderboard_msg = AttributeDict(
        {
            "embeds": [
                AttributeDict(
                    {
                        "fields": [
                            AttributeDict(
                                {
                                    "name": "chunk:0",
                                    "value": "```" + MOCK_ENCODED_STR_CHUNKS[0] + "```",
                                }
                            ),
                            AttributeDict(
                                {
                                    "name": "chunk:1",
                                    "value": "```" + MOCK_ENCODED_STR_CHUNKS[1] + "```",
                                }
                            ),
                            AttributeDict(
                                {
                                    "name": "chunk:2",
                                    "value": "```" + MOCK_ENCODED_STR_CHUNKS[2] + "```",
                                }
                            ),
                        ]
                    }
                ),
            ]
        }
    )

    result = get_encoded_user_scores_from_embeds(leaderboard_msg)

    assert result == EXPECTED_MOCK_STR

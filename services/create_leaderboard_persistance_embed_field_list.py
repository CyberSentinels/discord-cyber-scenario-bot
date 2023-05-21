import json
import base64


async def create_leaderboard_persistance_embed_field_list(user_scores):
    user_scores_json = json.dumps(user_scores)
    user_scores_base64 = base64.b64encode(user_scores_json.encode()).decode()
    encoded_score_chunks = split_by_1000_chars(user_scores_base64)
    field_list = []
    for i, chunk in enumerate(encoded_score_chunks):
        field_list.append({"name": "chunk:" + str(i), "value": f"```{chunk}```"})
    return field_list


def split_by_1000_chars(base64_user_scores):
    chunks = []
    chunks_len = 0
    n = len(base64_user_scores)
    while chunks_len < n:
        new_chunk = base64_user_scores[chunks_len : chunks_len + 1000]
        chunks.append(new_chunk)
        chunks_len += len(new_chunk)
    return chunks


async def test_create_leaderboard_persistance_embed():
    from services.__fixtures__.mocks import MOCK_USER_SCORES

    user_scores = MOCK_USER_SCORES
    field_list = await create_leaderboard_persistance_embed_field_list(user_scores)

    assert field_list == [
        {
            "name": "chunk:0",
            "value": "```eyIxMTExMTEiOiB7ImNpc3NwIjogeyJjb3JyZWN0IjogNSwgImluY29ycmVjdCI6IDF9LCAiY2VoIjogeyJjb3JyZWN0IjogMCwgImluY29ycmVjdCI6IDB9LCAiY2NuYSI6IHsiY29ycmVjdCI6IDAsICJpbmNvcnJlY3QiOiAwfSwgImFwbHVzIjogeyJjb3JyZWN0IjogMCwgImluY29ycmVjdCI6IDF9LCAibmV0cGx1cyI6IHsiY29ycmVjdCI6IDAsICJpbmNvcnJlY3QiOiAwfSwgImxpbnV4cGx1cyI6IHsiY29ycmVjdCI6IDAsICJpbmNvcnJlY3QiOiAwfSwgInNlY3BsdXMiOiB7ImNvcnJlY3QiOiAwLCAiaW5jb3JyZWN0IjogMH0sICJxdWl6IjogeyJjb3JyZWN0IjogMCwgImluY29ycmVjdCI6IDB9fSwgIjIyMjIyMiI6IHsiY2lzc3AiOiB7ImNvcnJlY3QiOiAwLCAiaW5jb3JyZWN0IjogMH0sICJjZWgiOiB7ImNvcnJlY3QiOiAwLCAiaW5jb3JyZWN0IjogMH0sICJjY25hIjogeyJjb3JyZWN0IjogMCwgImluY29ycmVjdCI6IDB9LCAiYXBsdXMiOiB7ImNvcnJlY3QiOiAxLCAiaW5jb3JyZWN0IjogMH0sICJuZXRwbHVzIjogeyJjb3JyZWN0IjogMCwgImluY29ycmVjdCI6IDB9LCAibGludXhwbHVzIjogeyJjb3JyZWN0IjogMiwgImluY29ycmVjdCI6IDB9LCAic2VjcGx1cyI6IHsiY29ycmVjdCI6IDAsICJpbmNvcnJlY3QiOiAwfSwgInF1aXoiOiB7ImNvcnJlY3QiOiAwLCAiaW5jb3JyZWN0IjogMX19LCAiMzMzMzMzIjogeyJjaXNzcCI6IHsiY29ycmVjdCI6IDAsICJpbmNvcnJlY3QiOiAwfSwgImNlaCI6IHsi```",
        },
        {
            "name": "chunk:1",
            "value": "```Y29ycmVjdCI6IDAsICJpbmNvcnJlY3QiOiAwfSwgImNjbmEiOiB7ImNvcnJlY3QiOiAwLCAiaW5jb3JyZWN0IjogMH0sICJhcGx1cyI6IHsiY29ycmVjdCI6IDEsICJpbmNvcnJlY3QiOiAwfSwgIm5ldHBsdXMiOiB7ImNvcnJlY3QiOiAwLCAiaW5jb3JyZWN0IjogMH0sICJsaW51eHBsdXMiOiB7ImNvcnJlY3QiOiAyLCAiaW5jb3JyZWN0IjogMH0sICJzZWNwbHVzIjogeyJjb3JyZWN0IjogMCwgImluY29ycmVjdCI6IDB9LCAicXVpeiI6IHsiY29ycmVjdCI6IDAsICJpbmNvcnJlY3QiOiAxfX0sICI0NDQ0NDQiOiB7ImNpc3NwIjogeyJjb3JyZWN0IjogMCwgImluY29ycmVjdCI6IDB9LCAiY2VoIjogeyJjb3JyZWN0IjogMCwgImluY29ycmVjdCI6IDB9LCAiY2NuYSI6IHsiY29ycmVjdCI6IDAsICJpbmNvcnJlY3QiOiAwfSwgImFwbHVzIjogeyJjb3JyZWN0IjogMSwgImluY29ycmVjdCI6IDB9LCAibmV0cGx1cyI6IHsiY29ycmVjdCI6IDAsICJpbmNvcnJlY3QiOiAwfSwgImxpbnV4cGx1cyI6IHsiY29ycmVjdCI6IDIsICJpbmNvcnJlY3QiOiAwfSwgInNlY3BsdXMiOiB7ImNvcnJlY3QiOiAwLCAiaW5jb3JyZWN0IjogMH0sICJxdWl6IjogeyJjb3JyZWN0IjogMCwgImluY29ycmVjdCI6IDF9fX0=```",
        },
    ]

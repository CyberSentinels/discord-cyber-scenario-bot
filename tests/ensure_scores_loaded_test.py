from ..bot import ensure_scores_loaded

def mock_object():
    return { "mock": "value" }

loaded_scores_from_leaderboard = False

async def test_ensure_scores_loaded():
    # given
    global loaded_scores_from_leaderboard
    loaded_scores_from_leaderboard = False

    user_scores = mock_object()
    leaderboard_persistance_channel = mock_object()
    client = mock_object()

    # when
    await ensure_scores_loaded(user_scores, leaderboard_persistance_channel, client)

    # then
    assert loaded_scores_from_leaderboard is True

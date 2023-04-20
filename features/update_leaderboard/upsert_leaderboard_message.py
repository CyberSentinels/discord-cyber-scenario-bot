async def upsert_leaderboard_message(leaderboard_channel, leaderboard_embed, client):
    leaderboard_message = None
    async for message in leaderboard_channel.history():
        if message.author == client.user:
            leaderboard_message = message
            break
    if leaderboard_message is None:
        leaderboard_message = await leaderboard_channel.send(embed=leaderboard_embed)
    else:
        await leaderboard_message.edit(embed=leaderboard_embed)

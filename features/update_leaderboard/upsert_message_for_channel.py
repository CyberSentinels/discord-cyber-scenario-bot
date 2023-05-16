async def upsert_message_for_channel(channel, embed, client):
    the_msg = None
    async for message in channel.history():
        if message.author == client.user:
            the_msg = message
            break
    if the_msg is None:
        the_msg = await channel.send(embed=embed)
    else:
        await the_msg.edit(embed=embed)

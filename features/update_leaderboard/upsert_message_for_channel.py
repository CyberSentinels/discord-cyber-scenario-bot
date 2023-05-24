async def upsert_message_for_channel(channel, embed, client):
    try:
        the_msg = None
        async for message in channel.history():
            if message.author == client.user:
                if message.embeds and message.embeds[0].title == embed.title:
                    the_msg = message
                    break
        if the_msg is None:
            the_msg = await channel.send(embed=embed)
        else:
            await the_msg.edit(embed=embed)
    except Exception as e:
        # Handle any errors that occur during the process
        raise ValueError(f"Error upserting message for channel: {str(e)}")

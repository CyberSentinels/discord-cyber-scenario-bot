import discord
from discord import Embed
from features.netplus.handle_netplus import handle_netplus

async def task_netplus(client, guildid, channelid, netplusrole, user_responses, valid_emojis):
    try:
        # Replace guildid with the ID of the server/guild where the role exists
        guild = client.get_guild(int(guildid))
        # Replace netplusrole with the name of the role to be mentioned
        role = guild.get_role(int(netplusrole))
        print(f"Translated ID to Role Name :{role} {netplusrole}")
        # Replace channelid with the ID of the channel to send the message in
        channel = guild.get_channel(int(channelid))
        message = f"It's time for the daily Network+ quiz! {role.mention}, make sure to participate!"
        await channel.send(message)
        response, question_id = handle_netplus(user_responses)
        embed = Embed(description=response)
        embed.set_footer(text=question_id)
        message = await channel.send(embed=embed)
        # Add reactions for each answer choice
        for emoji in valid_emojis:
            await message.add_reaction(emoji)


    except discord.errors.Forbidden:
        # This exception is raised if the bot doesn't have permission to perform an action
        await channel.send(f"Error: I don't have permission to perform this action. Please check my permissions.")
    except discord.errors.HTTPException:
        # This exception is raised if the bot fails to send a message
        await channel.send("Error: Failed to send message. Please try again later.")
    except Exception as e:
        # This exception is raised if any unexpected error occurs
        await channel.send(f"Error: {e}. An unexpected error occurred.")
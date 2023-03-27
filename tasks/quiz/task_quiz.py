import discord
from discord import Embed
from features.quiz.handle_quiz import handle_quiz

async def task_quiz(client, guildid, channelid, quizrole, user_responses):
    if guildid is None or channelid is None or quizrole is None:
        return
    try:
        # Replace guildid with the ID of the server/guild where the role exists
        guild = client.get_guild(int(guildid))
        # Replace quizrole with the name of the role to be mentioned
        role = guild.get_role(int(quizrole))
        print(f"Translated ID to Role Name : {role}")
        # Replace channelid with the ID of the channel to send the message in
        channel = guild.get_channel(int(channelid))
        message = f"It's time for the daily quiz! {role.mention}, make sure to participate!"
        await channel.send(message)
        response = handle_quiz(user_responses)
        embed = Embed(description=response)
        message = await channel.send(embed=embed)


    except discord.errors.Forbidden:
        # This exception is raised if the bot doesn't have permission to perform an action
        await channel.send(f"Error: I don't have permission to perform this action. Please check my permissions.")
    except discord.errors.HTTPException:
        # This exception is raised if the bot fails to send a message
        await channel.send("Error: Failed to send message. Please try again later.")
    except Exception as e:
        # This exception is raised if any unexpected error occurs
        await channel.send(f"Error: {e}. An unexpected error occurred.")
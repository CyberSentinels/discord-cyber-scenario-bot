import discord
from discord.ext import commands, tasks
import os

from features.bluescenarios.handle_bluescenarios import handle_bluescenarios
from features.redscenarios.handle_redscenarios import handle_redscenarios
from features.scenarios.handle_scenarios import handle_scenarios

from features.quiz.handle_quiz import handle_quiz
from features.netplus.handle_netplus import handle_netplus
from features.aplus.handle_aplus import handle_aplus
from features.secplus.handle_secplus import handle_secplus

from features.subnet.handle_subnet import handle_subnet

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix=["!", "/"], intents=intents)

# always needed
bottoken = os.environ.get("BOT_TOKEN")
# only needed if you want the timed quizes
guildid = os.environ.get("GUILD_ID")
channelid = os.environ.get("CHANNEL_ID")
aplusrole = os.environ.get("APLUSROLE")
netplusrole = os.environ.get("NETPLUSROLE")
secplusrole = os.environ.get("SECPLUSROLE")
quizrole = os.environ.get("QUIZROLE")

@client.hybrid_command()
async def scenario(ctx):
    try:
        response = handle_scenarios()
        await ctx.send(response)
    except Exception as e:
        print(f"An error occurred while running the 'scenario' command: {e}")
        await ctx.send("Sorry, an error occurred while running that command.")

@client.hybrid_command()
async def bluescenario(ctx):
    try:
        response = handle_bluescenarios()
        await ctx.send(response)
    except KeyError as e:
        await ctx.send(f"Error: {e}. This scenario is missing a required field.")
    except Exception as e:
        await ctx.send(f"Error: {e}. An unexpected error occurred.")

@client.hybrid_command()
async def redscenario(ctx):
    try:
        response = handle_redscenarios()
        await ctx.send(response)
    except KeyError as e:
        await ctx.send(f"Error: {e}. This scenario is missing a required field.")
    except Exception as e:
        await ctx.send(f"Error: {e}. An unexpected error occurred.")

@client.hybrid_command()
async def quiz(ctx):
    try:
        response = handle_quiz()
        await ctx.send(response)
    except Exception as e:
        await ctx.send(f"Error: {e}. An unexpected error occurred.")

@client.hybrid_command()
async def aplus(ctx):
    try:
        response = handle_aplus()
        await ctx.send(response)
    except Exception as e:
        await ctx.send(f"Error: {e}. An unexpected error occurred.")

@client.hybrid_command()
async def netplus(ctx):
    try:
        response = handle_netplus()
        await ctx.send(response)
    except Exception as e:
        await ctx.send(f"Error: {e}. An unexpected error occurred.")

@client.hybrid_command()
async def secplus(ctx):
    try:
        response = handle_secplus()
        await ctx.send(response)
    except Exception as e:
        await ctx.send(f"Error: {e}. An unexpected error occurred.")

@client.hybrid_command()
async def subnet(ctx, ip: str, mask: str):
    try:
        response = handle_subnet(ip: str, mask: str)
        await ctx.send(response)
    except Exception as e:
        await ctx.send(f"Error: {e}. Invalid input format.")

@client.hybrid_command()
async def commands(ctx):
    try:
        response = f"**Command prefix**: '!', '/'\n\n**Quiz**: Replies with a random Cyber Security Awareness Question.\n\n**Scenario**: Replies with either a red team or blue team scenario. \n\n**Bluescenario**: Replies with a blue team scenario. \n\n**Redscenario**: Replies with a redteam scenario.\n\n**Aplus**: Replies with CompTIA's A+ related prompts.\n\n**Netplus**: Replies with CompTIA's Network+ related prompts.\n\n**Secplus**: Replies with CompTIA's Security+ related prompts.\n\n**Commands**: Replies with this message.\n\n**Socials**: Replies with the various bot social media accounts and websites."
        await ctx.send(response)
    except Exception as e:
        await ctx.send(f"Error: {e}. An unexpected error occurred.")

@client.hybrid_command()
async def socials(ctx):
    try:
        response = f"**Website**: https://cybersentinels.com\n\n**GitHub**: https://github.com/cybersentinels"
        await ctx.send(response)
    except Exception as e:
        await ctx.send(f"Error: {e}. An unexpected error occurred.")

# Define a function to send the message and run the quiz command
@tasks.loop(hours=24, minutes=60*14)
async def send_message_and_quiz():
    if guildid is None or channelid is None or quizrole is None:
        return
    try:
        # Replace guildid with the ID of the server/guild where the role exists
        guild = client.get_guild(guildid)
        # Replace quizrole with the name of the role to be mentioned
        role = discord.utils.get(guild.roles, name=quizrole)

        # Replace channelid with the ID of the channel to send the message in
        channel = client.get_channel(channelid)
        message = f"It's time for the daily quiz! {role.mention}, make sure to participate!"
        await channel.send(message)
        response = handle_quiz()
        await channel.send(response)

    except discord.errors.Forbidden:
        # This exception is raised if the bot doesn't have permission to perform an action
        await channel.send(f"Error: I don't have permission to perform this action. Please check my permissions.")
    except discord.errors.HTTPException:
        # This exception is raised if the bot fails to send a message
        await channel.send("Error: Failed to send message. Please try again later.")
    except Exception as e:
        # This exception is raised if any unexpected error occurs
        await channel.send(f"Error: {e}. An unexpected error occurred.")

@send_message_and_quiz.before_loop
async def before_send_message_and_quiz():
    await client.wait_until_ready()

# Define the A+ quiz task to run at 8:00am every day
@tasks.loop(hours=24, minutes=60*8)
async def send_message_and_quiz_aplus():
    if guildid is None or channelid is None or aplusrole is None:
        return
    try:
        # Replace guildid with the ID of the server/guild where the role exists
        guild = client.get_guild(guildid)
        # Replace aplusrole with the name of the role to be mentioned
        role = discord.utils.get(guild.roles, name=aplusrole)

        # Replace channelid with the ID of the channel to send the message in
        channel = client.get_channel(channelid)
        message = f"It's time for the daily A+ quiz! {role.mention}, make sure to participate!"
        await channel.send(message)
        response = handle_aplus()
        await channel.send(response)

    except discord.errors.Forbidden:
        # This exception is raised if the bot doesn't have permission to perform an action
        await channel.send(f"Error: I don't have permission to perform this action. Please check my permissions.")
    except discord.errors.HTTPException:
        # This exception is raised if the bot fails to send a message
        await channel.send("Error: Failed to send message. Please try again later.")
    except Exception as e:
        # This exception is raised if any unexpected error occurs
        await channel.send(f"Error: {e}. An unexpected error occurred.")

@send_message_and_quiz_aplus.before_loop
async def before_send_message_and_quiz_aplus():
    await client.wait_until_ready()

# Define the Network+ quiz task to run at 10:00am every day
@tasks.loop(hours=24, minutes=60*10)
async def send_message_and_quiz_netplus():
    if guildid is None or channelid is None or netplusrole is None:
        return
    try:
        # Replace guildid with the ID of the server/guild where the role exists
        guild = client.get_guild(guildid)
        # Replace netplusrole with the name of the role to be mentioned
        role = discord.utils.get(guild.roles, name=netplusrole)

        # Replace channelid with the ID of the channel to send the message in
        channel = client.get_channel(channelid)
        message = f"It's time for the daily Network+ quiz! {role.mention}, make sure to participate!"
        await channel.send(message)
        response = handle_netplus()
        await channel.send(response)

    except discord.errors.Forbidden:
        # This exception is raised if the bot doesn't have permission to perform an action
        await channel.send(f"Error: I don't have permission to perform this action. Please check my permissions.")
    except discord.errors.HTTPException:
        # This exception is raised if the bot fails to send a message
        await channel.send("Error: Failed to send message. Please try again later.")
    except Exception as e:
        # This exception is raised if any unexpected error occurs
        await channel.send(f"Error: {e}. An unexpected error occurred.")

@send_message_and_quiz_netplus.before_loop
async def before_send_message_and_quiz_netplus():
    await client.wait_until_ready()

# Define the Security+ quiz task to run at 12:00pm every day
@tasks.loop(hours=24, minutes=60*12)
async def send_message_and_quiz_secplus():
    if guildid is None or channelid is None or secplusrole is None:
        return
    try:
        # Replace guildid with the ID of the server/guild where the role exists
        guild = client.get_guild(guildid)
        # Replace secplusrole with the name of the role to be mentioned
        role = discord.utils.get(guild.roles, name=secplusrole)

        # Replace channelid with the ID of the channel to send the message in
        channel = client.get_channel(channelid)
        message = f"It's time for the daily Security+ quiz! {role.mention}, make sure to participate!"
        await channel.send(message)
        response = handle_secplus()
        await channel.send(response)

    except discord.errors.Forbidden:
        # This exception is raised if the bot doesn't have permission to perform an action
        await channel.send(f"Error: I don't have permission to perform this action. Please check my permissions.")
    except discord.errors.HTTPException:
        # This exception is raised if the bot fails to send a message
        await channel.send("Error: Failed to send message. Please try again later.")
    except Exception as e:
        # This exception is raised if any unexpected error occurs
        await channel.send(f"Error: {e}. An unexpected error occurred.")

@send_message_and_quiz_secplus.before_loop
async def before_send_message_and_quiz_secplus():
    await client.wait_until_ready()

# Define the on_ready event handler
@client.event
async def on_ready():
    # Get the name of the bot user
    bot_username = client.user.name
    
    # Find the Discord guild object based on its ID
    guild = client.get_guild(int(guildid))
    
    # Find the channel object based on its ID
    channel = guild.get_channel(int(channelid))
    
    # Print a message indicating that the bot is logged in and ready
    print(f"Logged in as {bot_username} ({client.user.id})")
    print(f"Connected to Discord server '{guild.name}' ({guild.id})")
    print(f"Bot is ready and listening for commands in channel '{channel.name}' ({channel.id})")

client.run(bottoken)

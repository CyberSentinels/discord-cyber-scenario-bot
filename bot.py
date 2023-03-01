import discord
from discord.ext import commands, tasks
import os
import datetime
import asyncio

# import features
from features.bluescenarios.handle_bluescenarios import handle_bluescenarios
from features.redscenarios.handle_redscenarios import handle_redscenarios
from features.scenarios.handle_scenarios import handle_scenarios
from features.quiz.handle_quiz import handle_quiz
from features.netplus.handle_netplus import handle_netplus
from features.aplus.handle_aplus import handle_aplus
from features.secplus.handle_secplus import handle_secplus
from features.ccna.handle_ccna import handle_ccna
from features.cissp.handle_cissp import handle_cissp
from features.subnet.handle_subnet import handle_subnet

#import tasks
from tasks.aplus.task_aplus import task_aplus
from tasks.netplus.task_netplus import task_netplus
from tasks.secplus.task_secplus import task_secplus
from tasks.quiz.task_quiz import task_quiz

import tracemalloc
tracemalloc.start()

#setup the discord.py client and intents
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix=["!", "/"], intents=intents)

# setup variables
# always needed
bottoken = os.environ.get("BOT_TOKEN")
# only needed if you want the timed quizes
guildid = os.environ.get("GUILD_ID")
channelid = os.environ.get("CHANNEL_ID")
aplusrole = os.environ.get("APLUSROLE")
netplusrole = os.environ.get("NETPLUSROLE")
secplusrole = os.environ.get("SECPLUSROLE")
quizrole = os.environ.get("QUIZROLE")

#print variables to confirmed they were passed in correctly
print(f"BOT_TOKEN: {bottoken}")
print(f"GUILD_ID: {guildid}")
print(f"CHANNEL_ID: {channelid}")
print(f"APLUSROLE: {aplusrole}")
print(f"NETPLUSROLE: {netplusrole}")
print(f"SECPLUSROLE: {secplusrole}")
print(f"QUIZROLE: {quizrole}")

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
async def ccna(ctx):
    try:
        response = handle_ccna()
        await ctx.send(response)
    except Exception as e:
        await ctx.send(f"Error: {e}. An unexpected error occurred.")

@client.hybrid_command()
async def cissp(ctx):
    try:
        response = handle_cissp()
        await ctx.send(response)
    except Exception as e:
        await ctx.send(f"Error: {e}. An unexpected error occurred.")

@client.hybrid_command()
async def subnet(ctx, ip: str, mask: str):
    try:
        response = handle_subnet(ip, mask)
        await ctx.send(response)
    except Exception as e:
        await ctx.send(f"Error: {e}. Invalid input format.")

@client.hybrid_command()
async def commands(ctx):
    try:
        response = """**Command prefix**: '!', '/'

**Quiz**: Replies with a random Cyber Security Awareness Question.

**Scenario**: Replies with either a red team or blue team scenario.

**Bluescenario**: Replies with a blue team scenario.

**Redscenario**: Replies with a red team scenario.

**Aplus**: Replies with CompTIA's A+ related prompts.

**Netplus**: Replies with CompTIA's Network+ related prompts.

**Secplus**: Replies with CompTIA's Security+ related prompts.

**CCNA**: Replies with Cisco CCNA related multiple choice prompts.

**CISSP**: Replies with Replies with a ISC2's CISSP multiple choice prompt.

**Commands**: Replies with this message.

**Socials**: Replies with the various bot social media accounts and websites."""
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
@tasks.loop(hours=24, minutes=60*18)
async def send_message_and_quiz():
    try:
        await task_quiz(client, guildid, channelid, quizrole)
    except Exception as e:
        print(f"An error occurred while running send_message_and_quiz: {e}")

@send_message_and_quiz.before_loop
async def before_send_message_and_quiz():
    await client.wait_until_ready()
    if guildid is None or channelid is None or quizrole is None:
        print("Missing required input parameters. Please make sure to set guildid, channelid, and quizrole before starting the task.")
        return
    try:
        now = datetime.datetime.utcnow()
        scheduled_time = datetime.time(hour=0, minute=0)  # Adjust the time as necessary
        # Calculate the time until the next scheduled time
        if now.time() < scheduled_time:
            wait_time = (datetime.datetime.combine(now.date(), scheduled_time) - now).total_seconds()
        else:
            wait_time = (datetime.datetime.combine(now.date() + datetime.timedelta(days=1), scheduled_time) - now).total_seconds()
        # Wait for the calculated time
        print(f"Waiting for {wait_time} seconds before starting task loop")
        await asyncio.sleep(wait_time)
    except Exception as e:
        print(f"An error occurred while setting up send_message_and_quiz: {e}")

# Define the A+ quiz task to run at 4:00pm every day
@tasks.loop(hours=24, minutes=60*16)
async def send_message_and_quiz_aplus():
    try:
        await task_aplus(client, guildid, channelid, aplusrole)
    except Exception as e:
        print(f"An error occurred while running send_message_and_quiz_aplus: {e}")

@send_message_and_quiz_aplus.before_loop
async def before_send_message_and_quiz_aplus():
    await client.wait_until_ready()
    if guildid is None or channelid is None or aplusrole is None:
        print("Missing required input parameters. Please make sure to set guildid, channelid, and aplusrole before starting the task.")
        return
    try:
        now = datetime.datetime.utcnow()
        scheduled_time = datetime.time(hour=20, minute=0)  # Adjust the time as necessary
        # Calculate the time until the next scheduled time
        if now.time() < scheduled_time:
            wait_time = (datetime.datetime.combine(now.date(), scheduled_time) - now).total_seconds()
        else:
            wait_time = (datetime.datetime.combine(now.date() + datetime.timedelta(days=1), scheduled_time) - now).total_seconds()
        # Wait for the calculated time
        print(f"Waiting for {wait_time} seconds before starting task loop")
        await asyncio.sleep(wait_time)
    except Exception as e:
        print(f"An error occurred while setting up send_message_and_quiz_aplus: {e}")

# Define the Network+ quiz task to run at 2:00pm every day
@tasks.loop(hours=24, minutes=60*14)
async def send_message_and_quiz_netplus():
    try:
        await task_netplus(client, guildid, channelid, netplusrole)
    except Exception as e:
        print(f"An error occurred while running send_message_and_quiz_netplus: {e}")

@send_message_and_quiz_netplus.before_loop
async def before_send_message_and_quiz_netplus():
    try:
        await client.wait_until_ready()
        if guildid is None or channelid is None or netplusrole is None:
            return
        now = datetime.datetime.utcnow()
        scheduled_time = datetime.time(hour=18, minute=0)  # Adjust the time as necessary
        # Calculate the time until the next scheduled time
        if now.time() < scheduled_time:
            wait_time = (datetime.datetime.combine(now.date(), scheduled_time) - now).total_seconds()
        else:
            wait_time = (datetime.datetime.combine(now.date() + datetime.timedelta(days=1), scheduled_time) - now).total_seconds()
        # Wait for the calculated time
        print(f"Waiting for {wait_time} seconds before starting task loop")
        await asyncio.sleep(wait_time)
    except Exception as e:
        print(f"An error occurred while running the 'send_message_and_quiz_netplus.before_loop' command: {e}")
        return

# Define the Security+ quiz task to run at 12:00pm every day
@tasks.loop(hours=24, minutes=60*12)
async def send_message_and_quiz_secplus():
    try:
        await task_secplus(client, guildid, channelid, secplusrole)
    except Exception as e:
        print(f"An error occurred while running the 'task_secplus' command: {e}")
        return

@send_message_and_quiz_secplus.before_loop
async def before_send_message_and_quiz_secplus():
    try:
        await client.wait_until_ready()
        if guildid is None or channelid is None or secplusrole is None:
            return
        now = datetime.datetime.utcnow()
        scheduled_time = datetime.time(hour=16, minute=0)  # Adjust the time as necessary
        # Calculate the time until the next scheduled time
        if now.time() < scheduled_time:
            wait_time = (datetime.datetime.combine(now.date(), scheduled_time) - now).total_seconds()
        else:
            wait_time = (datetime.datetime.combine(now.date() + datetime.timedelta(days=1), scheduled_time) - now).total_seconds()
        # Wait for the calculated time
        print(f"Waiting for {wait_time} seconds before starting task loop")
        await asyncio.sleep(wait_time)
    except Exception as e:
        print(f"An error occurred while running the 'before_send_message_and_quiz_secplus' command: {e}")
        return
    

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        print(f"Unsupported command detected: {ctx.message.content}")
    else:
        print(f"Unsupported command detected: {error}")


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

    print(f"Starting Scheduled Task Loops")
    try:
        if guildid is not None and channelid is not None and secplusrole is not None:
            try:
                send_message_and_quiz_secplus.start()
                print(f"Sec Plus Task Scheduled Successfully")
            except Exception as e:
                print(f"Error starting Sec Plus Task: {e}")
        if guildid is not None and channelid is not None and netplusrole is not None:
            try:
                send_message_and_quiz_netplus.start()
                print(f"Net Plus Task Scheduled Successfully")
            except Exception as e:
                print(f"Error starting Net Plus Task: {e}")
        if guildid is not None and channelid is not None and aplusrole is not None:    
            try:
                send_message_and_quiz_aplus.start()
                print(f"A Plus Task Scheduled Successfully")
            except Exception as e:
                print(f"Error starting A Plus Task: {e}")
        if guildid is not None and channelid is not None and quizrole is not None: 
            try:  
                send_message_and_quiz.start()
                print(f"Quiz Task Scheduled Successfully")
            except Exception as e:
                print(f"Error starting Quiz Task: {e}")
    except Exception as e:
        print(f"Error starting scheduled tasks: {e}")

client.run(bottoken)

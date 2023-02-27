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
from features.subnet.handle_subnet import handle_subnet

#import tasks
from tasks.aplus.task_aplus import task_aplus
from tasks.netplus.task_netplus import task_netplus
from tasks.secplus.task_secplus import task_secplus
from tasks.quiz.task_quiz import task_quiz

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
async def subnet(ctx, ip: str, mask: str):
    try:
        response = handle_subnet(ip, mask)
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
@tasks.loop(hours=24, minutes=60*18)
async def send_message_and_quiz():
    task_quiz(client, guildid, channelid, quizrole)

@send_message_and_quiz.before_loop
async def before_send_message_and_quiz():
    await client.wait_until_ready()
    if guildid is None or channelid is None or quizrole is None:
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
    # Start the task loop
    send_message_and_quiz.start(client, guildid, channelid, quizrole)
    print(f"Quiz Task loop started")

# Define the A+ quiz task to run at 4:00pm every day
@tasks.loop(hours=24, minutes=60*16)
async def send_message_and_quiz_aplus():
    task_aplus(client, guildid, channelid, aplusrole)

@send_message_and_quiz_aplus.before_loop
async def before_send_message_and_quiz_aplus():
    await client.wait_until_ready()
    if guildid is None or channelid is None or aplusrole is None:
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
    # Start the task loop
    send_message_and_quiz_aplus.start(client, guildid, channelid, aplusrole)
    print(f"Aplus Task loop started")


# Define the Network+ quiz task to run every minute
@tasks.loop(minutes=1)
async def send_message_and_quiz_netplus():
    task_netplus(client, guildid, channelid, netplusrole)

@send_message_and_quiz_netplus.before_loop
async def before_send_message_and_quiz_netplus():
    await client.wait_until_ready()
    if guildid is None or channelid is None or netplusrole is None:
        return
    send_message_and_quiz_netplus.start(client, guildid, channelid, netplusrole)
    print(f"Netplus Task loop started")



# Define the Security+ quiz task to run at 12:00pm every day
@tasks.loop(hours=24, minutes=60*12)
async def send_message_and_quiz_secplus():
    task_secplus(client, guildid, channelid, secplusrole)

@send_message_and_quiz_secplus.before_loop
async def before_send_message_and_quiz_secplus():
    await client.wait_until_ready()
    if guildid is None or channelid is None or secplusrole is None:
        return
    now = datetime.datetime.utcnow()
    scheduled_time = datetime.time(hour=12, minute=0)  # Adjust the time as necessary
    # Calculate the time until the next scheduled time
    if now.time() < scheduled_time:
        wait_time = (datetime.datetime.combine(now.date(), scheduled_time) - now).total_seconds()
    else:
        wait_time = (datetime.datetime.combine(now.date() + datetime.timedelta(days=1), scheduled_time) - now).total_seconds()
    # Wait for the calculated time
    print(f"Waiting for {wait_time} seconds before starting task loop")
    await asyncio.sleep(wait_time)
    # Start the task loop
    send_message_and_quiz_secplus(client, guildid, channelid, secplusrole)
    print(f"Secplus Task loop started")

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
                send_message_and_quiz_secplus.start(client, guildid, channelid, secplusrole)
                print(f"Sec Plus Task Scheduled Successfully")
            except:
                print(f"Sec Plus Task Failed to Start")
        if guildid is not None and channelid is not None and netplusrole is not None:
            try:
                send_message_and_quiz_netplus.start()
                print(f"Net Plus Task Scheduled Successfully")
            except:
                print(f"Net Plus Task Failed to Start")
        if guildid is not None and channelid is not None and aplusrole is not None:    
            try:
                send_message_and_quiz_aplus.start(client, guildid, channelid, aplusrole)
                print(f"A Plus Task Scheduled Successfully")
            except:
                print(f"A Plus Task Failed to Start")
        if guildid is not None and channelid is not None and quizrole is not None: 
            try:  
                send_message_and_quiz.start(client, guildid, channelid, quizrole)
                print(f"Quiz Task Scheduled Successfully")
            except:
                print(f"Quiz Task Failed to Start")
    except:
        print(f"Tasks Failed")

client.run(bottoken)

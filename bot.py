import asyncio
import datetime
import discord
import os
import random
from discord import Activity, ActivityType, Status, app_commands
from discord.ext import commands, tasks

# import features
from features.aplus.handle_aplus import *
from features.bluescenarios.handle_bluescenarios import *
from features.ccna.handle_ccna import *
from features.cissp.handle_cissp import *
from features.dns.handle_dns import *
from features.hash.handle_hash import *
from features.netplus.handle_netplus import *
from features.ping.handle_ping import *
from features.quiz.handle_quiz import *
from features.redscenarios.handle_redscenarios import *
from features.scenarios.handle_scenarios import *
from features.secplus.handle_secplus import *
from features.shodan.handle_shodanip import *
from features.subnet.handle_subnet import *
from features.whois.handle_whois import *

# import tasks
from tasks.aplus.task_aplus import task_aplus
from tasks.netplus.task_netplus import task_netplus
from tasks.quiz.task_quiz import task_quiz
from tasks.secplus.task_secplus import task_secplus

import tracemalloc

tracemalloc.start()

# setup the discord.py client and intents
intents = discord.Intents.all()
intents.message_content = True
client = commands.Bot(command_prefix=["!", "/"], intents=intents)
# tree = app_commands.CommandTree(client)

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

# print variables to confirmed they were passed in correctly
print(f"BOT_TOKEN: {bottoken}")
print(f"GUILD_ID: {guildid}")
print(f"CHANNEL_ID: {channelid}")
print(f"APLUSROLE: {aplusrole}")
print(f"NETPLUSROLE: {netplusrole}")
print(f"SECPLUSROLE: {secplusrole}")
print(f"QUIZROLE: {quizrole}")


@client.hybrid_command(
    name="quiz", description="Replies with CompTIA's A+ related prompt."
)
async def quiz(ctx):
    try:
        response = handle_quiz()
        await ctx.send(response)
    except Exception as e:
        await ctx.send(f"Error: {e}. An unexpected error occurred.")


@client.hybrid_command(
    name="scenario", description="Replies with either a red team or blue team scenario."
)
async def scenario(ctx):
    try:
        response = handle_scenarios()
        await ctx.send(response)
    except Exception as e:
        print(f"An error occurred while running the 'scenario' command: {e}")
        await ctx.send("Sorry, an error occurred while running that command.")


@client.hybrid_command(
    name="bluescenario", description="Replies with a blue team scenario."
)
async def bluescenario(ctx):
    try:
        response = handle_bluescenarios()
        await ctx.send(response)
    except KeyError as e:
        await ctx.send(f"Error: {e}. This scenario is missing a required field.")
    except Exception as e:
        await ctx.send(f"Error: {e}. An unexpected error occurred.")


@client.hybrid_command(
    name="redscenario", description="Replies with a redteam scenario."
)
async def redscenario(ctx):
    try:
        response = handle_redscenarios()
        await ctx.send(response)
    except KeyError as e:
        await ctx.send(f"Error: {e}. This scenario is missing a required field.")
    except Exception as e:
        await ctx.send(f"Error: {e}. An unexpected error occurred.")


@client.hybrid_command(
    name="aplus", description="Replies with CompTIA's A+ related prompt."
)
async def aplus(ctx):
    try:
        response = handle_aplus()
        await ctx.send(response)
    except Exception as e:
        await ctx.send(f"Error: {e}. An unexpected error occurred.")


@client.hybrid_command(
    name="netplus", description="Replies with CompTIA's Network+ related prompt."
)
async def netplus(ctx):
    try:
        response = handle_netplus()
        await ctx.send(response)
    except Exception as e:
        await ctx.send(f"Error: {e}. An unexpected error occurred.")


@client.hybrid_command(
    name="secplus", description="Replies with CompTIA's Security+ related prompt."
)
async def secplus(ctx):
    try:
        response = handle_secplus()
        await ctx.send(response)
    except Exception as e:
        await ctx.send(f"Error: {e}. An unexpected error occurred.")


@client.hybrid_command(
    name="ccna",
    description="Replies with Replies with a Cisco's CCNA multiple choice prompt.",
)
async def ccna(ctx):
    try:
        response = handle_ccna()
        await ctx.send(response)
    except Exception as e:
        await ctx.send(f"Error: {e}. An unexpected error occurred.")


@client.hybrid_command(
    name="cissp",
    description="Replies with Replies with a ISC2's CISSP multiple choice prompt.",
)
async def cissp(ctx):
    try:
        response = handle_cissp()
        await ctx.send(response)
    except Exception as e:
        await ctx.send(f"Error: {e}. An unexpected error occurred.")

@client.hybrid_command(
    name="dns", description="Gives you useful information about a dns name."
)
async def dns(ctx, domain: str):
    try:
        response = await handle_dns(domain)
        await ctx.send(embed=response)
    except Exception as e:
        await ctx.send(f"Error: {e}. Invalid input format.")

@client.hybrid_command(
    name="hash",
    description="Hashes a message using the specified algorithm."
)
async def hash(ctx, algorithm: str, message: str):
    try:
        response = await handle_hash(message, algorithm)
        await ctx.send(response)
    except Exception as e:
        await ctx.send(f"Error: {e}. Invalid input format or unsupported hashing algorithm.")


@client.hybrid_command(
    name="ping", description="Sends a ping packet to a specified IP address to check if it is reachable."
)
async def ping(ctx, ip: str):
    try:
        response = await handle_ping(ip)
        await ctx.send(response)
    except Exception as e:
        await ctx.send(f"Error: {e}. Invalid input format or IP address not reachable.")

@client.hybrid_command(
    name="shodanip", description="Gives you useful information about a given ip address."
)
async def shodanip(ctx, ip: str):
    try:
        response = await handle_shodanip(ip)
        await ctx.send(embed=response)
    except Exception as e:
        await ctx.send(f"Error: {e}. Invalid input format.")

@client.hybrid_command(
    name="subnet", description="Gives you useful information about a given subnet."
)
async def subnet(ctx, ip: str, mask: str):
    try:
        response = await handle_subnet(ip, mask)
        await ctx.send(response)
    except Exception as e:
        await ctx.send(f"Error: {e}. Invalid input format.")

@client.hybrid_command(
    name="whois", description="Gives you useful information about a given subnet."
)
async def whois(ctx, domain: str):
    try:
        response = await handle_whois(domain)
        await ctx.send(response)
    except Exception as e:
        await ctx.send(f"Error: {e}. Invalid input format.")

@client.hybrid_command(name="commands", description="Describes the available commands.")
async def commands(ctx):
    try:
        response = """**Command prefix**: '!', '/'

### Quiz and Scenario Commands
- **Aplus**: Replies with CompTIA's A+ related prompt.
- **Bluescenario**: Replies with a blue team scenario.
- **CCNA**: Replies with Cisco's CCNA multiple choice prompt.
- **CISSP**: Replies with ISC2's CISSP multiple choice prompt.
- **Netplus**: Replies with CompTIA's Network+ related prompt.
- **Quiz**: Replies with a random Cyber Security Awareness Question.
- **Redscenario**: Replies with a redteam scenario.
- **Secplus**: Replies with CompTIA's Security+ related prompt.

### Tool Commands:
- **Dns**: Takes in a `domain name` and returns A, AAAA, NS, TXT, etc. records.
- **Hash**: Takes in `1 of 4 supported algos` and a `string` and outputs a corresponding hash.
- **Ping**: Takes in an `IP address` and returns with a success message and average latency or a failure message.
- **Shodanip**: Takes in an `IP address` and outputs useful information from https://internetdb.shodan.io/.
- **Subnet**: Takes in an `IP address` and a `Subnet Mask` and outputs the Range, Usable IPs, Gateway Address, Broadcast Address, and Number of Supported Hosts.
- **Whois**: Takes in a `domain name` and outputs domain whois information.

### Informational Commands
- **Commands**: Replies with this message.
- **Socials**: Replies with the various bot social media accounts and websites."""
        await ctx.send(response)
    except Exception as e:
        await ctx.send(f"Error: {e}. An unexpected error occurred.")


@client.hybrid_command(
    name="socials",
    description="Replies with the various bot social media accounts and websites.",
)
async def socials(ctx):
    try:
        response = f"**Website**: https://cybersentinels.com\n\n**GitHub**: https://github.com/cybersentinels"
        await ctx.send(response)
    except Exception as e:
        await ctx.send(f"Error: {e}. An unexpected error occurred.")

# Define the random quiz task to run at 12:00pm every day
@tasks.loop(hours=24, minutes=0)
async def send_message_and_random():
    try:
        await client.wait_until_ready()
        if guildid is None or channelid is None or secplusrole or aplusrole or netplusrole or quizrole is None:
            return
        now = datetime.datetime.utcnow()
        scheduled_time = datetime.time(
            hour=16, minute=0
        )  # Adjust the time as necessary
        # Calculate the time until the next scheduled time
        if now.time() < scheduled_time:
            wait_time = (
                datetime.datetime.combine(now.date(), scheduled_time) - now
            ).total_seconds()
        else:
            wait_time = (
                datetime.datetime.combine(
                    now.date() + datetime.timedelta(days=1), scheduled_time
                )
                - now
            ).total_seconds()
        # Wait for the calculated time
        print(f"Waiting for {wait_time} seconds before starting task loop")
        await asyncio.sleep(wait_time)
        try:
            tasks = [task_quiz, task_aplus, task_netplus, task_secplus]
            selected_task = random.choice(tasks)
            await selected_task(client, guildid, channelid, quizrole)
        except Exception as e:
            print(f"An error occurred while running the 'send_message_and_random' task: {e}")
            return
    except Exception as e:
        print(
            f"An error occurred while running the 'send_message_and_random' command: {e}"
        )
        return

# # Define a function to send the message and run the quiz command
# @tasks.loop(hours=24, minutes=0)
# async def send_message_and_quiz():
#     await client.wait_until_ready()
#     if guildid is None or channelid is None or quizrole is None:
#         print(
#             "Missing required input parameters. Please make sure to set guildid, channelid, and quizrole before starting the task."
#         )
#         return
#     try:
#         now = datetime.datetime.utcnow()
#         scheduled_time = datetime.time(hour=0, minute=0)  # Adjust the time as necessary
#         # Calculate the time until the next scheduled time
#         if now.time() < scheduled_time:
#             wait_time = (
#                 datetime.datetime.combine(now.date(), scheduled_time) - now
#             ).total_seconds()
#         else:
#             wait_time = (
#                 datetime.datetime.combine(
#                     now.date() + datetime.timedelta(days=1), scheduled_time
#                 )
#                 - now
#             ).total_seconds()
#         # Wait for the calculated time
#         print(f"Waiting for {wait_time} seconds before starting task loop")
#         await asyncio.sleep(wait_time)
#         try:
#             await task_quiz(client, guildid, channelid, quizrole)
#         except Exception as e:
#             print(f"An error occurred while running send_message_and_quiz: {e}")
#     except Exception as e:
#         print(f"An error occurred while setting up send_message_and_quiz: {e}")

# # Define the A+ quiz task to run at 4:00pm every day
# @tasks.loop(hours=24, minutes=0)
# async def send_message_and_quiz_aplus():
#     await client.wait_until_ready()
#     if guildid is None or channelid is None or aplusrole is None:
#         print(
#             "Missing required input parameters. Please make sure to set guildid, channelid, and aplusrole before starting the task."
#         )
#         return
#     try:
#         now = datetime.datetime.utcnow()
#         scheduled_time = datetime.time(
#             hour=20, minute=0
#         )  # Adjust the time as necessary
#         # Calculate the time until the next scheduled time
#         if now.time() < scheduled_time:
#             wait_time = (
#                 datetime.datetime.combine(now.date(), scheduled_time) - now
#             ).total_seconds()
#         else:
#             wait_time = (
#                 datetime.datetime.combine(
#                     now.date() + datetime.timedelta(days=1), scheduled_time
#                 )
#                 - now
#             ).total_seconds()
#         # Wait for the calculated time
#         print(f"Waiting for {wait_time} seconds before starting task loop")
#         await asyncio.sleep(wait_time)
#         try:
#             await task_aplus(client, guildid, channelid, aplusrole)
#         except Exception as e:
#             print(f"An error occurred while running send_message_and_quiz_aplus: {e}")
#     except Exception as e:
#         print(f"An error occurred while setting up send_message_and_quiz_aplus: {e}")

# # Define the Network+ quiz task to run at 2:00pm every day
# @tasks.loop(hours=24, minutes=0)
# async def send_message_and_quiz_netplus():
#     try:
#         await client.wait_until_ready()
#         if guildid is None or channelid is None or netplusrole is None:
#             return
#         now = datetime.datetime.utcnow()
#         scheduled_time = datetime.time(
#             hour=18, minute=0
#         )  # Adjust the time as necessary
#         # Calculate the time until the next scheduled time
#         if now.time() < scheduled_time:
#             wait_time = (
#                 datetime.datetime.combine(now.date(), scheduled_time) - now
#             ).total_seconds()
#         else:
#             wait_time = (
#                 datetime.datetime.combine(
#                     now.date() + datetime.timedelta(days=1), scheduled_time
#                 )
#                 - now
#             ).total_seconds()
#         # Wait for the calculated time
#         print(f"Waiting for {wait_time} seconds before starting task loop")
#         await asyncio.sleep(wait_time)
#         try:
#             await task_netplus(client, guildid, channelid, netplusrole)
#         except Exception as e:
#             print(f"An error occurred while running send_message_and_quiz_netplus: {e}")
#     except Exception as e:
#         print(
#             f"An error occurred while running the 'send_message_and_quiz_netplus.before_loop' command: {e}"
#         )
#         return

# # Define the Security+ quiz task to run at 12:00pm every day
# @tasks.loop(hours=24, minutes=0)
# async def send_message_and_quiz_secplus():
#     try:
#         await client.wait_until_ready()
#         if guildid is None or channelid is None or secplusrole is None:
#             return
#         now = datetime.datetime.utcnow()
#         scheduled_time = datetime.time(
#             hour=16, minute=0
#         )  # Adjust the time as necessary
#         # Calculate the time until the next scheduled time
#         if now.time() < scheduled_time:
#             wait_time = (
#                 datetime.datetime.combine(now.date(), scheduled_time) - now
#             ).total_seconds()
#         else:
#             wait_time = (
#                 datetime.datetime.combine(
#                     now.date() + datetime.timedelta(days=1), scheduled_time
#                 )
#                 - now
#             ).total_seconds()
#         # Wait for the calculated time
#         print(f"Waiting for {wait_time} seconds before starting task loop")
#         await asyncio.sleep(wait_time)
#         try:
#             await task_secplus(client, guildid, channelid, secplusrole)
#         except Exception as e:
#             print(f"An error occurred while running the 'task_secplus' command: {e}")
#             return
#     except Exception as e:
#         print(
#             f"An error occurred while running the 'before_send_message_and_quiz_secplus' command: {e}"
#         )
#         return

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        print(f"Unsupported command: {ctx.message.content}")

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
    print(
        f"Bot is ready and listening for commands in channel '{channel.name}' ({channel.id})"
    )
    print("\nLogged in as:")
    print(" Username", client.user.name)
    print(" User ID", client.user.id)
    print(
        "To invite the bot in your server use this link:\n https://discord.com/api/oauth2/authorize?client_id="
        + str(client.user.id)
        + "&permissions=8&scope=bot%20applications.commands"
    )
    print("Time now", str(datetime.datetime.now()))

    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

    await client.change_presence(
        activity=Activity(
            type=ActivityType.custom, name="cybersentinels.org", url="https://cybersentinels.org/"
        ),
        status=Status.online,
    )

    print(f"Starting Scheduled Task Loops")
    send_message_and_random.start()
    # try:
    #     if guildid is not None and channelid is not None and secplusrole is not None:
    #         try:
    #             send_message_and_quiz_secplus.start()
    #             print(f"Sec Plus Task Scheduled Successfully")
    #         except Exception as e:
    #             print(f"Error starting Sec Plus Task: {e}")
    #     if guildid is not None and channelid is not None and netplusrole is not None:
    #         try:
    #             send_message_and_quiz_netplus.start()
    #             print(f"Net Plus Task Scheduled Successfully")
    #         except Exception as e:
    #             print(f"Error starting Net Plus Task: {e}")
    #     if guildid is not None and channelid is not None and aplusrole is not None:
    #         try:
    #             send_message_and_quiz_aplus.start()
    #             print(f"A Plus Task Scheduled Successfully")
    #         except Exception as e:
    #             print(f"Error starting A Plus Task: {e}")
    #     if guildid is not None and channelid is not None and quizrole is not None:
    #         try:
    #             send_message_and_quiz.start()
    #             print(f"Quiz Task Scheduled Successfully")
    #         except Exception as e:
    #             print(f"Error starting Quiz Task: {e}")
    # except Exception as e:
    #     print(f"Error starting scheduled tasks: {e}")


client.run(bottoken)

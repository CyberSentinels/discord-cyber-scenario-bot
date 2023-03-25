import asyncio
import datetime
import discord
import os
import random
import time
import traceback
from discord import Activity, ActivityType, Status, app_commands, Embed
from discord.ext import commands, tasks


# import features
from features.aplus.handle_aplus import *
from features.bluescenarios.handle_bluescenarios import *
from features.ccna.handle_ccna import *
from features.ceh.handle_ceh import *
from features.cissp.handle_cissp import *
from features.dns.handle_dns import *
from features.hash.handle_hash import *
from features.linuxplus.handle_linuxplus import *
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
from tasks.aplus.task_aplus import *
from tasks.netplus.task_netplus import *
from tasks.quiz.task_quiz import *
from tasks.secplus.task_secplus import *

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
leaderboardid = os.environ.get("LEADERBOARD_CHANNEL_ID")
channelid = os.environ.get("CHANNEL_ID")
aplusrole = os.environ.get("APLUSROLE")
netplusrole = os.environ.get("NETPLUSROLE")
secplusrole = os.environ.get("SECPLUSROLE")
quizrole = os.environ.get("QUIZROLE")

# print variables to confirmed they were passed in correctly
print(f"BOT_TOKEN: {bottoken}")
print(f"GUILD_ID: {guildid}")
print(f"LEADERBOARD_CHANNEL_ID: {leaderboardid}")
print(f"CHANNEL_ID: {channelid}")
print(f"APLUSROLE: {aplusrole}")
print(f"NETPLUSROLE: {netplusrole}")
print(f"SECPLUSROLE: {secplusrole}")
print(f"QUIZROLE: {quizrole}")

user_responses = {}  # Format: {message_id: {question_id: {user_id: answer}}}
valid_emojis = ["🇦", "🇧", "🇨", "🇩", "❓"]  # :regional_indicator_a:, :regional_indicator_b:, :regional_indicator_c:, :regional_indicator_d:, :question_mark:
emoji_to_answer = {
    "🇦": "A",
    "🇧": "B",
    "🇨": "C",
    "🇩": "D",
    "❓": "show_answer"
}

question_dict_mapping = {
    "cissp": cisspdict,
    "ceh": cehdict,
    "ccna": ccnadict,
    "aplus": aplusdict,
    "netplus": netplusdict,
    "linuxplus": linuxplusdict,
    "secplus": secplusdict,
    "quiz": quizdict
    # Add more prefixes and corresponding question dictionaries as needed
}

user_scores = {}

@client.event
async def on_reaction_add(reaction, user):
    if user == client.user or reaction.message.author != client.user:
        return

    if reaction.emoji in valid_emojis:
        message_id = reaction.message.id  # Get the message ID
        question_id = reaction.message.embeds[0].footer.text  # Get question ID from message footer
        prefix, question_number = question_id.split("_")  # Extract prefix and question number
        question_number = int(question_number)
        answer = emoji_to_answer[reaction.emoji]  # Convert the emoji to the corresponding answer option
        user_id = user.id  # Get the user's Discord ID
        global user_responses
        global user_scores

        # Check if the user has already responded to this question
        if message_id in user_responses and question_id in user_responses[message_id] and user_id in user_responses[message_id][question_id]:
            # User has already responded to this question, do not update their response or score
            await reaction.remove(user)
            return

        # Update the response for this question for all users
        if message_id not in user_responses:
            user_responses[message_id] = {}
        if question_id not in user_responses[message_id]:
            user_responses[message_id][question_id] = {}
        user_responses[message_id][question_id][user_id] = answer

        # Remove the user's reaction to prevent duplicate responses
        await reaction.remove(user)

        # Check if the answer is correct and update the user's score for the appropriate prefix
        question_dict = question_dict_mapping[prefix]
        question = question_dict[question_number]
        correct_answer = question["correctanswer"].lower()
        if answer == "show_answer":  # Check if the question mark emoji was selected
            if "reasoning" in question:
                await user.send(f"The correct answer is '{correct_answer}'\n\n**Reasoning**: {question['reasoning']}")
                return
            else:
                await user.send(f"The correct answer is '{correct_answer}'")
            return  # Stop processing the selected reaction if the question mark emoji was selected

        if answer:
            if user_id not in user_scores:
                user_scores[user_id] = {p: {"correct": 0, "incorrect": 0} for p in question_dict_mapping}  # Initialize the user's score if it doesn't exist
        # Convert the correct answer to lowercase
        if answer.lower() == correct_answer.lower():
            user_scores[user_id][prefix]["correct"] += 1  # Increment the user's score for this prefix
            await user.send(f"🎉 Congratulations, your answer '{answer}' is correct!")
        else:
            user_scores[user_id][prefix]["incorrect"] += 1  # Increment the user's score for this prefix
            await user.send(f"🤔 Your answer '{answer}' is incorrect. The correct answer is '{correct_answer}'.\n\n**Reasoning**: {question['reasoning']}")
            return


async def update_leaderboard():
    print("Updating leaderboard")
    await client.wait_until_ready()
    global user_scores
    if guildid is None or leaderboardid is None:
        print(f"missing required guild or leaderboard channel id")
        return
    guild = client.get_guild(int(guildid))
    leaderboard_channel = guild.get_channel(int(leaderboardid))

    # Compute the scores for each user and prefix
    prefix_scores = {p: {} for p in question_dict_mapping}
    for user_id, scores in user_scores.items():
        for prefix, score in scores.items():
            prefix_scores[prefix][user_id] = {"correct": score["correct"], "incorrect": score["incorrect"]}

    # Compute the overall scores for each user
    overall_scores = {}
    for user_id, scores in user_scores.items():
        overall_correct = sum([s["correct"] for s in scores.values()])
        overall_incorrect = sum([s["incorrect"] for s in scores.values()])
        overall_scores[user_id] = {"correct": overall_correct, "incorrect": overall_incorrect}

    # Sort the users by their overall score and number of incorrect answers
    sorted_users = sorted(overall_scores.items(), key=lambda x: (x[1]["correct"], x[1]["incorrect"]), reverse=True)

    # Create the leaderboard embed
    leaderboard_embed = Embed(title="Quiz Commands Leaderboard", color=0x006400)
    leaderboard_embed.set_footer(text="Note: The leaderboard is updated once per hour. \n To learn more about the quiz commands, run `/commands` in #bot-commands")

    # Add the overall leaderboard to the embed
    overall_leaderboard_desc = ""
    rank = 1
    for user_id, scores in sorted_users:
        member = guild.get_member(user_id)
        if member is not None:
            username = member.display_name
        else:
            username = f"Unknown User ({user_id})"
        correct = scores["correct"]
        incorrect = scores["incorrect"]
        overall_leaderboard_desc += f"{rank}. **{username}**: {correct} correct, {incorrect} incorrect\n"
        rank += 1
        if rank > 5:
            break
    leaderboard_embed.add_field(name="Overall", value=overall_leaderboard_desc, inline=False)

    # Add the leaderboard for each prefix to the embed
    for prefix, scores in prefix_scores.items():
        prefix_leaderboard_desc = ""
        sorted_users = sorted(scores.items(), key=lambda x: (x[1]["correct"], x[1]["incorrect"]), reverse=True)
        rank = 1
        for user_id, user_scores in sorted_users:
            member = guild.get_member(user_id)
            if member is not None:
                username = member.display_name
            else:
                username = f"Unknown User ({user_id})"
            correct = user_scores["correct"]
            incorrect = user_scores["incorrect"]
            prefix_leaderboard_desc += f"{rank}. **{username}**: {correct} correct, {incorrect} incorrect\n"
            rank += 1
            if rank > 5:
                break
        leaderboard_embed.add_field(name=prefix.upper(), value=prefix_leaderboard_desc, inline=False)

    # Update the leaderboard message in the leaderboard channel
    leaderboard_message = None
    async for message in leaderboard_channel.history():
        if message.author == client.user:
            leaderboard_message = message
            break
    if leaderboard_message is None:
        leaderboard_message = await leaderboard_channel.send(embed=leaderboard_embed)
    else:
        await leaderboard_message.edit(embed=leaderboard_embed)

    print("Leaderboard updated successfully")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        print(f"Unsupported command: {ctx.message.content}")

@client.hybrid_command(
    name="socials",
    description="Replies with the various bot social media accounts and websites.",
)
async def socials(ctx):
    try:
        response = f"**Website**: https://cybersentinels.org\n\n**GitHub**: https://github.com/cybersentinels"
        await ctx.send(response)
    except Exception as e:
        await ctx.send(f"Error: {e}. An unexpected error occurred.")

@client.hybrid_command(name="commands", description="Describes the available commands.")
async def commands(ctx):
    try:
        response = """## Commands Available:
*Command prefix: '!', '/'*

### Quiz and Scenario Commands
*Multiple-choice questions are dynamically weighted similar to the real exams based on if they are answered correctly or incorrectly*
- **Aplus**: Replies with CompTIA's A+ related prompt.
- **Bluescenario**: Replies with a blue team scenario.
- **CCNA**: Replies with Cisco's CCNA multiple choice prompt.
- **CEH**: Replies with EC-Council's CEH multiple choice prompt.
- **CISSP**: Replies with ISC2's CISSP multiple choice prompt.
- **Linuxplus**: Replies with CompTIA's Linux+ multiple choice prompt.
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
        response, question_id = handle_ccna(user_responses)
        embed = Embed(description=response)
        embed.set_footer(text=question_id)
        message = await ctx.send(embed=embed)
        # Add reactions for each answer choice
        for emoji in valid_emojis:
            await message.add_reaction(emoji)
    except Exception as e:
        print({e})
        await ctx.send(f"Error: {e}. An unexpected error occurred.")

@client.hybrid_command(
    name="cissp",
    description="Replies with Replies with an ISC2's CISSP multiple choice prompt.",
)
async def cissp(ctx):
    try:
        response, question_id = handle_cissp(user_responses)
        embed = Embed(description=response)
        embed.set_footer(text=question_id)
        message = await ctx.send(embed=embed)
        # Add reactions for each answer choice
        for emoji in valid_emojis:
            await message.add_reaction(emoji)
    except Exception as e:
        print({e})
        await ctx.send(f"Error: {e}. An unexpected error occurred.")

@client.hybrid_command(
    name="linuxplus",
    description="Replies with Replies with a Comptia's Linux+ multiple choice prompt.",
)
async def linuxplus(ctx):
    try:
        response, question_id = handle_linuxplus(user_responses)
        embed = Embed(description=response)
        embed.set_footer(text=question_id)
        message = await ctx.send(embed=embed)
        # Add reactions for each answer choice
        for emoji in valid_emojis:
            await message.add_reaction(emoji)
    except Exception as e:
        print({e})
        await ctx.send(f"Error: {e}. An unexpected error occurred.")

@client.hybrid_command(
    name="ceh",
    description="Replies with Replies with an EC-Council's CEH multiple choice prompt.",
)
async def ceh(ctx):
    try:
        response, question_id = handle_ceh(user_responses)
        embed = Embed(description=response)
        embed.set_footer(text=question_id)
        message = await ctx.send(embed=embed)
        # Add reactions for each answer choice
        for emoji in valid_emojis:
            await message.add_reaction(emoji)
    except Exception as e:
        print({e})
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

# Define the leaderboard update task
@tasks.loop(hours=1, minutes=0)
async def update_leaderboard_task():
    await update_leaderboard()

# Define the random quiz task to run at 12:00pm every day
@tasks.loop(hours=24, minutes=0)
async def send_message_and_random():
    print("starting send random message")
    try:
        await client.wait_until_ready()
        if guildid is None or channelid is None or secplusrole is None or aplusrole is None or netplusrole is None or quizrole is None:
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

# Define the on_ready event handler
@client.event
async def on_ready():
    print(f"Starting Scheduled Task Loops")
    send_message_and_random.start()
    update_leaderboard_task.start()
    print(f"Finished Starting Tasks")
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

    if bot_username == "Cyber Sentinel":
        activity = Activity(
            type=ActivityType.streaming,
            name="cybersentinels.org",
            url="https://cybersentinels.org/",
            state="Creating Content",
            details="Creating Content for the Cyber Sentinels",
            assets={
                "large_image": "cybersentinels_logo",
                "large_text": "Cyber Sentinels Logo",
                "small_image": "cybersentinels_logo",
                "small_text": "Cyber Sentinels Logo",
            },
            buttons=["Try", "Harder"],
            emoji=None,
        )
        await client.change_presence(activity=activity, status=Status.online)
    else:
        activity = Activity(
            type=ActivityType.streaming,
            name="cybersentinels.org",
            url="https://cybersentinels.org/",
            state="Creating Content",
            details="Creating Content for the Cyber Sentinels",
            emoji=None,
        )
        await client.change_presence(activity=activity, status=Status.online)
        
    # Start Task Loops
    # try:
    # except Exception as e:
    #     traceback.print_exc()
    #     print(f"Error starting scheduled tasks: {e}")

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

client.run(bottoken)

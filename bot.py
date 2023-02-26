import random
import discord
from discord.ext import commands
from discord import app_commands
from discord.ext import commands, tasks
import ipaddress
import os

from features.bluescenarios.bluescenarios import bluescenarios
from features.redscenarios.redscenarios import redscenarios
from features.quiz.quizdict import quizdict
import features.aplus.handle_aplus as handle_aplus
from features.netplus.netplusdict import netplusdict
from features.secplus.secplusdict import secplusdict

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
        scenarios = bluescenarios + redscenarios
        scenario = random.choice(scenarios)
        prompt = scenario["prompt"]
        if "ways_to_prevent" in scenario:
            prevent = "\n".join(scenario["ways_to_prevent"])
            respond = "\n".join(scenario["how_to_respond"])
            response = f"**Here's a Blue Team Scenario for you**:\n\nPrompt: {prompt}\n\n**Ways to prevent**: ||{prevent}||\n\n**How to respond**: ||{respond}||"
        else:
            solution = scenario["solution"]
            response = f"**Here's a Red Team Scenario for you**:\n\n**Prompt**: {prompt}\n\n**Solution**: ||{solution}||"
        await ctx.send(response)
    except Exception as e:
        print(f"An error occurred while running the 'scenario' command: {e}")
        await ctx.send("Sorry, an error occurred while running that command.")


@client.hybrid_command()
async def bluescenario(ctx):
    try:
        scenario = random.choice(bluescenarios)
        prompt = scenario["prompt"]
        prevent = "\n".join(scenario["ways_to_prevent"])
        respond = "\n".join(scenario["how_to_respond"])
        response = f"**Here's a Blue Team Scenario for you**:\n\n**Prompt**: {prompt}\n\n**Ways to prevent**: ||{prevent}||\n\n**How to respond**: ||{respond}||"
        await ctx.send(response)
    except KeyError as e:
        await ctx.send(f"Error: {e}. This scenario is missing a required field.")
    except Exception as e:
        await ctx.send(f"Error: {e}. An unexpected error occurred.")


@client.hybrid_command()
async def redscenario(ctx):
    try:
        scenario = random.choice(redscenarios)
        prompt = scenario["prompt"]
        solution = scenario["solution"]
        response = f"**Here's a Red Team Scenario for you**:\n\n**Prompt**: {prompt}\n\n**Solution**: ||{solution}||"
        await ctx.send(response)
    except KeyError as e:
        await ctx.send(f"Error: {e}. This scenario is missing a required field.")
    except Exception as e:
        await ctx.send(f"Error: {e}. An unexpected error occurred.")


@client.hybrid_command()
async def quiz(ctx):
    try:
        question = random.choice(quizdict)
        prompt = question["question"]
        answer = question["answer"]
        response = f"**Here's a security question for you**:\n\n**Prompt**: {prompt}\n\n**Answer**: ||{answer}||"
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
        question = random.choice(netplusdict)
        prompt = question["question"]
        answer = question["answer"]
        response = f"**Here's a practice Network+ question for you**:\n\n**Prompt**: {prompt}\n\n**Answer**: ||{answer}||"
        await ctx.send(response)
    except Exception as e:
        await ctx.send(f"Error: {e}. An unexpected error occurred.")


@client.hybrid_command()
async def secplus(ctx):
    try:
        question = random.choice(secplusdict)
        prompt = question["question"]
        answer = question["answer"]
        response = f"**Here's a practice Security+ question for you**:\n\n**Prompt**: {prompt}\n\n**Answer**: ||{answer}||"
        await ctx.send(response)
    except Exception as e:
        await ctx.send(f"Error: {e}. An unexpected error occurred.")

@client.hybrid_command()
async def subnet(ctx, ip: str, mask: str):
    try:
        network = ipaddress.ip_network(f"{ip}/{mask}", strict=False)
        net_addr = str(network.network_address)
        broadcast_addr = str(network.broadcast_address)
        usable_range = f"{str(network[1])} - {str(network[-2])}"
        host_count = network.num_addresses
        response = f"**Here are the details for subnet {network}**: \n\n**Network address**: {net_addr}\n**Broadcast address**: {broadcast_addr}\n**Usable IP range**: {usable_range}\n**Number of hosts**: {host_count}"
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

        # Get a random question from the quiz dictionary
        question = random.choice(quizdict)
        prompt = question["question"]
        answer = question["answer"]
        response = f"**Here's a security question for you**:\n\n**Prompt**: {prompt}\n\n**Answer**: ||{answer}||"
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

        # Get a random question from the A+ dictionary
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

        # Get a random question from the Network+ dictionary
        question = random.choice(netplusdict)
        prompt = question["question"]
        answer = question["answer"]
        response = f"**Here's a practice Network+ question for you**:\n\n**Prompt**: {prompt}\n\n**Answer**: ||{answer}||"
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

        # Get a random question from the Security+ dictionary
        question = random.choice(secplusdict)
        prompt = question["question"]
        answer = question["answer"]
        response = f"**Here's a practice Security+ question for you**:\n\n**Prompt**: {prompt}\n\n**Answer**: ||{answer}||"
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

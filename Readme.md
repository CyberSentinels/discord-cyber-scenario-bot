# Discord Cyber Scenario, Quiz, And Cyber Awareness Training Bot

[![Docker Image CI](https://github.com/simeononsecurity/discord-cyber-scenario-bot/actions/workflows/docker-image.yml/badge.svg)](https://github.com/simeononsecurity/discord-cyber-scenario-bot/actions/workflows/docker-image.yml)

This bot may be useful in a cybersecurity training or awareness program, where users can be exposed to various cybersecurity scenarios and learn how to prevent or respond to them. By using a Discord bot, the scenarios can be easily shared with users in a server environment, and the bot can be customized to include additional commands or functionality as needed. Additionally, the bot can be run in a Docker container, making it easy to deploy and manage in various environments.

## Commands Available:
*Command prefix: '!', '/'*

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
- **Socials**: Replies with the various bot social media accounts and websites.

## How to run:
### Python:
Assuming you are using a Unix-based system, open a terminal and navigate to the directory where the bot.py script is located. Then, run the following command:
```bash
export BOT_TOKEN="INSERT YOUR BOT TOKEN HERE"
export GUILD_ID="INSERT YOUR GUILD ID HERE (only needed for timed quizes)"
export CHANNEL_ID="INSERT YOUR CHANNEL ID HERE (only needed for timed quizes)"
export APLUSROLE="INSERT YOUR A+ ROLE ID HERE (only needed for timed quizes)"
export NETPLUSROLE="INSERT YOUR Network+ ROLE ID HERE (only needed for timed quizes)"
export SECPLUSROLE="INSERT YOUR Security+ ROLE ID HERE (only needed for timed quizes)"
export QUIZROLE="INSERT YOUR QUIZ ROLE ID HERE (only needed for timed quizes)"
python bot.py
```
Note that if you are using a Windows-based system, you'll need to use a slightly different command to set the environment variable. Here's an example command that should work on Windows:
```powershell
set BOT_TOKEN="INSERT YOUR BOT TOKEN HERE"
set GUILD_ID="INSERT YOUR GUILD ID HERE (only needed for timed quizes)"
set CHANNEL_ID="INSERT YOUR CHANNEL ID HERE (only needed for timed quizes)"
set APLUSROLE="INSERT YOUR A+ ROLE ID HERE (only needed for timed quizes)"
set NETPLUSROLE="INSERT YOUR Network+ ROLE ID HERE (only needed for timed quizes)"
set SECPLUSROLE="INSERT YOUR Security+ ROLE ID HERE (only needed for timed quizes)"
set QUIZROLE="INSERT YOUR QUIZ ROLE ID HERE (only needed for timed quizes)"
python bot.py
```
### Docker:
When running the Docker container, you can pass in the BOT_TOKEN environment variable using the -e flag as follows:

```bash
docker run -e BOT_TOKEN="INSERT YOUR BOT TOKEN HERE" -it --rm simeononsecurity/discord-cyber-scenario-bot:latest
```

To run the bot in the background:
```bash
docker run -td --name scenario-bot -e BOT_TOKEN="INSERT YOUR BOT TOKEN HERE" simeononsecurity/discord-cyber-scenario-bot:latest
```

To run the bot in the background with all scheduled prompts and roles:
```bash
docker run -td --name scenario-bot \
-e BOT_TOKEN="INSERT YOUR BOT TOKEN HERE" \
-e GUILD_ID="INSERT YOUR GUILD ID HERE" \
-e CHANNEL_ID="INSERT YOUR CHANNEL ID HERE" \
-e APLUSROLE="INSERT YOUR A+ ROLE ID HERE" \
-e NETPLUSROLE="INSERT YOUR NET+ ROLE ID HERE" \
-e SECPLUSROLE="INSERT YOUR SEC+ ROLE ID HERE" \
-e QUIZROLE="INSERT YOUR QUIZ ROLE ID HERE" \
simeononsecurity/discord-cyber-scenario-bot:latest
```

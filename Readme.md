# Discord Cyber Scenario, Quiz, And Cyber Awareness Training Bot

[![Docker Image CI](https://github.com/simeononsecurity/discord-cyber-scenario-bot/actions/workflows/docker-image.yml/badge.svg)](https://github.com/simeononsecurity/discord-cyber-scenario-bot/actions/workflows/docker-image.yml)

This bot may be useful in a cybersecurity training or awareness program, where users can be exposed to various cybersecurity scenarios and learn how to prevent or respond to them. By using a Discord bot, the scenarios can be easily shared with users in a server environment, and the bot can be customized to include additional commands or functionality as needed. Additionally, the bot can be run in a Docker container, making it easy to deploy and manage in various environments.

## Commands Available:
*Command prefix: '!', '/'*

- **Quiz**: Replies with a random Cyber Security Awareness Question.

- **Scenario**: Replies with either a red team or blue team scenario. 

- **Bluescenario**: Replies with a blue team scenario. 

- **Redscenario**: Replies with a redteam scenario.

- **Aplus**: Replies with CompTIA's A+ related prompt.

- **Netplus**: Replies with CompTIA's Network+ related prompt.

- **Secplus**: Replies with CompTIA's Security+ related prompt.

- **Commands**: Replies with this message.

- **Socials**: replies with the various bot social media accounts and websites.

## How to run:
### Python:
Assuming you are using a Unix-based system, open a terminal and navigate to the directory where the bot.py script is located. Then, run the following command:
```bash
export BOT_TOKEN="INSERT YOUR BOT TOKEN HERE"
python bot.py
```
Note that if you are using a Windows-based system, you'll need to use a slightly different command to set the environment variable. Here's an example command that should work on Windows:
```powershell
set BOT_TOKEN="INSERT YOUR BOT TOKEN HERE"
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

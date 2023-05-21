
# CyberScenarioBot

Discord Cyber Scenario, Quiz, And Cyber Awareness Training Bot.

You can skip to [🚀 Quick Start](#quick-start) to add `CyberScenarioBot` to your server now.

[![Docker Image CI](https://github.com/simeononsecurity/discord-cyber-scenario-bot/actions/workflows/docker-image.yml/badge.svg)](https://github.com/simeononsecurity/discord-cyber-scenario-bot/actions/workflows/docker-image.yml)

## Table of Contents

- [CyberScenarioBot](#cyberscenariobot)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [🚀 Quick Start](#🚀-quick-start)
  - [Features](#features)
    - [📝 **Quizzes and Scenarios**](#📝-quizzes-and-scenarios)
    - [💯🎯 **Leaderboard**](#💯🎯-leaderboard)
    - [🛠️ **Tool Commands**](#🛠️-tool-commands)
    - [ℹ️ **Informational Commands**](#ℹ️-informational-commands)
    - [⚙️ **Easy Setup**](#⚙️-easy-setup)
  - [Upcoming Features](#upcoming-features)
  - [Usage](#usage)
  - [Examples](#examples)
    - [Example 1: Command A](#example-1-command-a)
    - [Example 2: Command B](#example-2-command-b)
  - [Issues](#issues)
  - [Contributing](#contributing)
  - [License](#license)

## Introduction

This bot may be useful in a cybersecurity training or awareness program, where users can be exposed to various cybersecurity scenarios and learn how to prevent or respond to them. By using a Discord bot, the scenarios can be easily shared with users in a server environment, and the bot can be customized to include additional commands or functionality as needed. Additionally, the bot can be run in a Docker container, making it easy to deploy and manage in various environments.

[See the bot in action](https://discord.io/cybersentinels)

![](https://discord.io/cybersentinels/badge)

## 🚀 Quick Start

1. TODO Show how someone can add this bot to their server, include explanation of the ENV VARIABLE opt-in
2. ...

## Features

### 📝 **Quiz and Scenario Commands**
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

### 💯🎯 **Leaderboard Commands**
*Multiple-choice questions are dynamically weighted similar to the real exams based on if they are answered correctly or incorrectly*

- *Track your progress over time and see how you compare against others in your server*
- *See scores for each quiz category as well as overall*

### 🛠️ **Tool Commands**
- **Dns**: Takes in a `domain name` and returns A, AAAA, NS, TXT, etc. records.
- **Hash**: Takes in `1 of 4 supported algos` and a `string` and outputs a corresponding hash.
- **Ping**: Takes in an `IP address` and returns with a success message and average latency or a failure message.
- **Phonelookup**: Takes in a `phone number` and outputs the carrier and location.
- **Shodanip**: Takes in an `IP address` and outputs useful information from https://internetdb.shodan.io/.
- **Subnet**: Takes in an `IP address` and a `Subnet Mask` and outputs the Range, Usable IPs, Gateway Address, Broadcast Address, and Number of Supported Hosts.
- **Whois**: Takes in a `domain name` and outputs domain whois information.

### ℹ️ **Informational Commands**
- **Commands**: Replies with this message.
- **Socials**: Replies with the various bot social media accounts and websites.

### ⚙️ **Easy Setup**
- *See [🚀 Quick Start](#🚀-quick-start)*

## Upcoming Features

- Describe the features that are currently being developed or planned for future releases. This helps users understand the project's roadmap and future enhancements.

## Usage

Explain how to use the project. Provide examples of common use cases or workflows to guide users. Include any important command line options or configuration details.

## Examples

Provide concrete examples of how to use the project's features or functionalities. Include code snippets, configuration files, or any relevant resources to assist users in understanding and implementing the project effectively.

### Example 1: Command A

To execute command A, use the following command:

`project commandA --option1 value1 --option2 value2`

Explain what this command does and provide additional details if necessary.

### Example 2: Command B

For executing command B with a specific file, use the following command:

`project commandB path/to/file`

Describe the purpose of this command and any required parameters.

## Issues

If users encounter any issues or have suggestions for improvements, they can open a GitHub issue to report them. Encourage users to provide detailed information about the problem and steps to reproduce it.

To open an issue, follow these steps:

1. Go to the Issues tab on the project's GitHub repository: [Issues](https://github.com/username/project/issues)
2. Click on the "New Issue" button.
3. Provide a descriptive title and a clear description of the issue.
4. Include any relevant logs, screenshots, or code snippets to help with troubleshooting.
5. Submit the issue and await further communication from the project maintainers.

## Contributing

TODO Show how to get necessary ENV Variables here and how to set up with own discord server. Explain how others can contribute to the project. Provide guidelines for submitting pull requests, reporting bugs, or suggesting new features. Include information about the project's coding style, testing procedures, and any other relevant information.

## License

Specify the project's license and provide a link to the full license text if applicable.

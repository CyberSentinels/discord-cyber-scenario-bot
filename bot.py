import random
import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents)

bottoken = os.environ.get('BOT_TOKEN')

scenarios = [
    "Insider Threat: An employee with authorized access to an organization's network uses their access to steal or leak sensitive information, or to cause disruption to the organization's operations. What are some ways to prevent insider threats, and how can organizations detect and respond to them?",
    "Password Reuse: An attacker gains access to an employee's password through a third-party breach, and uses the same password to gain access to the organization's network. What are some ways to prevent password reuse, and how can organizations ensure that their employees are using strong and unique passwords?",
    "Advanced Persistent Threat: An attacker uses sophisticated techniques, such as malware, social engineering, and targeted attacks, to gain persistent access to an organization's network over an extended period of time. What are some ways to prevent advanced persistent threats, and how can organizations detect and respond to them?",
    "Supply Chain Attack: An attacker compromises a vendor or supplier that provides services or products to an organization, in order to gain access to the organization's network. What are some ways to prevent supply chain attacks, and how can organizations ensure that their vendors and suppliers are following best security practices?",
    "Ransomware: An attacker uses malware to encrypt an organization's data or lock its devices, and demands a ransom in exchange for restoring access. What are some ways to prevent ransomware attacks, and how can organizations respond when they happen?",
    "Wireless Network Compromise: An attacker gains unauthorized access to an organization's wireless network, allowing them to eavesdrop on network traffic, steal sensitive information, or launch attacks on other devices on the network. What are some ways to prevent wireless network compromises, and how can organizations detect and respond to them?",
    "Voice Phishing (Vishing): An attacker uses social engineering techniques to trick an employee into revealing sensitive information over the phone. What are some ways to prevent voice phishing attacks, and how can organizations train their employees to recognize and respond to them?",
    "Insider Trading: An employee with access to sensitive financial information uses it to profit in the stock market, causing harm to the organization's reputation and financial wellbeing. What are some ways to prevent insider trading, and how can organizations ensure that their employees are following best ethical practices?",
    "IoT Device Compromise: An attacker gains unauthorized access to an organization's Internet of Things (IoT) devices, such as smart thermostats or security cameras, allowing them to steal sensitive information or launch attacks on other devices on the network. What are some ways to prevent IoT device compromises, and how can organizations detect and respond to them?",
    "Email Spoofing: An attacker sends an email that appears to be from a trusted source, in order to trick the recipient into revealing sensitive information or taking a malicious action. What are some ways to prevent email spoofing, and how can organizations train their employees to recognize and respond to it?",
    "Distributed Denial of Service (DDoS) Attack: An attacker uses a network of compromised devices to flood an organization's network with traffic or requests, causing it to become unavailable to legitimate users. What are some ways to prevent DDoS attacks, and how can organizations mitigate the damage when they occur?",
    "Malware Infection: An attacker installs malware on an organization's network that steals sensitive information, monitors network activity, or disrupts the organization's operations. What are some ways to prevent malware infections, and how can organizations detect and respond to them?",
    "Insider Sabotage: An employee with authorized access to an organization's network uses their access to cause intentional harm to the organization's operations, reputation, or financial wellbeing. What are some ways to prevent insider sabotage, and how can organizations detect and respond to it?",
    "Social Media Hijacking: An attacker gains access to an organization's social media accounts and posts unauthorized content, damaging the organization's reputation. What are some ways to prevent social media hijacking, and how can organizations respond when it happens?",
    "Third-Party Breach: An organization's vendor or supplier experiences a data breach that exposes sensitive information about the organization's customers or employees. What are some ways to prevent third-party breaches, and how can organizations minimize the damage when they occur?",
    "Malware Infection: An organization's network becomes infected with malware that causes data loss, system downtime, or other disruptions. What are some ways to prevent malware infections, and how can organizations detect and respond to them?",
    "Insider Threat: An employee with legitimate access to an organization's network misuses their privileges to steal data, cause damage, or engage in other malicious activities. What are some ways to prevent insider threats, and how can organizations monitor for and respond to them?",
    "Physical Theft: An attacker steals physical devices such as laptops, smartphones, or USB drives that contain sensitive information. What are some ways to prevent physical theft, and how can organizations protect the data that is stored on these devices?",
    "DDoS Attack: An attacker floods an organization's website with traffic, causing it to become unavailable to legitimate users. What are some ways to prevent DDoS attacks, and how can organizations respond when they happen?",
    "Password Attack: An attacker gains access to an organization's network by guessing or cracking weak passwords. What are some ways to prevent password attacks, and how can organizations encourage their employees to use strong passwords?",
    "Insider Trading: An employee uses confidential information about an organization's financial performance to make illegal trades on the stock market. What are some ways to prevent insider trading, and how can organizations monitor for and respond to it?",
    "Physical Sabotage: An attacker damages an organization's physical infrastructure, such as servers, routers, or power supplies, causing disruption to its operations. What are some ways to prevent physical sabotage, and how can organizations protect their critical infrastructure?",
    "Cyber Espionage: A nation-state or other sophisticated attacker targets an organization's network to steal intellectual property or other sensitive information. What are some ways to prevent cyber espionage, and how can organizations detect and respond to these types of attacks?",
    "Software Vulnerability: An attacker exploits a known vulnerability in a software application to gain unauthorized access to an organization's network. What are some ways to prevent software vulnerabilities, and how can organizations keep their software up-to-date?",
    "Spear Phishing Attack: An attacker sends a targeted phishing email to an employee that appears to be from a trusted source, in order to steal sensitive information. What are some ways to prevent spear phishing attacks, and how can organizations train their employees to recognize and respond to them?",
    "Cloud Security Breach: An attacker gains unauthorized access to an organization's cloud storage, compromising sensitive information. What are some ways to prevent cloud security breaches, and how can organizations ensure that their cloud providers are following best security practices?",
    "Brute Force Attack: An attacker uses automated tools to guess a user's password or encryption key, in order to gain unauthorized access to an organization's network. What are some ways to prevent brute force attacks, and how can organizations detect and respond to them?",
    "Website Defacement: An attacker replaces an organization's website content with unauthorized content, causing reputational damage. What are some ways to prevent website defacement, and how can organizations recover from this type of attack?",
    "Man-in-the-Middle Attack: An attacker intercepts and modifies network traffic between two parties, in order to steal or modify information. What are some ways to prevent man-in-the-middle attacks, and how can organizations detect and respond to them?",
    "Data Loss: An organization accidentally or intentionally deletes or destroys sensitive data, causing significant harm to the organization or its customers. What are some ways to prevent data loss, and how can organizations ensure that their data backups are secure?",
    "Physical Destruction: An attacker physically destroys an organization's equipment, such as servers or routers, causing disruption to its operations. What are some ways to prevent physical destruction, and how can organizations respond when it happens?",
    "SQL Injection: An attacker uses a vulnerability in a web application's SQL database to extract sensitive information. What are some ways to prevent SQL injection attacks, and how can organizations detect and respond to them?",
    "Denial of Service Attack: An attacker floods an organization's network with traffic or requests, causing it to become unavailable to legitimate users. What are some ways to prevent denial of service attacks, and how can organizations mitigate the damage when they occur?",
    "Cyber Extortion: An attacker threatens to release sensitive information or disrupt an organization's operations unless a ransom is paid. What are some ways to prevent cyber extortion, and how can organizations respond when it happens?",
    "Cryptojacking: An attacker installs malware on an organization's network that uses its resources to mine cryptocurrency. What are some ways to prevent cryptojacking, and how can organizations detect and respond to this type of attack?",
    "Social Media Impersonation: An attacker creates fake social media profiles that impersonate an organization or its employees, in order to steal sensitive information or spread disinformation. What are some ways to prevent social media impersonation, and how can organizations respond when it happens?",
    "Watering Hole Attack: An attacker compromises a legitimate website that is frequently visited by an organization's employees, in order to infect their devices with malware. What are some ways to prevent watering hole attacks, and how can organizations detect and respond to them?",
    "Physical Surveillance: An attacker uses physical surveillance techniques, such as hidden cameras or audio recorders, to gather sensitive information about an organization. What are some ways to prevent physical surveillance, and how can organizations detect and respond to it?"
    ]

@client.command()
async def scenario(ctx):
    scenario = random.choice(scenarios)
    response = f"Here's a scenario for you:\n\n{scenario}"
    await ctx.send(response)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    print('Bot is ready.')

async def on_message(message):
    if message.content.startswith('!scenario') or message.content.startswith('/scenario'):
        scenario = random.choice(scenarios)
        response = f"Here's a scenario for you:\n\n{scenario}"
        await channel.send(response)

client.run(bottoken)
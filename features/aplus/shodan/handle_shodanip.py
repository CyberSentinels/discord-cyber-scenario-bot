import re
import json
import discord
import requests
from discord.ext import commands

def is_valid_ip(ip):
    m = re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", ip)
    return bool(m) and all(map(lambda n: 0 <= int(n) <= 255, m.groups()))

async def handle_shodanip(ip):
  if is_valid_ip(ip):
    shodan_result = requests.get("https://internetdb.shodan.io/" + ip)
    shodan_json = json.loads(shodan_result.content)

    if("detail" in shodan_json and shodan_json["detail"] == "No information available"):
      return ("Error: No information availible for this IP address.")
    else:
      DESCRIPTION="Shodan InternetDB Results For " + ip
      embed=discord.Embed(title=DESCRIPTION, color=0xdf0000)
      embed.add_field(name="Hostnames", value=shodan_json["hostnames"], inline=False)
      embed.add_field(name="Open Ports", value=shodan_json["ports"], inline=False)
      embed.add_field(name="Tags", value=shodan_json["tags"], inline=False)
      embed.add_field(name="CPEs", value=shodan_json["cpes"], inline=False)
      embed.add_field(name="Vulns", value=shodan_json["vulns"], inline=False)
      return embed
  else:
    return ("Error: Invalid IP Address.")
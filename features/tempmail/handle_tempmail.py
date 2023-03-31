import discord
from discord.ext import commands
from tempmail2 import TempMail

tempmail = TempMail()

async def handle_tempmail():
    # get a new temporary email address
    email_address = tempmail.get_email_address()

    # get the URL to the inbox for the email address
    inbox_url = tempmail.get_inbox_url(email_address)

    # create an embed with the email address and inbox link
    embed = discord.Embed(title="Temporary Email", description="Use this email address to receive temporary emails:")
    embed.add_field(name="Email Address", value=email_address, inline=False)
    embed.add_field(name="Inbox URL", value=f"[Click Here]({inbox_url})", inline=False)
    embed.set_footer(text="This email will be deleted after some time.")

    # send the embed to the user who requested it
    return embed
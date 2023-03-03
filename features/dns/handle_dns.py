import discord
import dns.resolver

async def handle_dns(domain):
    query = domain
    embed = discord.Embed(title=f'DNS Records for {query}')
    try:
        response = dns.resolver.query(query, 'A')
        for answer in response:
            embed.add_field(name='A Record', value=answer.address)
    except dns.resolver.NXDOMAIN:
        embed.add_field(name='Error', value=f'Unable to resolve {query}')

    try:
        response = dns.resolver.query(query, 'AAAA')
        for answer in response:
            embed.add_field(name='AAAA Record', value=answer.address)
    except dns.resolver.NoAnswer:
        pass

    try:
        response = dns.resolver.query(query, 'TXT')
        for answer in response:
            embed.add_field(name='TXT Record', value=answer.to_text())
    except dns.resolver.NoAnswer:
        pass

    try:
        response = dns.resolver.query(query, 'NS')
        for answer in response:
            embed.add_field(name='NS Record', value=answer.to_text())
    except dns.resolver.NoAnswer:
        pass

    try:
        response = dns.resolver.query(query, 'CNAME')
        for answer in response:
            embed.add_field(name='CNAME Record', value=answer.to_text())
    except dns.resolver.NoAnswer:
        pass

    try:
        response = dns.resolver.query('_dmarc.' + query, 'TXT')
        for answer in response:
            embed.add_field(name='DMARC Record', value=answer.to_text())
    except dns.resolver.NoAnswer:
        pass

    return embed
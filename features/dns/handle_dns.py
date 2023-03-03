import discord
import dns.resolver

async def handle_dns(domain):
    resolver = dns.resolver.Resolver()
    resolver.lport = 0
    query = domain
    
    a_records = []
    aaaa_records = []
    txt_records = []
    ns_records = []
    cname_records = []
    dmarc_records = []

    try:
        response = dns.resolver.query(query, 'A')
        for answer in response:
            a_records.append(answer.address)
    except dns.resolver.NXDOMAIN:
        a_records.append("No A records found")

    try:
        response = dns.resolver.query(query, 'AAAA')
        for answer in response:
            aaaa_records.append(answer.address)
    except dns.resolver.NoAnswer:
        aaaa_records.append("No AAAA records found")

    try:
        response = dns.resolver.query(query, 'TXT')
        for answer in response:
            txt_records.append(answer.to_text())
    except dns.resolver.NoAnswer:
        txt_records.append("No TXT records found")

    try:
        response = dns.resolver.query(query, 'NS')
        for answer in response:
            ns_records.append(answer.to_text())
    except dns.resolver.NoAnswer:
        ns_records.append("No NS records found")

    try:
        response = dns.resolver.query(query, 'CNAME')
        for answer in response:
            cname_records.append(answer.to_text())
    except dns.resolver.NoAnswer:
        cname_records.append("No CNAME records found")

    try:
        response = dns.resolver.query('_dmarc.' + query, 'TXT')
        for answer in response:
            dmarc_records.append(answer.to_text())
    except dns.resolver.NoAnswer:
        dmarc_records.append("No DMARC records found")

    embed = discord.Embed(title=f"DNS Lookup - Results for {query}")
    if a_records:
        embed.add_field(name="A Records", value="\n".join(a_records), inline=False)
    if aaaa_records:
        embed.add_field(name="AAAA Records", value="\n".join(aaaa_records), inline=False)
    if ns_records:
        embed.add_field(name="NS Records", value="\n".join(ns_records), inline=False)
    if txt_records:
        embed.add_field(name="TXT Records", value="\n".join(txt_records), inline=False)
    if cname_records:
        embed.add_field(name="CNAME Records", value="\n".join(cname_records), inline=False)
    if dmarc_records:
        embed.add_field(name="DMARC Records", value="\n".join(dmarc_records), inline=False)

    return embed
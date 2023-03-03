import whois

async def handle_whois(domain: str):
    # Get the WHOIS information for the specified domain
    try:
        w = whois.whois(domain)
    except Exception as e:
        return f"Error: {e}. Unable to retrieve WHOIS information for {domain}."

    # Parse the WHOIS information and return it
    registrant = w.get("registrant_name") or w.get("name") or "N/A"
    registrar = w.get("registrar") or "N/A"
    nameservers = ", ".join(w.get("name_servers") or ["N/A"])
    return f"Registrant: {registrant}\nRegistrar: {registrar}\nName servers: {nameservers}"

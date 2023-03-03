import ipaddress

async def handle_subnet(ip: str, mask: str):
    network = ipaddress.ip_network(f"{ip}/{mask}", strict=False)
    net_addr = str(network.network_address)
    broadcast_addr = str(network.broadcast_address)
    usable_range = f"{str(network[1])} - {str(network[-2])}"
    host_count = network.num_addresses
    response = f"**Here are the details for subnet {network}**: \n\n**Network address**: {net_addr}\n**Broadcast address**: {broadcast_addr}\n**Usable IP range**: {usable_range}\n**Number of hosts**: {host_count}"
    return response
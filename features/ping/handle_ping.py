import asyncio
import platform
import subprocess

async def handle_ping(ip):
    # Determine the platform-specific arguments for the ping command
    if platform.system().lower() == "windows":
        args = ["ping", "-n", "1", "-w", "1000", ip]
    else:
        args = ["ping", "-c", "1", "-W", "1", ip]

    # Execute the ping command and capture the output
    proc = await asyncio.create_subprocess_exec(
        *args, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    output = stdout.decode().strip() or stderr.decode().strip()

    # Determine whether the ping was successful
    if "time=" in output.lower():
        latency = output.split("time=")[1].split()[0]
        return f"Ping successful. Average latency: {latency} ms."
    else:
        return "Ping failed."
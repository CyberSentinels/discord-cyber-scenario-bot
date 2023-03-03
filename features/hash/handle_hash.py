import hashlib

async def handle_hash(message, algorithm):
    # Hash the message using the specified algorithm
    if algorithm == "md5":
        hashed = hashlib.md5(message.encode()).hexdigest()
    elif algorithm == "sha1":
        hashed = hashlib.sha1(message.encode()).hexdigest()
    elif algorithm == "sha256":
        hashed = hashlib.sha256(message.encode()).hexdigest()
    elif algorithm == "sha512":
        hashed = hashlib.sha512(message.encode()).hexdigest()
    else:
        return f"Invalid algorithm. Supported algorithms are 'md5', 'sha1', 'sha256', and 'sha512'."

    # Return the hashed message
    return f"Hashed message: {hashed}"

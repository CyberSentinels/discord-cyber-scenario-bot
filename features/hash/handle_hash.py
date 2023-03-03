from cryptography.hazmat.primitives import hashes

async def handle_hash(message, algorithm):
    # Hash the message using the specified algorithm
    if algorithm == "md5":
        digest = hashes.Hash(hashes.MD5())
    elif algorithm == "sha1":
        digest = hashes.Hash(hashes.SHA1())
    elif algorithm == "sha256":
        digest = hashes.Hash(hashes.SHA256())
    elif algorithm == "sha512":
        digest = hashes.Hash(hashes.SHA512())
    else:
        return f"Invalid algorithm. Supported algorithms are 'md5', 'sha1', 'sha256', and 'sha512'."

    digest.update(message.encode())
    hashed = digest.finalize()

    # Return the hashed message
    return f"Hashed message: {hashed.hex()}"
from pathlib import Path

# Load binary key from file
key = Path("../../assets/STATIC_KEY_20MB").read_bytes()

# Generate python file from key
with open("key.py", "w") as f:
    # encode first 10MB key as hex string
    encoded_key = key[:10 * 1024 * 1024].hex()
    f.write("def get_key():\n")
    f.write(f'\treturn bytes.fromhex("""{encoded_key}""")\n')
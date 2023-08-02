# SPDX-FileCopyrightText: 2023-present anjomro <py@anjomro.de>
#
# SPDX-License-Identifier: EUPL-1.2
import os

import click
import requests

from .key import get_key

KEY_DOWNLOAD_URL = "https://github.com/anjomro/camouflage-decryptor/releases/download/v0.3.0/STATIC_KEY_1GB"

# Use once key can be embedded as binary
# EMBEDDED_KEY_LOCATION = os.path.join(os.path.dirname(__file__), "../../assets/STATIC_KEY_20MB")

ENV_VARIABLE_CUSTOM_KEY = os.environ.get("CAMOUFLAGE_DECRYPTOR_KEY", None)


def get_static_camouflage_key(size_bytes: int) -> bytes:
    """Returns static camouflage key"""
    # Check file size of embedded key without reading it
    embedded_key_size = len(get_key())

    if embedded_key_size >= size_bytes:
        # Read n bytes from embedded key
        return get_key()[:size_bytes]
    else:
        # Check if environment variable is set
        if ENV_VARIABLE_CUSTOM_KEY is not None:
            click.echo("Using user supplied key")
            # Check size of file specified in environment variable
            key_file_size = os.path.getsize(ENV_VARIABLE_CUSTOM_KEY)
            if key_file_size >= size_bytes:
                # Read n bytes from file specified in environment variable
                with open(ENV_VARIABLE_CUSTOM_KEY, "rb") as f:
                    return f.read(size_bytes)
            else:
                # Fail with error message
                raise click.exceptions.UsageError("User supplied key: The hidden file is too large!")
        else:
            # Check size of downloadable key
            response = requests.head(KEY_DOWNLOAD_URL, allow_redirects=True)
            online_key_size = int(response.headers['Content-Length'])
            print(f"Using online key  (up to {make_file_size_human_readable(int(response.headers['Content-Length']))})")
            print(f"The size of the download will be {make_file_size_human_readable(size_bytes)}")
            if online_key_size >= size_bytes:
                # Download exactly the needed amount of bytes
                headers = {"Range": f"bytes=0-{size_bytes - 1}"}  # Range is inclusive
                response = requests.get(KEY_DOWNLOAD_URL, headers=headers)
                return response.content
            else:
                # Fail with error message
                raise click.exceptions.UsageError("The hidden file is too large!")


def decrypt_with_static_key(raw: bytes) -> bytes:
    '''Decrypts raw bytes that were encrypted with static camouflage key'''
    # Get static camouflage key
    key_bytes = get_static_camouflage_key(len(raw))
    # Repeat key bytes to the length of raw bytes
    key_bytes = key_bytes * (len(raw) // len(key_bytes) + 1)
    # XOR static key with raw bytes
    decrypted_bytes = bytes([a ^ b for a, b in zip(raw, key_bytes)])
    return decrypted_bytes


def get_till_space(raw: bytes) -> bytes:
    """Return all bytes of input till first space byte (0x20)"""
    return raw.split(b'\x20')[0]


def extract_text(raw: bytes) -> str:
    '''Extracts text from raw bytes encoded by camouflage standard technique'''
    # Only take bytes till first space byte (0x20)
    text_bytes = get_till_space(raw)
    # Decrypt bytes
    decrypted_bytes = decrypt_with_static_key(text_bytes)
    # Decode bytes to stringfp.clo
    decrypted_text = decrypted_bytes.decode("utf-8")
    return decrypted_text


def bytes_to_int(raw: bytes) -> int:
    """Converts raw bytes to int"""
    return int.from_bytes(raw, byteorder='little')


def get_camouflage_part(raw: bytes) -> bytes:
    """Extract camouflage part from bytes of treated file"""
    camouflage_start_position = get_camouflage_start(raw)
    # Get camouflage part of raw bytes
    craw = raw[camouflage_start_position:]
    return craw


def get_camouflage_start(raw: bytes) -> int:
    """Extract camouflage start position encoded in camouflage part"""
    # Get camouflage start position from fixed position -281
    camouflage_start_position = bytes_to_int(raw[-281:-279])
    return camouflage_start_position


def is_valid_camouflage_part(craw: bytes) -> bool:
    """Checks if bytes are from a file treated with camouflage"""
    # Check that camouflage part starts with one of the following (mixtures of start and end bytes are also ok);
    # ---- 0x00 0x00 0x?? 0x?? 0xd9 0x01
    # ---- 0x20 0x00 0x?? 0x?? 0xc3 0x01

    if craw[:2] not in [b'\x00\x00', b'\x20\x00'] or craw[4:6] not in [b'\xd9\x01', b'\xc3\x01']:
        click.echo("This most likely isn't a file that has been treated with camouflage.")
        return False
    return True


def get_camouflage_password(craw: bytes, verbose: bool = False) -> str:
    """Extract key from image treated with camouflage"""
    # Get obscured key at fixed position -275
    password = extract_text(craw[-275:])
    # Check that key isn't empty
    if len(password) == 0 and verbose:
        click.echo("This camouflage image has no password.", err=True)
    return password


def make_file_size_human_readable(size: int) -> str:
    '''Make file size human readable, adapt to right unit (KB, MB, GB, ...)'''
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    file_size_str = ""
    for unit in units:
        if size < 1024.0:
            file_size_str = f"{size:.2f} {unit}"
            break
        size /= 1024.0
    return file_size_str


def get_all_infos(craw: bytes):
    '''Prints all information that is encoded in camouflage part of file'''
    hidden_file_size = bytes_to_int(craw[-285:-281])
    camouflage_version = extract_text(craw[-20:])
    file_name_carrier = extract_text(craw[-540:])
    file_name_secret = extract_text(craw[-795:])
    original_file_size = get_camouflage_start(craw)

    click.echo(f"{'File Name Carrier:':<30} {file_name_carrier}")
    click.echo(f"{'File Name Secret:':<30} {file_name_secret}")
    click.echo(f"{'Size secret file:':<30} {make_file_size_human_readable(hidden_file_size)}")
    click.echo(f"{'File size unmodified carrier:':<30} {make_file_size_human_readable(original_file_size)}")
    click.echo(f"{'Camouflage Version:':<30} {camouflage_version}")
    click.echo(f"{'Password:':<30} {get_camouflage_password(craw)}")


def get_hidden_data(craw: bytes, max_bytes: int = -1) -> bytes:
    """Extract hidden data from camouflage part of file"""
    # Get size of hidden part at fixed position -285
    hidden_size = bytes_to_int(craw[-285:-281])
    # If max_bytes is -1, take all bytes, else max_bytes
    if max_bytes != -1:
        hidden_size = min(hidden_size, max_bytes)
    # Get hidden part of raw bytes
    hidden_data = decrypt_with_static_key(craw[30:30 + hidden_size])
    return hidden_data


def get_original_data(file_raw: bytes) -> bytes:
    """Extract original data from camouflage part of file"""
    # Check if file is valid camouflage file
    if not is_valid_camouflage_part(get_camouflage_part(file_raw)):
        click.echo("This isn't a valid camouflage file. Outputting unchanged file.", err=True)
        return file_raw
    else:
        # Get start of camouflage part
        camouflage_start_position = get_camouflage_start(file_raw)
        # Get original data
        original_data = file_raw[:camouflage_start_position]
        return original_data

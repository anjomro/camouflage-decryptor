# SPDX-FileCopyrightText: 2023-present anjomro <py@anjomro.de>
#
# SPDX-License-Identifier: EUPL-1.2

import click

CAMOUFLAGE_KEY = """02957A220CA614E1E1CFBF65206F9EB3 99654A53FBF67554AD23CD7E9C29E7FC
E2F94DD2424E06C0F89A1C6238742400 55DF41CB01A2B7F38F8ADDAC33836029
F378243E7AEBD3E49D9D43944AC7456D 2574EB0B98C97CFCC8BA326B00D3C5C2
9434AFB0E5957D2A84A45FE56E272ADB 967E3E483946CF6F71AA3C319AA99E8F
8973B339CA32D5F031597C022E8637F9 2B7E51F241810CD46515F770D4199820
BF20B85567CC81188C133C633C9211E4 5B1B0822604C4AC58AB3C575C3907AF2
B2B6C8D0388AC286F0ACE9CA5C4E3E09 297829995A84D5BA5ED5927A38FAD060
ECF527BAEEB7DE9F9BDE65D47639769C DA688DA8A0A61ED9DB0F4DAB92CD71"""


def get_static_camouflage_key() -> bytes:
    """Returns static camouflage key"""
    # Remove all non hex chars
    key_string: str = "".join([c for c in CAMOUFLAGE_KEY if c in "0123456789ABCDEFabcdef"])
    # Convert to bytes
    key_bytes: bytes = bytes.fromhex(key_string)
    return key_bytes


def decrypt_with_static_key(raw: bytes) -> bytes:
    '''Decrypts raw bytes that were encrypted with static camouflage key'''
    # Get static camouflage key
    key_bytes = get_static_camouflage_key()
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
    # Decode bytes to string
    decrypted_text = decrypted_bytes.decode("utf-8")
    return decrypted_text


def bytes_to_int(raw: bytes) -> int:
    """Converts raw bytes to int"""
    return int.from_bytes(raw, byteorder='little')


def get_camouflage_part(raw: bytes) -> bytes:
    """Extract camouflage part from bytes of treated file"""
    # Get camouflage start position from fixed position -281
    camouflage_start_position = bytes_to_int(raw[-281:-279])
    # Get camouflage part of raw bytes
    craw = raw[camouflage_start_position:]
    return craw


def is_valid_camouflage_part(craw: bytes) -> bool:
    """Checks if bytes are from a file treated with camouflage"""
    # Get size of hidden part at fixed position -285
    hidden_size = bytes_to_int(craw[26:30])
    # The size of the hidden part is twice in the encoded part at different postions.
    control_hidden_size = bytes_to_int(craw[-285:-283])
    # This can be used to reliably check that it is a file that has been treated with camouflage
    if hidden_size != control_hidden_size:
        click.echo("This most likely isn't a file that has been treated with camouflage.")
        return False
    return True


def extract_camouflage_password(craw: bytes):
    """Extract key from image treated with camouflage"""

    # Get obscured key at fixed position -275
    password = extract_text(craw[-275:])
    # Check that key isn't empty
    if len(password) == 0:
        click.echo("This camouflage image has no password. Exiting.")
        return b''
    click.echo("Password Str: " + password)


def get_all_infos(craw: bytes):
    '''Prints all information that is encoded in camouflage part of file'''
    hidden_file_size_bytes = bytes_to_int(craw[26:30])
    camouflage_version = extract_text(craw[-20:])
    file_name_carrier = extract_text(craw[-540:])
    file_name_secret = extract_text(craw[-795:])

    # Make file size human readable (convert to KB, MB, GB, ...)
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    size = hidden_file_size_bytes
    hidden_file_size = ""
    for unit in units:
        if size < 1024.0:
            hidden_file_size = f"{size:.2f} {unit}"
            break
        size /= 1024.0


    click.echo("File Name Carrier: " + file_name_carrier)
    click.echo("File Name Secret: " + file_name_secret)
    click.echo("Hidden File Size: " + hidden_file_size)
    click.echo("Camouflage Version: " + camouflage_version)
    extract_camouflage_password(craw)

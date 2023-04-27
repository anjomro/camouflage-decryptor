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


def split_camouflage_part(jpg_raw: bytes) -> bytes:
    """Split and return camouflage encoded part of jpg"""
    # Get end of jpg (bytes: FF D9)
    end_of_jpg = jpg_raw.rfind(b'\xff\xd9')
    # Get camouflage part of jpg
    camouflage_part = jpg_raw[end_of_jpg + 2:]
    return camouflage_part


def check_if_jpg(data_raw: bytes) -> bool:
    """Check if data is a jpg"""
    if data_raw.startswith(b'\xff\xd8'):
        # Check that data contains jpg end bytes (FF D9)
        if b'\xff\xd9' in data_raw:
            return True
    return False


def extract_camouflage_password(jpg_raw: bytes) -> bytes:
    """Extract key from image treated with camouflage"""
    # Check if jpg
    if not check_if_jpg(jpg_raw):
        click.echo("No jpg found. Are you sure this is a camouflage image? Exiting.")
        return b''
    # Get camouflage part of jpg
    camouflage_part = split_camouflage_part(jpg_raw)
    if len(camouflage_part) == 0:
        click.echo("No camouflage part found. Are you sure this is a camouflage image? Exiting.")
        return b''
    # Ensure that camouflage part starts with 0x20 0x00
    if not camouflage_part.startswith(b'\x20\x00'):
        click.echo("The camouflage part doesn't start with bytes 20 00, this is unexpected. Exiting.")
        #return b''
    # Get obscured key at fixed position -275
    obscured_key = camouflage_part[-275:]
    # Take all bytes till first whitespace byte (0x20)
    key_bytes = obscured_key.split(b'\x20')[0]
    # Check that key isn't empty
    if len(key_bytes) == 0:
        click.echo("This camouflage image has no password. Exiting.")
        return b''
    # Get static camouflage key with same length as obscured key
    static_key = get_static_camouflage_key()[:len(key_bytes)]
    # XOR static key with obscured key
    decrypted_key = bytes([a ^ b for a, b in zip(key_bytes, static_key)])
    click.echo("Password Hex: " + decrypted_key.hex(" ", -2))
    click.echo("Password Str: " + decrypted_key.decode("utf-8"))
    return decrypted_key
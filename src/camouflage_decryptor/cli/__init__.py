# SPDX-FileCopyrightText: 2023-present anjomro <py@anjomro.de>
#
# SPDX-License-Identifier: EUPL-1.2
import click

from camouflage_decryptor.__about__ import __version__
from camouflage_decryptor.decryptor import get_camouflage_password, get_camouflage_part, is_valid_camouflage_part, \
    get_all_infos, get_hidden_data, get_original_data, bytes_to_int


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(version=__version__, prog_name="camouflage-decryptor")
def camouflage_decryptor():
    pass


# Subcommand group to group all dev commands
@click.group()
def dev():
    """Subcommand for development tools"""
    pass


@click.command()
@click.argument('input', type=click.File('rb'))
def get_key(input):
    """Extract password from file treated with camouflage"""
    img_raw = input.read()
    camouflage_bytes = get_camouflage_part(img_raw)
    if is_valid_camouflage_part(camouflage_bytes):
        password = get_camouflage_password(camouflage_bytes, verbose=True)
        click.echo("Password: ", nl=False, err=True)
        click.echo(password)


@click.command()
@click.argument('input', type=click.File('rb'))
def get_info(input):
    """Extract all information from file treated with camouflage"""
    img_raw = input.read()
    camouflage_bytes = get_camouflage_part(img_raw)
    if is_valid_camouflage_part(camouflage_bytes):
        get_all_infos(camouflage_bytes)


def bytes_output(input: bytes, hex: bool, index: bool):
    """Prints bytes to stdout, if wanted as hex with or without index"""
    if hex:
        # Display in blocks of 16 bytes
        for i in range(0, len(input), 16):
            if index:
                # If index enabled print hex position index
                click.echo(f"{i:08x}   {input[i:i + 16].hex(' ')}")
            else:
                click.echo(input[i:i + 16].hex(' '))
    else:
        click.echo(input)


@click.command()
@click.argument('input', type=click.File('rb'))
@click.option("-x", "--hex", is_flag=True, show_default=True, default=False,
              help="Display output as hexadecimal string")
@click.option("-i", "--index", is_flag=True, show_default=True, default=False,
              help="Add hex index to hexadecimal output. Only useful with --hex")
def get_data(input, hex: bool, index: bool):
    """Print hidden data to stdout"""""
    file_raw = input.read()
    camouflage_bytes = get_camouflage_part(file_raw)
    if is_valid_camouflage_part(camouflage_bytes):
        hidden_data = get_hidden_data(camouflage_bytes)
        bytes_output(hidden_data, hex, index)


@click.command()
@click.argument('input', type=click.File('rb'))
@click.option("-x", "--hex", is_flag=True, show_default=True, default=False,
              help="Display output as hexadecimal string")
@click.option("-i", "--index", is_flag=True, show_default=True, default=False,
              help="Add hex index to hexadecimal output. Only useful with --hex")
def get_original(input, hex: bool, index: bool):
    """Print original file to stdout (with removed camouflage part)"""
    file_raw = input.read()
    original_data = get_original_data(file_raw)
    bytes_output(original_data, hex, index)


# Command to generate test payload with x*"a" to stdout to reverse engineer static key
@click.command()
# Argument size: Size of Payload in Bytes, Kilobytes, Megabytes, Gigabytes
@click.argument('size', type=str, default="10MB", required=False)
def generate_test_payload(size: str):
    """Generate test payload with x*"a" to stdout to reverse engineer static key"""
    size = size.upper()
    unit_factor = 1
    unit_signs = ["K", "M", "G", "T", "P"]
    amount = 0
    if size.endswith("B"):
        if size[:-1].isdigit():
            amount = int(size[:-1])
        elif size[-2:-1] in unit_signs:
            amount = int(size[:-2])
            unit_factor = 1024 ** (unit_signs.index(size[-2:-1]) + 1)
        else:
            raise click.BadParameter("Unknown unit, must be one of B, KB, MB, GB, TB, PB")
    elif size.isdigit():
        amount = int(size)
    else:
        raise click.BadParameter(
            "Size must be a whole number with unit (B, KB, MB, GB, TB, PB), unit defaults to Bytes")
    click.echo("a" * amount * unit_factor, nl=False)


# Function to extract static key from payload with recurring character
@click.command()
@click.argument('input', type=click.File('rb'))
@click.option("-x", "--hex", is_flag=True, show_default=True, default=False,
              help="Display output as hexadecimal string")
@click.option("-i", "--index", is_flag=True, show_default=True, default=False,
              help="Add hex index to hexadecimal output. Only useful with --hex")
def extract_static_key(input, hex: bool, index: bool):
    """Extract static key from payload with recurring character"""
    file_raw = input.read()
    camouflage_bytes = get_camouflage_part(file_raw)
    if is_valid_camouflage_part(camouflage_bytes):
        first_decrypted_part = get_hidden_data(camouflage_bytes, 20)
        # Check that data is only one character
        if len(set(first_decrypted_part)) == 1:
            # Get size of hidden part from fixed position
            hidden_size = bytes_to_int(camouflage_bytes[-285:-281])
            # Get recurring character
            recurring_character = first_decrypted_part[0]
            # Get encrypted data
            encrypted_data = camouflage_bytes[30:30 + hidden_size]
            # Get key by XORing encrypted data with -recurring character- * hidden_size
            key = bytes([a ^ recurring_character for a in encrypted_data])
            bytes_output(key, hex, index)
        else:
            raise click.BadParameter(
                "Hidden data is not a recurring character. Please generate payload with: camouflage-decrpytor generate-test-payload")


# Function that reads a binary files that outputs csv containing all bytes converted to int
@click.command()
@click.argument('input', type=click.File('rb'))
@click.option("-o", "--output", type=click.File('w'), default="/dev/stdout",
              help="Destination file for csv output, defaults to stdout")
def get_csv(input, output):
    """Reads a binary files that outputs csv containing all bytes converted to int"""
    file_raw = input.read()
    output.write("index;byte\n")
    for i in range(len(file_raw)):
        output.write(f"{i};{file_raw[i]}\n")


camouflage_decryptor.add_command(get_key)
camouflage_decryptor.add_command(get_info)
camouflage_decryptor.add_command(get_data)
camouflage_decryptor.add_command(get_original)
camouflage_decryptor.add_command(dev)

dev.add_command(generate_test_payload)
dev.add_command(extract_static_key)
dev.add_command(get_csv)

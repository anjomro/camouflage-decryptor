# SPDX-FileCopyrightText: 2023-present anjomro <py@anjomro.de>
#
# SPDX-License-Identifier: EUPL-1.2
import click

from camouflage_decryptor.__about__ import __version__
from camouflage_decryptor.decryptor import get_camouflage_password, get_camouflage_part, is_valid_camouflage_part, \
    get_all_infos, get_hidden_data, get_original_data


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(version=__version__, prog_name="camouflage-decryptor")
def camouflage_decryptor():
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
@click.option("-x", "--hex", is_flag=True, show_default=True, default=False, help="Display output as hexadecimal string")
@click.option("-i", "--index", is_flag=True, show_default=True, default=False, help="Add hex index to hexadecimal output. Only useful with --hex")
def get_data(input, hex: bool, index: bool):
    """Print hidden data to stdout"""""
    file_raw = input.read()
    camouflage_bytes = get_camouflage_part(file_raw)
    if is_valid_camouflage_part(camouflage_bytes):
        hidden_data = get_hidden_data(camouflage_bytes)
        bytes_output(hidden_data, hex, index)


@click.command()
@click.argument('input', type=click.File('rb'))
@click.option("-x", "--hex", is_flag=True, show_default=True, default=False, help="Display output as hexadecimal string")
@click.option("-i", "--index", is_flag=True, show_default=True, default=False, help="Add hex index to hexadecimal output. Only useful with --hex")
def get_original(input, hex: bool, index: bool):
    """Print original file to stdout (with removed camouflage part)"""
    file_raw = input.read()
    original_data = get_original_data(file_raw)
    bytes_output(original_data, hex, index)


camouflage_decryptor.add_command(get_key)
camouflage_decryptor.add_command(get_info)
camouflage_decryptor.add_command(get_data)
camouflage_decryptor.add_command(get_original)

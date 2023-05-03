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
    """Extract key from file treated with camouflage"""
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


@click.command()
@click.argument('input', type=click.File('rb'))
def get_data(input):
    """Print hidden data to stdout"""""
    file_raw = input.read()
    camouflage_bytes = get_camouflage_part(file_raw)
    if is_valid_camouflage_part(camouflage_bytes):
        hidden_data = get_hidden_data(camouflage_bytes)
        click.echo(hidden_data, nl=False)


@click.command()
@click.argument('input', type=click.File('rb'))
def get_original(input):
    """Print original file to stdout (with removed camouflage part)"""
    file_raw = input.read()
    original_data = get_original_data(file_raw)
    click.echo(original_data, nl=False)


camouflage_decryptor.add_command(get_key)
camouflage_decryptor.add_command(get_info)
camouflage_decryptor.add_command(get_data)
camouflage_decryptor.add_command(get_original)

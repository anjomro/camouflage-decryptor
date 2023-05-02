# SPDX-FileCopyrightText: 2023-present anjomro <py@anjomro.de>
#
# SPDX-License-Identifier: EUPL-1.2
import click

from camouflage_decryptor.__about__ import __version__
from camouflage_decryptor.decryptor import extract_camouflage_password, get_camouflage_part, is_valid_camouflage_part


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(version=__version__, prog_name="camouflage-decryptor")
def camouflage_decryptor():
    pass


@click.command()
@click.argument('input', type=click.File('rb'))
def get_key(input):
    """Extract key from JPG file treated with camouflage"""
    img_raw = input.read()
    camouflage_bytes = get_camouflage_part(img_raw)
    if is_valid_camouflage_part(camouflage_bytes):
        extract_camouflage_password(camouflage_bytes)


camouflage_decryptor.add_command(get_key)

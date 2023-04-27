# SPDX-FileCopyrightText: 2023-present anjomro <py@anjomro.de>
#
# SPDX-License-Identifier: EUPL-1.2
import click

from camouflage_decryptor.__about__ import __version__
from camouflage_decryptor.decryptor import extract_camouflage_password


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(version=__version__, prog_name="camouflage-decryptor")
def camouflage_decryptor():
    pass


@click.command()
@click.argument('input', type=click.File('rb'), help="JPG file treated with camouflage"
def get_key(input):
    """Extract key from JPG file treated with camouflage"""
    img_raw = input.read()
    extract_camouflage_password(img_raw)


camouflage_decryptor.add_command(get_key)

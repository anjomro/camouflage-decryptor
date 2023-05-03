# camouflage-decryptor

[![PyPI - Version](https://img.shields.io/pypi/v/camouflage-decryptor.svg)](https://pypi.org/project/camouflage-decryptor)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/camouflage-decryptor.svg)](https://pypi.org/project/camouflage-decryptor)

-----
This is a tool to extract information from files that have been generated with camouflage.

**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

```console
pip install camouflage-decryptor
```

## Usage
This tool provides different tools for analyzing a file that has been generated with [camouflage](http://camouflage.unfiction.com/). This includes the following:

#### Metadata retrieval
To retrieve all the camouflage metadata from a prepared file the following command can be used:
```console
camouflage-decryptor get-key camouflaged-file.jpg
```
The output will look similar to this one:

    File Name Carrier:             normal_file.png
    File Name Secret:              secret.txt
    Size secret file:              4.00 B
    File size unmodified carrier:  4.00 B
    Camouflage Version:            v1.2.1
    Password:                      very-secret-password

'Carrier' refers to the file that has been used to hide the secret file. 'Secret' refers to the file that has been hidden in the carrier file.

#### Password retrieval

To get the password only from a stego file:
```console
camouflage-decryptor get-key my-stego-file.jpg
```

#### Secret file retrieval
To retrieve the secret file from a stego file and save it to a file (here: `secret.txt`):
```console
camouflage-decryptor get-data my-stego-file.jpg > secret.txt
```
This solution only works on Linux and Mac OS X. On Windows, the following command can be used:
```console
python -m camouflage-decryptor get-data my-stego-file.jpg | Out-File -Encoding utf8 secret.txt
```

#### Get unmodified carrier file
To get the unmodified carrier file from a stego file (-> remove the part added by camouflage) and save it to a file (here: `carrier.png`):
```console
camouflage-decryptor get-original camouflaged-carrier.png > carrier.png
```
This solution only works on Linux and Mac OS X. On Windows, the following command can be used:
```console
python -m camouflage-decryptor get-original camouflaged-carrier.png | Out-File -Encoding utf8 carrier.png
```

#### Usage on Windows
For all presented commands you might need to use the following syntax to call the script, e.g. if on Windows:
```console
python -m camouflage_decryptor get-key my-stego-image.jpg
```

## License

`camouflage-decryptor` is distributed under the terms of the [EUPL-1.2](https://spdx.org/licenses/EUPL-1.2.html) license.

# camouflage-decryptor

[![PyPI - Version](https://img.shields.io/pypi/v/camouflage-decryptor.svg)](https://pypi.org/project/camouflage-decryptor)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/camouflage-decryptor.svg)](https://pypi.org/project/camouflage-decryptor)

-----
This is a tool to extract information from files that have been generated with camouflage. Currently only JPEG-files are supported.

**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

```console
pip install camouflage-decryptor
```

## Usage

To get the password from a stego image:
```console
camouflage-decryptor get-key my-stego-image.jpg
```

You might need to use the following syntax to call the script, e.g. if on Windows:
```console
python -m camouflage_decryptor get-key my-stego-image.jpg
```

## License

`camouflage-decryptor` is distributed under the terms of the [EUPL-1.2](https://spdx.org/licenses/EUPL-1.2.html) license.

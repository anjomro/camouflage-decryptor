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

#### Command Line Help
For the tool and all its subcommands, help can be retrieved by calling the tool with the `--help` flag:
```console
camouflage-decryptor --help
```


#### Metadata retrieval
To retrieve all the camouflage metadata from a prepared file the following command can be used:
```console
camouflage-decryptor get-info camouflaged-file.jpg
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

#### Advanced: Generate own static key file for larger files

The tool is able to decrypt files up to 10MB using an embedded key. For larger files up to 1GB a static key is downloaded to decrypt the file.
For larger files or to avoid the download of the static key, a custom static key can be supplied. 

A 1GB key can be downloaded from the releases for offline use: [https://github.com/anjomro/camouflage-decryptor/releases/download/v0.3.0/STATIC_KEY_1GB](https://github.com/anjomro/camouflage-decryptor/releases/download/v0.3.0/STATIC_KEY_1GB)

A larger key can be obtained using the following steps:

- Setup a virtual machine using Windows XP
  - This can be done using this vagrant box: https://app.vagrantup.com/dvgamerr/boxes/win-xp-sp3
  - Given that VirtualBox and Vagrant are installed the Box can be started using the following commands:
    - ```console
      mkdir vagrant-win-xp && cd vagrant-win-xp
      vagrant init dvgamerr/win-xp-sp3
      vagrant up
      ```
  - Follow these instructions to setup a shared folder to exchange files: https://techblog.willshouse.com/2013/01/27/connect-to-a-shared-folder-with-virtualbox-and-windows-xp/
- Download camouflage and install it on the virtual machine
  - Download camouflage from here: http://camouflage.unfiction.com/
  - Transfer the downloaded file to the virtual machine via the shared folder
  - Install camouflage on the virtual machine
- Create a payload with the intended size
  - This can be done using the camouflage-decryptor tool:
  - `camouflage-decryptor dev generate-test-payload 2GB > PAYLOAD_2GB.txt`
  - This will create a file with the size of 2GB. Adapt the size to your needs.
- Transfer the payload to the virtual machine
  - This can be done using the shared folder
- Create a stego file using camouflage
  - Find a carrier file (a file to hide the payload in)
    - Ideally this file should be small to avoid unneccecary resource consumption
    - Any random file will do
    - If no file is at hand, just create a small text file
  - Right click on the generated **payload** file and select the Camouflage Option
  - Click _Next_
  - For the field _Camouflage using_ select the previously selected carrier file
  - For the field _Create This File_ select a sensible file name, e.g `camouflaged_2GB.txt` and remove the _read only_ checkmark
  - You can leave the password field empty, but it also doesn't matter if you do set a password
- Extract the static key from the file treated with Camouflage
  - Use the camouoflage-decryptor tool to extract the static key
  - `camouflage-decryptor dev extract-static-key path/to/camouflaged_2GB.txt > save/path/STATIC_KEY_2GB`
  - Adapt the paths to the location and the location you want to save the static key

#### Advanced: Use a custom static key to decrypt a file

If you want to use a custom static key to decrypt a file you can use it using the following syntax:

```console
CAMOUFLAGE_DECRYPTOR_KEY=/path/to/static/key.bin camouflage-decryptor get-data my-stego-file.jpg > secret.txt
```

It is necessary to use an absolute path to the static key.

To avoid prefixing every command, you can also set the static key for your session:

```console
export CAMOUFLAGE_DECRYPTOR_KEY=/path/to/static/key.bin
```

After setting the key location once, you can then use the tool as usual:

```console
camouflage-decryptor get-data my-stego-file.jpg > secret.txt
```


Both methods work with all functionality that requires a static key.

To obtain a static key see the section above.

#### Usage on Windows
For all presented commands, you might need to use the following syntax to call the script, e.g. if on Windows:
```console
python -m camouflage_decryptor get-key my-stego-image.jpg
```

## License

`camouflage-decryptor` is distributed under the terms of the [EUPL-1.2](https://spdx.org/licenses/EUPL-1.2.html) license.

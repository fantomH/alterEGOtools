#!/usr/bin/env python
#--{ alterEGO Linux: "Open the vault of knowledge" }---------------------------
#
# ego.py
#   created        : 2021-06-05 00:03:38 UTC
#   updated        : 2021-06-05 00:03:43 UTC
#   description    : Deploy and update alterEGO Linux.
#------------------------------------------------------------------------------

import argparse
import os
import subprocess

def create_partition():
    partition = '''label: dos
                   device: /dev/sda
                   unit: sectors
                   sector-size: 512

                   /dev/sda1 : start=        2048, type=83, bootable
                '''

    subprocess.run(['sfdisk', '/dev/sda'], text=True, input=partition)

    #### Formating the File System.

    subprocess.run(['mkfs.ext4', '/dev/sda1'])

    #### Mounting /dev/sda1 to /mnt.

    subprocess.run(['mount', '/dev/sda1', '/mnt'])

    #### Creating ${HOME}. 

    os.mkdir('/mnt/home')

    #### Generating the fstab.

    subprocess.run(['genfstab', '-U', '/mnt', '>>', '/mnt/etc/fstab'])

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--minimal", action="store_true", help="Install a minimal instance of Arch Linux.")

    args = parser.parse_args()

    if args.minimal:
        create_partition()
        # print('hello')

if __name__ == '__main__':
    main()

#--{ file:FIN }----------------------------------------------------------------

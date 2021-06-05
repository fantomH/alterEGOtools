#!/usr/bin/env python
#--{ alterEGO Linux: "Open the vault of knowledge" }---------------------------
#
# ego.py
#   created        : 2021-06-05 00:03:38 UTC
#   updated        : 2021-06-05 00:03:43 UTC
#   description    : Deploy and update alterEGO Linux.
#------------------------------------------------------------------------------

import subprocess

def create_partition():
    partition = '''label: dos
                   device: /dev/sda
                   unit: sectors
                   sector-size: 512

                   /dev/sda1 : start=        2048, type=83, bootable
                '''

    subprocess.run(['sfdisk', '/dev/sda'], text=True, input=partition)

out = create_partition()


#--{ file:FIN }----------------------------------------------------------------

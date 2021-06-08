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
import shutil
import subprocess
import sys
import threading

git_tools = 'https://github.com/fantomH/alterEGOtools.git'
git_alterEGO = 'https://github.com/fantomH/alterEGO.git'
usr_local = '/usr/local'
local_tools = f'{usr_local}/alterEGOtools'
local_alterEGO = f'{usr_local}/alterEGO'

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

    #### Install minimal packages

    min_pkg = ['base',
               'base-devel',
               'git',
               'grub',
               'linux',
               'networkmanager',
               'pacman-contrib',
               'python',
               'vim']
    
    pacstrap = subprocess.run(['pacstrap', '/mnt'], input=' '.join(min_pkg), text=True).check_returncode

    #### Generating the fstab.
    subprocess.run('genfstab -U /mnt >> /mnt/etc/fstab', shell=True)

def chroot():
    '''
    Preparing and changing the root to the new system.
    '''

    print('NOT STARTED YET')

    thread = threading.Thread(target=create_partition)
    thread.start()
    thread.join()
    
    print(thread.getName())
    
    shutil.copy2('/root/ego.py', '/mnt/usr/local/bin/ego.py')
    shutil.whatis('git')
    subprocess.run(f'git clone {git_tools} /mnt/usr/local', shell=True)
    # subprocess.run(['arch-chroot', '/mnt', 'python', '/usr/local/alterEGOtools/ego.py', '--sysconfig'])

def sysconfig():
    subprocess.run(['git', 'clone', git_alterEGO, usr_local])
    
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--minimal", action="store_true", help="Install a minimal instance of Arch Linux.")
    parser.add_argument("--sysconfig", action="store_true", help="Stage 2")

    args = parser.parse_args()

    if args.minimal:
        chroot()
    if args.sysconfig:
        sysconfig()

if __name__ == '__main__':
    main()

#--{ file:FIN }----------------------------------------------------------------

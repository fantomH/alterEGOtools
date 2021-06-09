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
import shlex
import shutil
import subprocess
import sys
import threading

#----------{ GLOBAL VARIABLES }
git_tools = 'https://github.com/fantomH/alterEGOtools.git'
git_alterEGO = 'https://github.com/fantomH/alterEGO.git'
usr_local = '/usr/local'
local_tools = f'{usr_local}/alterEGOtools'
local_alterEGO = f'{usr_local}/alterEGO'

basic_pkg = ['base',
            'base-devel',
            'git',
            'grub',
            'linux',
            'networkmanager',
            'python',
            'vim']

def execute(cmd):
    args = shlex.split(cmd)
    subprocess.run(args)

def installer(mode):
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

    execute(f"pacstrap /mnt {' '.join(basic_pkg)}")

    #### Generating the fstab.
    subprocess.run('genfstab -U /mnt >> /mnt/etc/fstab', shell=True)

    shutil.copy('/root/ego.py', '/mnt/root/ego.py')
    if mode == 'minimal':
        execute(f'arch-chroot /mnt python /root/ego.py --sysconfigmin')

    # execute(f'umount -R /mnt')
    # execute(f'shutdown now') 

def sysconfig(mode):
    subprocess.run(['git', 'clone', git_tools, local_tools])

    if mode == 'beast':
        execute(f"git clone {git_alterEGO} {local_alterEGO}")

    #-----[ TIMEZONE & CLOCK ]
    os.symlink('/usr/share/zoneinfo/America/New_York', '/etc/localtime')
    execute(f'timedatectl set-ntp true')
    execute(f'hwclock --systohc --utc')

    #-----[ LOCALE ]

    print(':: Generating locale...')
    execute(f'sed -i "s/#en_US.UTF-8/en_US.UTF-8/" /etc/locale.gen')
    with open('/etc/locale.conf', 'w') as locale_conf:
        locale_conf.write('LANG=en_US.UTF-8')
    os.putenv('LANG', 'en_US.UTF-8')
    execute(f'locale-gen')

    #-----[ NETWORK CONFIGURATION ]

    print(':: Setting up network...')
    with open('/etc/hostname', 'w') as etc_hostname:
        etc_hostname.write('pc1')
    with open('/etc/hosts', 'w') as etc_hosts:
        etc_hosts.write('''
127.0.0.1	localhost
::1		localhost
127.0.1.1	pc1.localdomain	pc1
''')

    print(' -> Enabling NetworkManager daemon')
    execute(f'systemctl enable NetworkManager.service')

    #-----[ POPULATING /etc/skel ]

    #-----[ USERS and PASSWORDS ]

    print(':: Configuring users and passwords...')
    root_passwd = 'toor'
    subprocess.run(['passwd'], input=f'{root_passwd}\n{root_passwd}\n', text=True)

    # printf '%s\n' " -> Adding sudo user..."
    # useradd -m -g users -G wheel ${user} 
    # printf "${user_passwd}\n${user_passwd}\n" | passwd ${user}
    # sleep 1

    # printf '%s\n' " -> Enabling sudoers..."
    # sed -i 's/# %wheel ALL=(ALL) NOPASSWD: ALL/%wheel ALL=(ALL) NOPASSWD: ALL/' /etc/sudoers
    # sleep 1

    #-----[ SHARED RESOURCES ]

    #-----[ SWAPFILE ]

    #-----[ FIX PACMAN MIRRORLIST ]

    #-----[ PACKAGES INSTALL ]

    #-----[ YAY ]

    #-----[ BOOTLOADER ]

    print(':: Installing and configuring the bootloader...')
    execute(f'grub-install /dev/sda')
    execute(f'grub-mkconfig -o /boot/grub/grub.cfg')

    #-----[ VIRTUALBOX VM OPTIONS ]

    if mode == 'beast':
        execute(f'systemctl start vboxservice.service')
        execute(f'systemctl enable vboxservice.service')
    
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--minimal", action="store_true", help="Install a minimal instance of Arch Linux.")
    parser.add_argument("--sysconfigmin", action="store_true", help="Stage 2")

    args = parser.parse_args()

    if args.minimal:
        installer(mode='minimal')
    if args.sysconfigmin:
        sysconfig(mode='minimal')

if __name__ == '__main__':
    main()

#--{ file:FIN }----------------------------------------------------------------

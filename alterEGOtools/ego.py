#!/usr/bin/env python
#--{ alterEGO Linux: "Open the vault of knowledge" }---------------------------
#
# ego.py
#   created        : 2021-06-05 00:03:38 UTC
#   updated        : 2021-06-11 08:51:18 UTC
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

timezone = 'America/New_York'
hostname = 'pc1'
root_passwd = 'toor'
user = 'ghost'
user_passwd = 'password1'

basic_pkg = ['base',
            'base-devel',
            'git',
            'grub',
            'linux',
            'networkmanager',
            'python',
            'vim']

beast_pkg = ['firefox',
             'wget']

def copy_recursive(src, dst):
    '''
    The src is the source root directory.
    The dest is the source root of the destination.
    ref. http://techs.studyhorror.com/d/python-how-to-copy-or-move-folders-recursively
    '''

    print(f":: Copying files to {dst}...")

    for src_dir, dirs, files in os.walk(src):
        dst_dir = src_dir.replace(src, dst)
        if not os.path.exists(dst_dir):
            os.mkdir(dst_dir)

        for f in files:
            src_file = os.path.join(src_dir, f)
            dst_file = os.path.join(dst_dir, f)
            print(f" -> Copying {dst_file}")

            if os.path.exists(dst_file):
                os.remove(dst_file)
            else:
                shutil.copy2(src_file, dst_file)

def execute(cmd):
    args = shlex.split(cmd)
    subprocess.run(args)

def pacstrap():
    pacstrap = subprocess.run(shlex.split(f"pacstrap /mnt {' '.join(basic_pkg)}"), capture_output=True)

    if pacstrap.returncode != 0:
        pacstrap()

def pacman(pkg_list):
    pkgs = ' '.join(pkg_list)
    execute(f"pacman -Syu --noconfirm --needed {pkgs}")

def git(git_repository, local_directory):

    if not os.path.isdir(local_directory):
        execute(f"git clone {git_repository} {local_directory}")
    else:
        execute(f"git -C {local_directory} pull")

def testrerun(string):
    print(string)

def installer(mode):
    partition = '''label: dos
                   device: /dev/sda
                   unit: sectors
                   sector-size: 512

                   /dev/sda1 : start=        2048, type=83, bootable
                '''

    subprocess.run(['sfdisk', '/dev/sda'], text=True, input=partition)

    #### Formating the File System.

    execute(f"mkfs.ext4 /dev/sda1")

    #### Mounting /dev/sda1 to /mnt.

    execute(f"mount /dev/sda1 /mnt")

    #### Creating ${HOME}. 

    os.mkdir('/mnt/home')

    #### Install minimal packages

    pacstrap()

    #### Generating the fstab.
    subprocess.run('genfstab -U /mnt >> /mnt/etc/fstab', shell=True)

    shutil.copy('/root/ego.py', '/mnt/root/ego.py')
    if mode == 'minimal':
        execute(f'arch-chroot /mnt python /root/ego.py --sysconfig minimal')
    elif mode == 'beast':
        execute(f'arch-chroot /mnt python /root/ego.py --sysconfig beast')

    # execute(f'umount -R /mnt')
    # execute(f'shutdown now') 

def sysconfig(mode):

    #-----[ GIT REPOSITORIES ]
    print(f":: Fetching AlterEGO tools, config and other stuff...")

    print(f" -> Pulling {git_tools}...")
    git(git_tools, local_tools)

    if mode == 'beast':
        print(f" -> Pulling {git_alterEGO}")
        git(git_alterEGO, local_alterEGO)

    #-----[ TIMEZONE & CLOCK ]
    os.symlink(f'/usr/share/zoneinfo/{timezone}', '/etc/localtime')
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
        etc_hostname.write(hostname)
    with open('/etc/hosts', 'w') as etc_hosts:
        etc_hosts.write(f'''
127.0.0.1	localhost
::1		localhost
127.0.1.1	{hostname}.localdomain	{hostname}
''')

    print(' -> Enabling NetworkManager daemon...')
    execute(f'systemctl enable NetworkManager.service')

    #-----[ POPULATING /etc/skel ]

    if mode == beast:
        src = f"{local_alterEGO}/config/"
        dst = f"/etc/skel/"
        copy_recursive(src, dst)

    #-----[ USERS and PASSWORDS ]

    print(':: Configuring users and passwords...')
    print(' -> Setting password for root user...')
    subprocess.run(['passwd'], input=f'{root_passwd}\n{root_passwd}\n', text=True)

    if mode == 'beast':
        print(f' -> Creating user {user}...')
        execute(f'useradd -m -g users -G wheel {user}') 
        print(f' -> Setting password for {user}...')
        subprocess.run(['passwd', user], input=f'{user_passwd}\n{user_passwd}\n', text=True)

        print(f' -> Enabling sudoers...')
        execute(f'sed -i "s/# %wheel ALL=(ALL) NOPASSWD: ALL/%wheel ALL=(ALL) NOPASSWD: ALL/" /etc/sudoers')

    #-----[ SHARED RESOURCES ]

    #-----[ SWAPFILE ]

    #-----[ FIX PACMAN MIRRORLIST ]

    #-----[ PACKAGES INSTALL ]

    if mode == 'beast':
        pacman(beast_pkg)

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
    parser.add_argument("--install", type=str, choices=['minimal', 'beast'], help="Install AlterEGO Linux.")
    parser.add_argument("--sysconfig", type=str, choices=['minimal', 'beast'], help="Initiate the system configuration after the Installer.")
    parser.add_argument("--rerun", type=str, help="Until I figure out things...")

    args = parser.parse_args()

    if args.install:
        mode = args.install
        print(f":: This will install AlterEGO Linux in {mode} mode...")
        installer(mode)
    if args.sysconfig:
        mode = args.sysconfig
        sysconfig(mode)
    if args.rerun:
        eval(args.rerun)
        

if __name__ == '__main__':
    main()

#--{ file:FIN }----------------------------------------------------------------

#!/usr/bin/env python
#--{ alterEGO Linux: "Open the vault of knowledge" }---------------------------
#
# ego.py
#   created        : 2021-06-05 00:03:38 UTC
#   updated        : 2021-06-21 11:08:17 UTC
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
gitTOOLS = 'https://github.com/fantomH/alterEGOtools.git'
gitEGO = 'https://github.com/fantomH/alterEGO.git'
usr_local = '/usr/local'
localTOOLS = f'{usr_local}/alterEGOtools'
localEGO = f'{usr_local}/alterEGO'

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

minimal_pkg = ['fzf',
               'lynx',
               'man-db',
               'man-pages',
               'openssh',
               'openvpn',
               'rsync',
               'tmux',
               'wget']

full_pkg = ['alsa-utils',
            'arp-scan',
            'bat',
            'bc',
            'bind',
            'binwalk',
            'bleachbit',
            'cmatrix',
            'code',
            'cronie',
            'dos2unix',
            'entr',
            'exfat-utils',
            'feh',
            'ffmpeg',
            'firefox',
            'freerdp',
            'gimp',
            'gnu-netcat',
            'go',
            'htop',
            'i3-gaps',
            'imagemagick',
            'inkscape',
            'john',
            'jq',
            'jre11-openjdk',
            'libreoffice-fresh',
            'mariadb-clients',
            'metasploit',
            'mlocate',
            'mtools',
            'mtr',
            'net-tools',
            'nfs-utils',
            'nikto',
            'nmap',
            'notify-osd',
            'ntfs-3g',
            'p7zip',
            'perl-image-exiftool',
            'polkit-gnome',
            'php',
            'postgresql',
            'pptpclient',
            'pulseaudio',
            'pv',
            'python-beautifulsoup4',
            'python-pandas',
            'python-pip',
            'python-pyaml',
            'python-rich',
            'qrencode',
            'qtile',
            'ranger',
            'remmina',
            'screen',
            'screenkey',
            'sddm',
            'shellcheck',
            'sqlitebrowser',
            'sxiv',
            'tcpdump',
            'tesseract',
            'tesseract-data-eng',
            'tesseract-data-fra',
            'thunar',
            'thunar-volman',
            'tidy',
            'tk',
            'traceroute',
            'transmission-gtk',
            'tree',
            'unzip',
            'virtualbox-guest-utils',
            'w3m',
            'whois',
            'wireshark-qt',
            'xclip',
            'xcompmgr',
            'xdotool',
            'xfce4-terminal',
            'xorg-server',
            'xorg-xinit',
            'xterm',
            'youtube-dl',
            'zathura',
            'zathura-pdf-mupdf',
            'zbar']

beast_pkg = [*minimal_pkg, *full_pkg]

aur_pkg = ['burpsuite',
           'dirbuster',
           'gobuster-git',
           'gromit-mpx-git',
           'inxi',
           'librespeed-cli-bin',
           'pandoc-bin',
           'powershell-bin',
           'simple-mtpfs',
           'wfuzz-git']

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
            shutil.copy2(src_file, dst_file)

def execute(cmd, cwd=None):
    cmd_list = shlex.split(cmd)
    subprocess.run(cmd_list, cwd=cwd)

def git(git_repository, local_directory):

    if not os.path.isdir(local_directory):
        execute(f"git clone {git_repository} {local_directory}")
    else:
        execute(f"git -C {local_directory} pull")

def shared_resources():

    #-----[ bookmarks.db ]
    f = 'bookmarks.db'
    print(f":: Deploying {f} to /usr/local/share...")
    src = os.path.join(localEGO, 'share', f)
    dst = os.path.join('/usr/local/share', f)
    os.symlink(src, dst)

def shared_bin():

    #### Deploys applications.

    localEGO_bin = f"{localEGO}/bin"
    files = os.listdir(localEGO_bin)

    for f in files:
        print(f":: Deploying {f} to /usr/local/bin...")
        src = os.path.join(localEGO_bin, f)
        dst = os.path.join('/usr/local/bin', f)
        os.symlink(src, dst)

def shared_wordlist():

    #### Deploys wordlists.

    if not os.path.exists('/usr/local/share/wordlist'):
        os.mkdir('/usr/local/share/wordlist')

    localEGO_wordlist = f"{localEGO}/share/wordlist"
    files = os.listdir(localEGO_wordlist)

    for f in files:
        print(f":: Deploying {f} to /usr/local/share/wordlist...")
        src = os.path.join(localEGO_wordlist, f)
        dst = os.path.join('/usr/local/share/wordlist', f)
        os.symlink(src, dst)

def shared_reverse_shell():

    #### Deploys reverse shells.

    if not os.path.exists('/usr/local/share/reverse_shell'):
        os.mkdir('/usr/local/share/reverse_shell')

    localEGO_reverse_shell = f"{localEGO}/share/reverse_shell"
    files = os.listdir(localEGO_reverse_shell)

    for f in files:
        print(f":: Deploying {f} to /usr/local/share/reverse_shell...")
        src = os.path.join(localEGO_reverse_shell, f)
        dst = os.path.join('/usr/local/share/reverse_shell', f)
        os.symlink(src, dst)

def pacman(pkg_list):
    pkgs = ' '.join(pkg_list)
    execute(f"pacman -Syu --noconfirm --needed {pkgs}")

def pacstrap():

    pacstrap = subprocess.run(shlex.split(f"pacstrap /mnt {' '.join(basic_pkg)}"))
    return pacstrap.returncode

def swapfile():

    execute(f"fallocate -l 1G /swapfile")
    os.chmod('/swapfile', 0o600)
    execute(f"mkswap /swapfile")
    execute(f"swapon /swapfile")
    with open('/etc/fstab', 'a') as swap_file:
        swap_file.write("/swapfile none swap defaults 0 0")

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
    #... Some pkgs might throw errors. Need to catch return code and retry if
    #... it fails.

    returned_code = pacstrap()
    rounds = 3
    while returned_code != 0:
        if rounds > 0:
            returned_code = pacstrap()
            rounds -= 1
        else:
            break

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

    print(f" -> Pulling {gitTOOLS}...")
    git(gitTOOLS, localTOOLS)

    if mode == 'beast':
        print(f" -> Pulling {gitEGO}")
        git(gitEGO, localEGO)

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

    if mode == 'beast':
        src = f"{localEGO}/config/"
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

    if mode == 'beast':
        shared_resources()
        shared_bin()
        shared_wordlist()
        shared_reverse_shell()
        #### assets
        copy_recursive(os.path.join(localEGO, 'share', 'assets'), os.path.join(usr_local, 'share', 'assets'))
        #### backgrounds
        copy_recursive(os.path.join(localEGO, 'share', 'backgrounds'), os.path.join(usr_local, 'share', 'backgrounds'))

    #-----[ SWAPFILE ]

    print(f":: Creating the swapfile...")
    swapfile()

    #-----[ FIX PACMAN MIRRORLIST ]

    #-----[ PACKAGES INSTALL ]

    if mode == 'minimal':
        pacman(minimal_pkg)

    if mode == 'beast':
        pacman(beast_pkg)

    #-----[ YAY ]

    if mode == 'beast':
        print(f":: Installing YAY...")
        # subprocess.run(shlex.split(f"git clone https://aur.archlinux.org/yay.git"), cwd='/opt')
        execute(f"git clone https://aur.archlinux.org/yay.git", cwd='/opt')
        execute(f"chown -R {user}:users /opt/yay")
        subprocess.run(shlex.split(f"su {user} -c 'makepkg -si --needed --noconfirm'"), cwd='/opt/yay')

        print(f":: Installing AUR packages...")
        pkg_list = ' '.join(aur_pkg)
        execute(f"sudo -u {user} /bin/bash -c 'yay -S --noconfirm {pkg_list}'")

    #-----[ SDDM ]

    if mode == 'beast':
        shutil.copy(os.path.join(localEGO, 'global', 'etc', 'sddm.conf'),
                    '/etc/sddm.conf')
        copy_recursive(os.path.join(localEGO, 'global', 'usr', 'share', 'sddm', 'themes', 'alterEGO-simplyblack'),
                       '/usr/share/sddm/themes/alterEGO-simplyblack')

    #-----[ GENERATING mandb ]

    execute(f"mandb")

    #-----[ SETTING JAVA DEFAULT ]

        #### Burpsuite
        #... Not running with java 16.
        #... will need to install jre11-openjdk.
        #... $ sudo archlinux-java set java-11-openjdk

    execute(f"archlinux-java set java-11-openjdk")

    #-----[ BOOTLOADER ]

    print(':: Installing and configuring the bootloader...')
    execute(f'grub-install /dev/sda')
    execute(f'grub-mkconfig -o /boot/grub/grub.cfg')

    #-----[ VIRTUALBOX SERVICES ]

    if mode == 'beast':
        execute(f'systemctl start vboxservice.service')
        execute(f'systemctl enable vboxservice.service')

    #-----[ SDDM SERVICES ]

    if mode == 'beast':
        execute(f'systemctl enable sddm.service')
    
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

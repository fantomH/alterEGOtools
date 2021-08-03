#!/usr/bin/env python
# { alterEGO Linux: "Open the vault of knowledge" }
#
# ego.py
#   created        : 2021-06-05 00:03:38 UTC
#   updated        : 2021-08-03 18:40:02 UTC
#   description    : Deploy and update alterEGO Linux.
# _____________________________________________________________________________

import argparse
from collections import namedtuple
import os
import shlex
import shutil
import subprocess
import sys
import threading
from time import sleep

# { GLOBAL VARIABLES }_________________________________________________________
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

pkgs = {
        'alsa-utils':               'full',
        'arp-scan':                 'full',
        'base':                     'basic',
        'base-devel':               'basic',
        'bat':                      'full',
        'bc':                       'full',
        'bind':                     'full',
        'binwalk':                  'full',
        'bleachbit':                'full',
        'brave':                    'full',
        'burpsuite':                'aur',
        'cmatrix':                  'full',
        'code':                     'full',
        'cronie':                   'full',
        'dirbuster':                'aur',
        'dos2unix':                 'full',
        'entr':                     'full',
        'exfat-utils':              'full',
        'feh':                      'full',
        'ffmpeg':                   'full',
        'firefox':                  'full',
        'freerdp':                  'full',
        'fzf':                      'minimal',
        'gimp':                     'full',
        'git':                      'basic',
        'gnu-netcat':               'full',
        'go':                       'full',
        'gobuster-git':             'aur',
        'gromit-mpx-git':           'aur',
        'grub':                     'basic',
        'htop':                     'full',
        'i3-gaps':                  'full',
        'imagemagick':              'full',
        'inkscape':                 'full',
        'inxi':                     'aur',
        'john':                     'full',
        'jq':                       'full',
        'jre11-openjdk':            'full',
        'libreoffice-fresh':        'full',
        'librespeed-cli-bin':       'aur',
        'linux':                    'basic',
        'lynx':                     'minimal',
        'man-db':                   'minimal',
        'man-pages':                'minimal',
        'mariadb-clients':          'full',
        'metasploit':               'full',
        'mlocate':                  'full',
        'mtools':                   'full',
        'mtr':                      'full',
        'net-tools':                'full',
        'networkmanager':           'basic',
        'nfs-utils':                'full',
        'nikto':                    'full',
        'nmap':                     'full',
        'notify-osd':               'full',
        'ntfs-3g':                  'full',
        'openssh':                  'minimal',
        'openvpn':                  'minimal',
        'p7zip':                    'full',
        'pandoc-bin':               'aur',
        'pavucontrol':              'full',
        'perl-image-exiftool':      'full',
        'php':                      'full',
        'polkit-gnome':             'full',
        'postgresql':               'full',
        'powershell-bin':           'aur',
        'pptpclient':               'full',
        'pulseaudio':               'full',
        'pv':                       'full',
        'python':                   'basic',
        'python-beautifulsoup4':    'full',
        'python-pandas':            'full',
        'python-pip':               'full',
        'python-pyaml':             'full',
        'python-rich':              'full',
        'qrencode':                 'full',
        'qtile':                    'full',
        'ranger':                   'full',
        'remmina':                  'full',
        'rsync':                    'minimal',
        'screen':                   'full',
        'screenkey':                'full',
        'sddm':                     'full',
        'shellcheck':               'full',
        'simple-mtpfs':             'aur',
        'sqlitebrowser':            'full',
        'sxiv':                     'full',
        'tcpdump':                  'full',
        'tesseract':                'full',
        'tesseract-data-eng':       'full',
        'tesseract-data-fra':       'full',
        'thunar':                   'full',
        'thunar-volman':            'full',
        'tidy':                     'full',
        'tk':                       'full',
        'tmux':                     'minimal',
        'traceroute':               'full',
        'transmission-gtk':         'full',
        'tree':                     'full',
        'unzip':                    'full',
        'vim':                      'basic',
        'virtualbox-guest-utils':   'full',
        'w3m':                      'full',
        'wfuzz-git':                'aur',
        'wget':                     'minimal',
        'whois':                    'full',
        'wireshark-qt':             'full',
        'xclip':                    'full',
        'xcompmgr':                 'full',
        'xdotool':                  'full',
        'xfce4-terminal':           'full',
        'xorg-server':              'full',
        'xorg-xinit':               'full',
        'xterm':                    'full',
        'youtube-dl':               'full',
        'zathura':                  'full',
        'zathura-pdf-mupdf':        'full',
        'zbar':                     'full',
        }

# { UTIL FUNCTIONS }___________________________________________________________

def is_virtual_machine():
    # -- Use `$ systemd-detect-virt`
    # .. If VirtualBox will return 'oracle'.
    # .. If not in VM, will return 'none'.
    pass

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
    cmd_run = subprocess.run(cmd_list, cwd=cwd)

    CommandResults = namedtuple('CommandResults', ['returncode'])
    return CommandResults(cmd_run.returncode)

def git(git_repository, local_directory):

    if not os.path.isdir(local_directory):
        execute(f"git clone {git_repository} {local_directory}")
    else:
        execute(f"git -C {local_directory} pull")

def msg(message, color=None):
    colors = {
        'green': '\033[92m'
        'reset': '\033[00m'
            }
    if color in not None:
        msg_color = colors.get[color]
    print(f"{color}{message}{reset}")
    sleep(5)

def testrerun(string):
    print(string)

# { INSTALLER FUNCTIONS }______________________________________________________

def packages(required_by, mode=None):

    if required_by == 'pacstrap':
        pkgs_list = [k for k, v in pkgs.items() if v in ['basic']]
    elif required_by == 'pacman':
        if mode == 'minimal':
            pkgs_list = [k for k, v in pkgs.items() if v in ['minimal']]
        elif mode == 'beast':
            pkgs_list = [k for k, v in pkgs.items() if v in ['minimal', 'full']]
    elif required_by == 'yay':
            pkgs_list = [k for k, v in pkgs.items() if v in ['aur']]

    return pkgs_list

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

def pacman(mode):
    pkgs_list = ' '.join(packages('pacman', mode))
    msg(f'Packages list: \n{pkgs_list}', color='green')
    execute(f"pacman -Syu --noconfirm --needed {pkgs_list}")

def pacstrap():

    pkgs_list = ' '.join(packages('pacstrap'))

    try:
        execute(f"pacstrap /mnt {pkgs_list}")
    except:
        execute(f"pacstrap /mnt {pkgs_list}")
    
    #### Install minimal packages
    #... Some pkgs might throw errors. Need to catch return code and retry if
    #... it fails.

    # returned_code = _pacstrap.returncode
    # print(returned_code)
    # rounds = 3
    # while returned_code != 0:
        # if rounds > 0:
            # returned_code = _pacstrap.returncode
            # rounds -= 1
        # else:
            # break

def swapfile():

    execute(f"fallocate -l 1G /swapfile")
    os.chmod('/swapfile', 0o600)
    execute(f"mkswap /swapfile")
    execute(f"swapon /swapfile")
    with open('/etc/fstab', 'a') as swap_file:
        swap_file.write("/swapfile none swap defaults 0 0")

# { INSTALLER }________________________________________________________________

def installer(mode):
    msg(':: Creating the partition...', color='green')
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
    print(f"  -> Created {os.listdir('/mnt')}")

    # [ PACSTRAP ]_____________________________________________________________

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

    # [ PACMAN ]_______________________________________________________________

    msg(f'just wait', color='green')
    msg(f'MODE IS {mode}', color='green')
    pacman(mode)
    msg(f'just wait', color='green')
    

    # [ YAY ]__________________________________________________________________

    if mode == 'beast':
        msg(":: Installing YAY...", color='green')
        execute(f"git clone https://aur.archlinux.org/yay.git", cwd='/opt')
        execute(f"chown -R {user}:users /opt/yay")
        execute(f"su {user} -c 'makepkg -si --needed --noconfirm'", cwd='/opt/yay')

        msg(f":: Installing AUR packages...", color='green')
        pkgs_list = ' '.join(packages('yay'))
        _yay = execute(f"sudo -u {user} /bin/bash -c 'yay -S --noconfirm {pkgs_list}'")
        if _yay.returncode == 0:
            msg('YAY!!', color='green')

    # [ SDDM ]_________________________________________________________________

    if mode == 'beast':
        shutil.copy(os.path.join(localEGO, 'global', 'etc', 'sddm.conf'), '/etc/sddm.conf')
        copy_recursive(os.path.join(localEGO, 'global', 'usr', 'share', 'sddm'), '/usr/share/')

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

# { FIN }______________________________________________________________________

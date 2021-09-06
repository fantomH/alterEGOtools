#!/usr/bin/env python

## { alterEGO Linux: "Open the vault of knowledge" }---------------------------
##
## ego.py
##   created        : 2021-06-05 00:03:38 UTC
##   updated        : 2021-09-06 14:38:31 UTC
##   description    : Deploy and update alterEGO Linux.
## ____________________________________________________________________________

#### https://bit.ly/2SlqWzt
#### https://tiny.cc/alterEGO

import argparse
from collections import namedtuple
import os
import shlex
import shutil
import subprocess
import sys
import threading
import time

## { GLOBAL VARIABLES }________________________________________________________

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
        'alsa-utils':               'nice',
        'arp-scan':                 'hack',
        'base':                     'minimal',
        'base-devel':               'minimal',
        'bash-completion':          'minimal',
        'bat':                      'nice',
        'bc':                       'minimal',
        'bind':                     'nice',
        'binwalk':                  'hack',
        'bleachbit':                'nice',
        'brave-bin':                'aur-nice',
        'burpsuite':                'aur-hack',
        'cmatrix':                  'hack',
        'code':                     'nice',
        'cronie':                   'minimal',
        'dirbuster':                'aur-hack',
        'docker':                   'hack',
        'dos2unix':                 'minimal',
        'entr':                     'nice',
        'exfat-utils':              'nice',
        'feh':                      'nice',
        'ffmpeg':                   'nice',
        'firefox':                  'nice',
        'freerdp':                  'nice',
        'fzf':                      'minimal',
        'gimp':                     'nice',
        'git':                      'minimal',
        'gnu-netcat':               'hack',
        'go':                       'nice',
        'gobuster-git':             'aur-hack',
        'gromit-mpx-git':           'aur-nice',
        'grub':                     'minimal',
        'htop':                     'nice',
        'i3-gaps':                  'nice',
        'imagemagick':              'nice',
        'inkscape':                 'nice',
        'inxi':                     'aur-nice',
        'john':                     'hack',
        'jq':                       'nice',
        'jre11-openjdk':            'hack',
        'libreoffice-fresh':        'nice',
        'librespeed-cli-bin':       'aur-nice',
        'linux':                    'minimal',
        'lynx':                     'minimal',
        'man-db':                   'minimal',
        'man-pages':                'minimal',
        'mariadb-clients':          'hack',
        'metasploit':               'hack',
        'mlocate':                  'nice',
        'mtools':                   'nice',
        'mtr':                      'hack',
        'net-tools':                'hack',
        'networkmanager':           'minimal',
        'nfs-utils':                'nice',
        'nikto':                    'hack',
        'nmap':                     'nice',
        'notify-osd':               'nice',
        'ntfs-3g':                  'nice',
        'openssh':                  'minimal',
        'openvpn':                  'minimal',
        'p7zip':                    'minimal',
        'pandoc-bin':               'aur-nice',
        'pavucontrol':              'nice',
        'perl-image-exiftool':      'hack',
        'php':                      'hack',
        'polkit-gnome':             'nice',
        'postgresql':               'hack',
        'powershell-bin':           'aur-nice',
        'pptpclient':               'nice',
        'pulseaudio':               'nice',
        'pv':                       'nice',
        'python-beautifulsoup4':    'hack',
        'python-pandas':            'hack',
        'python-pip':               'nice',
        'python-pyaml':             'hack',
        'python-rich':              'hack',
        'qrencode':                 'hack',
        'qtile':                    'nice',
        'ranger':                   'nice',
        'remmina':                  'nice',
        'rsync':                    'minimal',
        'rustscan':                 'aur-hack',
        'screen':                   'nice',
        'screenkey':                'nice',
        #'sddm':                     'nice',
        'shellcheck':               'nice',
        'simple-mtpfs':             'aur-nice',
        'sqlitebrowser':            'hack',
        'sxiv':                     'nice',
        'tcpdump':                  'hack',
        'tesseract':                'hack',
        'tesseract-data-eng':       'hack',
        'tesseract-data-fra':       'hack',
        'thunar':                   'nice',
        'thunar-volman':            'nice',
        'tidy':                     'hack',
        'tk':                       'hack',
        'tmux':                     'minimal',
        'traceroute':               'hack',
        'transmission-gtk':         'nice',
        'tree':                     'minimal',
        'ufw':                      'minimal',
        'unrar':                    'minimal',
        'unzip':                    'minimal',
        'vim':                      'minimal',
        'virtualbox-guest-utils':   'nice',
        'w3m':                      'nice',
        'wfuzz-git':                'aur-hack',
        'wget':                     'minimal',
        'whois':                    'hack',
        'wireshark-qt':             'hack',
        'xclip':                    'nice',
        'xcompmgr':                 'nice',
        'xdotool':                  'nice',
        'xfce4-terminal':           'nice',
        'xorg-server':              'nice',
        'xorg-xinit':               'nice',
        'xterm':                    'nice',
        'youtube-dl':               'nice',
        'zathura':                  'nice',
        'zathura-pdf-mupdf':        'nice',
        'zbar':                     'hack',
        }

GitOption = namedtuple('GitOption', ['name', 'remote', 'local', 'mode'])
git_repositories = [
    GitOption('alterEGOtools', 'https://github.com/fantomH/alterEGOtools.git', '/usr/local/alterEGOtools', ['minimal', 'niceguy', 'beast']),
    GitOption('alterEGO', 'https://github.com/fantomH/alterEGO.git', '/usr/local/alterEGO', ['minimal', 'niceguy', 'beast']),
                        ]

## { UTIL FUNCTIONS }__________________________________________________________

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

    if not os.path.exists(dst):
        os.makedirs(dst)

    Msg.console(f"{_green}[*]{_RESET} {_bold}Copying files to {dst}...", wait=5)

    for src_dir, dirs, files in os.walk(src):
        dst_dir = src_dir.replace(src, dst)
        if not os.path.exists(dst_dir):
            os.mkdir(dst_dir)
            Msg.console(f"{_blue}[-]{_RESET} {_bold}Creating directory {dst_dir}.", wait=5)

        for f in files:
            src_file = os.path.join(src_dir, f)
            dst_file = os.path.join(dst_dir, f)
            Msg.console(f"{_blue}[-]{_RESET} {_bold}Copying {dst_file}.", wait=5)

            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.copy2(src_file, dst_file)

def execute(cmd, cwd=None, shell=False, text=True, input=None):

    if shell == True:
        cmd_list = cmd
    else:
        cmd_list = shlex.split(cmd)
    if input:
        input = input.encode()
        
    cmd_run = subprocess.run(cmd_list, cwd=cwd, shell=shell, input=input)

    CommandResults = namedtuple('CommandResults', ['returncode'])
    return CommandResults(cmd_run.returncode)

class Msg:

    def color(color='white'):
        colors = {
            'reset': '\033[00m',
            'bold': '\033[1m',
            'underline': '\033[4m',
            'dim': '\033[2m',
            'strickthrough': '\033[9m',
            'blink': '\033[5m',
            'reverse': '\033[7m',
            'hidden': '\033[8m',
            'normal': '\033[0m',
            'black': '\033[30m',
            'red': '\033[31m',
            'green': '\033[32m',
            'orange': '\033[33m',
            'blue': '\033[34m',
            'purple': '\033[35m',
            'aqua': '\033[36m',
            'gray': '\033[37m',
            'darkgray': '\033[90m',
            'lightred': '\033[91m',
            'lightgreen': '\033[92m',
            'lightyellow': '\033[93m',
            'lightblue': '\033[94m',
            'lightpurple': '\033[95m',
            'lightaqua': '\033[96m',
            'white': '\033[97m',
            'default': '\033[39m',
            'bgblack': '\033[40m',
            'bgred': '\033[41m',
            'bggreen': '\033[42m',
            'bgorange': '\033[43m',
            'bgblue': '\033[44m',
            'bgpurple': '\033[45m',
            'bgaqua': '\033[46m',
            'bggray': '\033[47m',
            'bgdarkgray': '\033[100m',
            'bglightred': '\033[101m',
            'bglightgreen': '\033[102m',
            'bglightyellow': '\033[103m',
            'bglightblue': '\033[104m',
            'bglightpurple': '\033[105m',
            'bglightaqua': '\033[106m',
            'bgwhite': '\033[107m',
            'bgdefault': '\033[49m',
            }

        return colors.get(color)

    def console(message, wait=5):
        print(message + Msg.color('reset'))
        time.sleep(wait)

_blue = Msg.color('lightblue')
_green = Msg.color('lightgreen')
_bold = Msg.color('bold')
_RESET = Msg.color('reset')

## { INSTALLER FUNCTIONS }_____________________________________________________

def packages(required_by, mode=None):

    if required_by == 'pacstrap':
        if mode == 'minimal':
            pkgs_list = [k for k, v in pkgs.items() if v in ['minimal']]
        elif mode == 'niceguy':
            pkgs_list = [k for k, v in pkgs.items() if v in ['minimal', 'nice']]
        elif mode == 'beast':
            pkgs_list = [k for k, v in pkgs.items() if v in ['minimal', 'nice', 'hack']]
    elif required_by == 'yay':
        if mode == 'niceguy':
            pkgs_list = [k for k, v in pkgs.items() if v in ['aur-nice']]
        elif mode == 'beast':
            pkgs_list = [k for k, v in pkgs.items() if v in ['aur-nice', 'aur-hack']]

    return pkgs_list

def shared_bin():
    #### Deploys applications.

    localEGO_bin = f"{localEGO}/bin"
    files = os.listdir(localEGO_bin)

    Msg.console(f"{_green}[*]{_RESET} {_bold}Deploying application to /usr/local/bin...", wait=5)
    for f in files:
        Msg.console(f"{_blue}[-]{_RESET} {_bold}{f}", wait=5)
        src = os.path.join(localEGO_bin, f)
        dst = os.path.join('/usr/local/bin', f)
        os.symlink(src, dst)

def shared_resources():
    # -- TODO: All file copying should be one functions.
    # .. recursive, copy, symlinks...

    ## [ bookmarks.db ]

    f = 'bookmarks.db'
    Msg.console(f"{_green}[*]{_RESET} {_bold}Deploying {f} to /usr/local/share...", wait=5)
    src = os.path.join(localEGO, 'share', f)
    dst = os.path.join('/usr/local/share', f)
    os.symlink(src, dst)

def shared_reverse_shell():
    #### Deploys reverse shells.

    if not os.path.exists('/usr/local/share/reverse_shell'):
        os.mkdir('/usr/local/share/reverse_shell')

    localEGO_reverse_shell = f"{localEGO}/share/reverse_shell"
    files = os.listdir(localEGO_reverse_shell)

    Msg.console(f"{_green}[*]{_RESET} {_bold}Deploying application to /usr/local/share/reverse_shell...", wait=5)
    for f in files:
        Msg.console(f"{_blue}[-]{_RESET} {_bold}{f}", wait=1)
        src = os.path.join(localEGO_reverse_shell, f)
        dst = os.path.join('/usr/local/share/reverse_shell', f)
        os.symlink(src, dst)

def shared_wordlist():
    #### Deploys wordlists.

    if not os.path.exists('/usr/local/share/wordlist'):
        os.mkdir('/usr/local/share/wordlist')

    localEGO_wordlist = f"{localEGO}/share/wordlist"
    files = os.listdir(localEGO_wordlist)

    Msg.console(f"{_green}[*]{_RESET} {_bold}Deploying wordlist to /usr/local/share/wordlist...", wait=5)
    for f in files:
        Msg.console(f"{_blue}[-]{_RESET} {_bold}{f}", wait=5)
        src = os.path.join(localEGO_wordlist, f)
        dst = os.path.join('/usr/local/share/wordlist', f)
        os.symlink(src, dst)

## { INSTALLER }_______________________________________________________________

class Installer:

    def __init__(self, mode):
        self.mode = mode

    def partition(self):
        ## [ CREATE PARTITION ]
        Msg.console(f"{_green}[*]{_RESET} {_bold}Creating and mounting the partition...", wait=5)
        partition = '''label: dos
                    device: /dev/sda
                    unit: sectors
                    sector-size: 512

                    /dev/sda1 : start=        2048, type=83, bootable
                    '''

        execute(f"sfdisk /dev/sda", input=partition)

        ## [ FORMAT FILE SYSTEM ]
        Msg.console(f"{_green}[*]{_RESET} {_bold}Formating the file system...", wait=5)
        execute(f"mkfs.ext4 /dev/sda1")

    def mount(self):
        ## [ MOUNT /dev/sda1 TO /mnt ]
        Msg.console(f"{_green}[*]{_RESET} {_bold}Mounting /dev/sda1 to /mnt...", wait=5)
        execute(f"mount /dev/sda1 /mnt")

        ## [ CREATE ${HOME} ]
        Msg.console(f"{_green}[*]{_RESET} {_bold}Creating /home...", wait=5)
        os.mkdir('/mnt/home')

    def mod_pacman_conf(self):
        #### Enabling ParallelDownloads in pacman.conf
        pacman_conf = '/etc/pacman.conf'
        pacman_conf_bkp = pacman_conf + '.bkp'
        shutil.move(pacman_conf, pacman_conf_bkp)
        with open(pacman_conf_bkp, 'r') as fin:
            with open(pacman_conf, 'w') as fout:
                for line in fin.readlines():
                    if "#ParallelDownloads = 5" in line:
                        fout.write(line.replace("#ParallelDownloads = 5", "ParallelDownloads = 5"))
                    else:
                        fout.write(line)
        os.remove(pacman_conf_bkp)

    def pacstrap(self):

        execute(f"rm -rf /var/lib/pacman/sync")
        execute(f"curl -o /etc/pacman.d/mirrorlist 'https://archlinux.org/mirrorlist/?country=US&protocol=http&protocol=https&ip_version=4'")
        execute(f"sed -i -e 's/\#Server/Server/g' /etc/pacman.d/mirrorlist")
        execute(f"pacman -Syy --noconfirm archlinux-keyring")

        Msg.console(f"{_green}[*]{_RESET} {_bold}Starting pacstrap...", wait=5)
        pkgs_list = ' '.join(packages('pacstrap', self.mode))
        Msg.console(f"{_blue}[-]{_RESET} {_bold}Will install:\n{pkgs_list}", wait=5)
        run_pacstrap = execute(f"pacstrap /mnt {pkgs_list}")
        Msg.console(f"{_blue}[-]{_RESET} {_bold}Pacstrap exit code: {run_pacstrap.returncode}", wait=5)

        return run_pacstrap.returncode


    def fstab(self):
        Msg.console(f"{_green}[*]{_RESET} {_bold}Generating the fstab...", wait=5)
        execute(f"genfstab -U /mnt >> /mnt/etc/fstab", shell=True)

    def chroot(self):
        Msg.console(f"{_green}[*]{_RESET} {_bold}Preparing arch-root...", wait=2)
        shutil.copy('/root/ego.py', '/mnt/root/ego.py')

        #### Moves to chroot to configure the new system.
        if self.mode == 'minimal':
            execute(f'arch-chroot /mnt python /root/ego.py --sysconfig minimal')
        elif self.mode == 'niceguy':
            execute(f'arch-chroot /mnt python /root/ego.py --sysconfig niceguy')
        elif self.mode == 'beast':
            execute(f'arch-chroot /mnt python /root/ego.py --sysconfig beast')

    def pull_git(self):

        Msg.console(f"{_green}[*]{_RESET} {_bold}Fetching AlterEGO tools, config and other stuff...", wait=5)

        for g in git_repositories:
            if self.mode in g.mode:
                Msg.console(f"{_blue}[-]{_RESET} {_bold}Pulling {g.remote}.", wait=5)
                if not os.path.isdir(g.local):
                    execute(f"git clone {g.remote} {g.local}")
                else:
                    execute(f"git -C {g.local} pull")

    def set_time(self):
        Msg.console(f"{_green}[*]{_RESET} {_bold}Setting clock and timezone...", wait=5)

        os.symlink(f'/usr/share/zoneinfo/{timezone}', '/etc/localtime')
        execute(f'timedatectl set-ntp true')
        execute(f'hwclock --systohc --utc')

    def set_locale(self):
        Msg.console(f"{_green}[*]{_RESET} {_bold}Generating locale...", wait=5)

        execute(f'sed -i "s/#en_US.UTF-8/en_US.UTF-8/" /etc/locale.gen')
        with open('/etc/locale.conf', 'w') as locale_conf:
            locale_conf.write('LANG=en_US.UTF-8')
        os.putenv('LANG', 'en_US.UTF-8')
        execute(f'locale-gen')

    def set_network(self):
        Msg.console(f"{_green}[*]{_RESET} {_bold}Setting up network...", wait=5)

        with open('/etc/hostname', 'w') as etc_hostname:
            etc_hostname.write(hostname)
        with open('/etc/hosts', 'w') as etc_hosts:
            etc_hosts.write(f'''
                            127.0.0.1	localhost
                            ::1		localhost
                            127.0.1.1	{hostname}.localdomain	{hostname}
                            ''')

        Msg.console(f"{_blue}[-]{_RESET} {_bold}Enabling NetworkManager daemon...", wait=5)
        execute(f'systemctl enable NetworkManager.service')

    def skel(self):
        if self.mode == 'beast' or self.mode == 'niceguy':
            Msg.console(f"{_green}[*]{_RESET} {_bold}Populating /etc/skel...", wait=5)
            src = f"{localEGO}/config/"
            dst = f"/etc/skel/"
            copy_recursive(src, dst)

    def users(self):
        Msg.console(f"{_green}[*]{_RESET} {_bold}Configuring users and passwords...", wait=5)
        Msg.console(f"{_blue}[-]{_RESET} {_bold}Setting password for root user.", wait=5)
        execute(f"passwd", input=f'{root_passwd}\n{root_passwd}\n')

        if self.mode == 'beast' or self.mode == 'niceguy':
            Msg.console(f"{_blue}[-]{_RESET} {_bold}Creating user {user}", wait=5)
            execute(f"useradd -m -g users -G wheel,docker {user}") 
            Msg.console(f"{_blue}[-]{_RESET} {_bold}Setting password for {user}", wait=5)
            execute(f"passwd {user}", input=f"{user_passwd}\n{user_passwd}\n")

            Msg.console(f"{_blue}[-]{_RESET} {_bold}Enabling sudoers for {user}", wait=5)
            execute(f'sed -i "s/# %wheel ALL=(ALL) NOPASSWD: ALL/%wheel ALL=(ALL) NOPASSWD: ALL/" /etc/sudoers')

    def shared_resources(self):
        if self.mode == 'beast':
            Msg.console(f"{_green}[*]{_RESET} {_bold}Deploying shared resources...", wait=5)
            shared_resources()
            shared_bin()
            shared_wordlist()
            shared_reverse_shell()
            # -- assets
            copy_recursive(os.path.join(localEGO, 'share', 'assets'), os.path.join(usr_local, 'share', 'assets'))
            # -- backgrounds
            copy_recursive(os.path.join(localEGO, 'share', 'backgrounds'), os.path.join(usr_local, 'share', 'backgrounds'))

    def swapfile(self):
        Msg.console(f"{_green}Creating a 1G swapfile...", wait=5)

        execute(f"fallocate -l 1G /swapfile")
        os.chmod('/swapfile', 0o600)
        execute(f"mkswap /swapfile")
        execute(f"swapon /swapfile")

        with open('/etc/fstab', 'a') as swap_file:
            swap_file.write("/swapfile none swap defaults 0 0")

    def aur(self):
        if self.mode == 'niceguy' or self.mode == 'beast':
            Msg.console(f"{_green}[*]{_RESET} {_bold}Installing YAY...", wait=5)
            execute(f"git clone https://aur.archlinux.org/yay.git", cwd='/opt')
            execute(f"chown -R {user}:users /opt/yay")
            execute(f"su {user} -c 'makepkg -si --needed --noconfirm'", cwd='/opt/yay')

            Msg.console(f"{_green}[*]{_RESET} {_bold}Installing AUR packages...", wait=5)
            pkgs_list = ' '.join(packages('yay', mode=self.mode))
            Msg.console(f"{_blue}[-]{_RESET} {_bold}Will be installed:\n{pkgs_list}", wait=5)
            execute(f"sudo -u {user} /bin/bash -c 'yay -S --noconfirm {pkgs_list}'")

    def mandb(self):
        Msg.console(f"{_green}[*]{_RESET} {_bold}Generating mandb...", wait=5)
        execute(f"mandb")

    def set_java(self):
        #### Burpsuite not running with java 16.
        #### Will need to install jre11-openjdk.
        #### $ sudo archlinux-java set java-11-openjdk

        if self.mode == 'beast':
            Msg.console(f"{_green}[*]{_RESET} {_bold}Fixing Java...", wait=5)
            execute(f"archlinux-java set java-11-openjdk")

    def bootloader(self):
        Msg.console(f"{_green}[*]{_RESET} {_bold}Installing and configuring the bootloader...", wait=5)
        execute(f'grub-install /dev/sda')
        execute(f'grub-mkconfig -o /boot/grub/grub.cfg')

    def vbox_services(self):
        if self.mode == 'beast' or self.mode == 'niceguy':
            Msg.console(f"{_green}[*]{_RESET} {_bold}Starting vbox service...", wait=5)
            execute(f'systemctl start vboxservice.service')
            execute(f'systemctl enable vboxservice.service')


class HackerLab:

    def __init__(self, mode):
        self.mode = mode

    def is_hacker(self):
        pass

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--install", type=str, choices=['minimal', 'niceguy', 'beast'], help="Install AlterEGO Linux.")
    parser.add_argument("--post-mount", type=str, choices=['minimal', 'niceguy', 'beast'], help="Run on /mnt.")
    parser.add_argument("--sysconfig", type=str, choices=['minimal', 'niceguy', 'beast'], help="Initiate the system configuration after the Installer.")
    parser.add_argument("--rerun", type=str, help="Until I figure out things...")

    args = parser.parse_args()

    ## { PARTITION SET UP }____________________________________________________

    if args.install:
        mode = args.install
        Msg.console(f"{_green}[*]{_RESET} {_bold}This will install AlterEGO Linux in {mode} mode...", wait=3)

        installer = Installer(mode)

        installer.partition()
        installer.mount()
        installer.mod_pacman_conf()

        #### Temporary solution due to few failure.
        run_pacstrap = installer.pacstrap()
        while run_pacstrap != 0:
            if input(f"{_blue}[-]{_RESET} {_bold}Re-run pacstrap [Y/n]? {_RESET}").lower() in ['y', 'yes']:
                run_pacstrap = installer.pacstrap()
            else:
                break
        installer.fstab()
        installer.chroot()

        # [ ALL DONE ]

        #### Returns from chroot.
        all_done = input(f"{_green}[*]{_RESET} {_bold}Shutdown [Y/n]? ")
        if all_done.lower() in ['y', 'yes']:
            Msg.console(f"{_blue}[-]{_RESET} {_bold}Good Bye!", wait=1)
            try:
                execute(f'umount -R /mnt')
                execute(f'shutdown now') 
            except:
                execute(f'shutdown now') 
        else:
            Msg.console(f"{_blue}[-]{_RESET} {_bold}Do a manual shutdown when ready.", wait=1)

    ## { SYSTEM CONFIGURATION }________________________________________________

    if args.sysconfig:
        mode = args.sysconfig
        installer = Installer(mode)

        # [ PACMAN ]

        ### Enabling ParallelDownloads in pacman.conf
        # pacman_conf = '/etc/pacman.conf'
        # pacman_conf_bkp = pacman_conf + '.bkp'
        # shutil.move(pacman_conf, pacman_conf_bkp)
        # with open(pacman_conf_bkp, 'r') as fin:
            # with open(pacman_conf, 'w') as fout:
                # for line in fin.readlines():
                    # if "#ParallelDownloads = 5" in line:
                        # fout.write(line.replace("#ParallelDownloads = 5", "ParallelDownloads = 8"))
                    # else:
                        # fout.write(line)
        # os.remove(pacman_conf_bkp)

        # def pacman(mode):

            # pkgs_list = ' '.join(packages('pacman', mode))

            ### Re-install archlinux-keyring in case of corruption.
            # execute(f"pacman -S --noconfirm archlinux-keyring")
            # execute(f"pacman -Syy")

            # Msg.console(f"{_green}[*]{_RESET} {_bold}Starting pacman...", wait=5)
            # Msg.console(f"{_blue}[-]{_RESET} {_bold}Will install:\n{pkgs_list}", wait=5)
            # run_pacman = execute(f"pacman -Syu --noconfirm --needed {pkgs_list}")
            # Msg.console(f"{_blue}[-]{_RESET} {_bold}Pacman exit code: {run_pacman.returncode}", wait=5)

        # pacman(mode)

        ### Temporary solution due to few failure.
        # while True:
            # if input(f"{_green}[*]{_RESET} {_bold}Re-run pacman [Y/n]? {_RESET}").lower() in ['y', 'yes']:
                # pacman(mode)
            # else:
                # break

        ## [ GIT REPOSITORIES ]
        installer.pull_git()
        ## [ TIMEZONE & CLOCK ]
        installer.set_time()
        ## [ LOCALE ]
        installer.set_locale()
        ## [ NETWORK CONFIGURATION ]
        installer.set_network()
        ## [ POPULATING /etc/skel ]
        installer.skel()
        ## [ USERS and PASSWORDS ]
        installer.users()
        ## [ SHARED RESOURCES ]
        installer.shared_resources()
        ## [ SWAPFILE ]
        installer.swapfile()
        ## [ YAY ]
        installer.aur()

        ## [ SDDM ]

        #### Disabled for now. Still prefer to login in the traditional way.
        # if mode == 'beast':
            # Msg.console(f"{_green}[*]{_RESET} {_bold}Deploying sddm and starting the service...", wait=5)
            # shutil.copy(os.path.join(localEGO, 'global', 'etc', 'sddm.conf'), '/etc/sddm.conf')
            # copy_recursive(os.path.join(localEGO, 'global', 'usr', 'share', 'sddm'), '/usr/share/sddm')
            # execute(f'systemctl enable sddm.service')

        ## [ GENERATING mandb ]
        installer.mandb()
        ## [ SETTING JAVA DEFAULT ]
        installer.set_java()
        ## [ BOOTLOADER ]
        installer.bootloader()
        ## [ VIRTUALBOX SERVICES ]
        installer.vbox_services()

    ## { TESTING }_____________________________________________________________

    if args.rerun:
        eval(args.rerun)

if __name__ == '__main__':
    main()

## { FIN }_____________________________________________________________________

#!/usr/bin/env python

## { alterEGO Linux: "Open the vault of knowledge" }___________________________
##
## ego.py
##   created        : 2021-06-05 00:03:38 UTC
##   updated        : 2021-08-23 19:28:44 UTC
##   description    : Deploy and update alterEGO Linux.
## ____________________________________________________________________________

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
        'arp-scan':                 'full',
        'base':                     'minimal',
        'base-devel':               'minimal',
        'bat':                      'nice',
        'bc':                       'nice',
        'bind':                     'nice',
        'binwalk':                  'full',
        'bleachbit':                'nice',
        'brave-bin':                'aur',
        'burpsuite':                'aur',
        'cmatrix':                  'full',
        'code':                     'nice',
        'cronie':                   'nice',
        'dirbuster':                'aur',
        'dos2unix':                 'nice',
        'entr':                     'nice',
        'exfat-utils':              'nice',
        'feh':                      'nice',
        'ffmpeg':                   'nice',
        'firefox':                  'nice',
        'freerdp':                  'nice',
        'fzf':                      'minimal',
        'gimp':                     'nice',
        'git':                      'minimal',
        'gnu-netcat':               'nice',
        'go':                       'nice',
        'gobuster-git':             'aur',
        'gromit-mpx-git':           'aur',
        'grub':                     'minimal',
        'htop':                     'nice',
        'i3-gaps':                  'nice',
        'imagemagick':              'nice',
        'inkscape':                 'nice',
        'inxi':                     'aur',
        'john':                     'full',
        'jq':                       'nice',
        'jre11-openjdk':            'full',
        'libreoffice-fresh':        'nice',
        'librespeed-cli-bin':       'aur',
        'linux':                    'minimal',
        'lynx':                     'minimal',
        'man-db':                   'minimal',
        'man-pages':                'minimal',
        'mariadb-clients':          'full',
        'metasploit':               'full',
        'mlocate':                  'nice',
        'mtools':                   'nice',
        'mtr':                      'full',
        'net-tools':                'full',
        'networkmanager':           'minimal',
        'nfs-utils':                'nice',
        'nikto':                    'full',
        'nmap':                     'full',
        'notify-osd':               'nice',
        'ntfs-3g':                  'nice',
        'openssh':                  'minimal',
        'openvpn':                  'minimal',
        'p7zip':                    'full',
        'pandoc-bin':               'aur',
        'pavucontrol':              'nice',
        'perl-image-exiftool':      'full',
        'php':                      'full',
        'polkit-gnome':             'nice',
        'postgresql':               'full',
        'powershell-bin':           'aur',
        'pptpclient':               'nice',
        'pulseaudio':               'nice',
        'pv':                       'full',
        'python-beautifulsoup4':    'full',
        'python-pandas':            'full',
        'python-pip':               'nice',
        'python-pyaml':             'full',
        'python-rich':              'full',
        'qrencode':                 'full',
        'qtile':                    'nice',
        'ranger':                   'nice',
        'remmina':                  'nice',
        'rsync':                    'minimal',
        #'rustscan':                 'aur_cli_hack',
        'rustscan':                 'aur',
        'screen':                   'nice',
        'screenkey':                'full',
        #'sddm':                     'full',
        'shellcheck':               'nice',
        'simple-mtpfs':             'aur',
        'sqlitebrowser':            'full',
        'sxiv':                     'nice',
        'tcpdump':                  'full',
        'tesseract':                'full',
        'tesseract-data-eng':       'full',
        'tesseract-data-fra':       'full',
        'thunar':                   'nice',
        'thunar-volman':            'nice',
        'tidy':                     'full',
        'tk':                       'full',
        'tmux':                     'minimal',
        'traceroute':               'full',
        'transmission-gtk':         'full',
        'tree':                     'nice',
        'ufw':                      'minimal',
        'unrar':                    'minimal',
        'unzip':                    'minimal',
        'vim':                      'minimal',
        'virtualbox-guest-utils':   'nice',
        'w3m':                      'nice',
        'wfuzz-git':                'aur',
        'wget':                     'minimal',
        'whois':                    'full',
        'wireshark-qt':             'full',
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
        'zbar':                     'full',
        }

GitOption = namedtuple('GitOption', ['name', 'remote', 'local', 'mode'])
git_repositories = [

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

    Msg.console(f":: {_green}Copying files to {dst}...", wait=0)

    for src_dir, dirs, files in os.walk(src):
        dst_dir = src_dir.replace(src, dst)
        if not os.path.exists(dst_dir):
            os.mkdir(dst_dir)
            Msg.console(f" -> {_blue}Creating directory {dst_dir}.", wait=0)

        for f in files:
            src_file = os.path.join(src_dir, f)
            dst_file = os.path.join(dst_dir, f)
            Msg.console(f" -> {_blue}Copying {dst_file}.", wait=0)

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

def git(git_repository, local_directory):

    if not os.path.isdir(local_directory):
        execute(f"git clone {git_repository} {local_directory}")
    else:
        execute(f"git -C {local_directory} pull")

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

    def console(message, wait=0):
        print(message + Msg.color('reset'))
        time.sleep(wait)

_blue = Msg.color('lightblue')
_green = Msg.color('lightgreen')
_RESET = Msg.color('reset')

## { INSTALLER FUNCTIONS }_____________________________________________________

def packages(required_by, mode=None):

    if required_by == 'pacstrap':
        if mode == 'minimal':
            pkgs_list = [k for k, v in pkgs.items() if v in ['minimal']]
        elif mode == 'nice':
            pkgs_list = [k for k, v in pkgs.items() if v in ['minimal', 'nice']]
        elif mode == 'beast':
            pkgs_list = [k for k, v in pkgs.items() if v in ['minimal', 'nice', 'full']]
    elif required_by == 'yay':
            pkgs_list = [k for k, v in pkgs.items() if v in ['aur']]

    return pkgs_list

def shared_bin():
    #### Deploys applications.

    localEGO_bin = f"{localEGO}/bin"
    files = os.listdir(localEGO_bin)

    Msg.console(f":: {_green}Deploying application to /usr/local/bin...", wait=0)
    for f in files:
        Msg.console(f" -> {_blue}{f}", wait=0)
        src = os.path.join(localEGO_bin, f)
        dst = os.path.join('/usr/local/bin', f)
        os.symlink(src, dst)

def shared_resources():
    # -- TODO: All file copying should be one functions.
    # .. recursive, copy, symlinks...

    ## [ bookmarks.db ]

    f = 'bookmarks.db'
    Msg.console(f":: {_green}Deploying {f} to /usr/local/share...", wait=0)
    src = os.path.join(localEGO, 'share', f)
    dst = os.path.join('/usr/local/share', f)
    os.symlink(src, dst)

def shared_reverse_shell():
    #### Deploys reverse shells.

    if not os.path.exists('/usr/local/share/reverse_shell'):
        os.mkdir('/usr/local/share/reverse_shell')

    localEGO_reverse_shell = f"{localEGO}/share/reverse_shell"
    files = os.listdir(localEGO_reverse_shell)

    Msg.console(f":: {_green}Deploying application to /usr/local/share/reverse_shell...", wait=0)
    for f in files:
        Msg.console(f" -> {_blue}{f}", wait=1)
        src = os.path.join(localEGO_reverse_shell, f)
        dst = os.path.join('/usr/local/share/reverse_shell', f)
        os.symlink(src, dst)

def shared_wordlist():
    #### Deploys wordlists.

    if not os.path.exists('/usr/local/share/wordlist'):
        os.mkdir('/usr/local/share/wordlist')

    localEGO_wordlist = f"{localEGO}/share/wordlist"
    files = os.listdir(localEGO_wordlist)

    Msg.console(f":: {_green}Deploying application to /usr/local/share/wordlist...", wait=0)
    for f in files:
        Msg.console(f" -> {_blue}{f}", wait=0)
        src = os.path.join(localEGO_wordlist, f)
        dst = os.path.join('/usr/local/share/wordlist', f)
        os.symlink(src, dst)


## { INSTALLER }_______________________________________________________________

class Installer:

    def __init__(self, mode):
        self.mode = mode

    def partition(self):
        ## [ CREATE PARTITION ]
        Msg.console(f":: {_green}Creating and mounting the partition...", wait=0)
        partition = '''label: dos
                    device: /dev/sda
                    unit: sectors
                    sector-size: 512

                    /dev/sda1 : start=        2048, type=83, bootable
                    '''

        execute(f"sfdisk /dev/sda", input=partition)

        ## [ FORMAT FILE SYSTEM ]
        Msg.console(f":: {_green}Formating the file system...", wait=0)
        execute(f"mkfs.ext4 /dev/sda1")

    def mount(self):
        ## [ MOUNT /dev/sda1 TO /mnt ]
        Msg.console(f":: {_green}Mounting /dev/sda1 to /mnt...", wait=0)
        execute(f"mount /dev/sda1 /mnt")

        ## [ CREATE ${HOME} ]
        Msg.console(f":: {_green}Creating /home...", wait=0)
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
        execute(f"curl -o /etc/pacman.d/mirrorlist 'https://archlinux.org/mirrorlist/?country=CA&country=US&protocol=http&protocol=https&ip_version=4'")
        execute(f"sed -i -e 's/\#Server/Server/g' /etc/pacman.d/mirrorlist")
        execute(f"pacman -Syy --noconfirm archlinux-keyring")

        Msg.console(f":: {_green}Starting pacstrap...", wait=0)
        pkgs_list = ' '.join(packages('pacstrap', self.mode))
        Msg.console(f" -> {_blue}Will install:\n{pkgs_list}", wait=0)
        run_pacstrap = execute(f"pacstrap /mnt {pkgs_list}")
        Msg.console(f" -> {_blue}Pacstrap exit code: {run_pacstrap.returncode}", wait=0)

        #### Temporary solution due to few failure.
        while run_pacstrap.returncode != 0:
            if input(f":: {_green}Re-run pacstrap [Y/n]? {_RESET}").lower() in ['y', 'yes']:
                installer.pacstrap()
            else:
                break

    def fstab(self):
        Msg.console(f":: {_green}Generating the fstab...", wait=0)
        execute(f"genfstab -U /mnt >> /mnt/etc/fstab", shell=True)

    def chroot(self):
        Msg.console(f":: {_green}Preparing arch-root...", wait=2)
        shutil.copy('/root/ego.py', '/mnt/root/ego.py')

        #### Moves to chroot to configure the new system.
        if self.mode == 'minimal':
            execute(f'arch-chroot /mnt python /root/ego.py --sysconfig minimal')
        elif self.mode == 'nice':
            execute(f'arch-chroot /mnt python /root/ego.py --sysconfig nice')
        elif self.mode == 'beast':
            execute(f'arch-chroot /mnt python /root/ego.py --sysconfig beast')

    def set_time(self):
        Msg.console(f":: {_green}Setting clock and timezone...", wait=0)

        os.symlink(f'/usr/share/zoneinfo/{timezone}', '/etc/localtime')
        execute(f'timedatectl set-ntp true')
        execute(f'hwclock --systohc --utc')

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--install", type=str, choices=['minimal', 'nice', 'beast'], help="Install AlterEGO Linux.")
    parser.add_argument("--post-mount", type=str, choices=['minimal', 'nice', 'beast'], help="Run on /mnt.")
    parser.add_argument("--sysconfig", type=str, choices=['minimal', 'nice', 'beast'], help="Initiate the system configuration after the Installer.")
    parser.add_argument("--rerun", type=str, help="Until I figure out things...")

    args = parser.parse_args()

    ## { PARTITION SET UP }____________________________________________________

    if args.install:
        mode = args.install
        Msg.console(f":: {_green}This will install AlterEGO Linux in {mode} mode...", wait=3)

        installer = Installer(mode)

        installer.partition()
        installer.mount()

        installer.mod_pacman_conf()

        installer.pacstrap()

        installer.fstab()

        installer.chroot()

        # [ ALL DONE ]

        #### Returns from chroot.
        all_done = input(f":: {_green}Shutdown [Y/n]? ")
        if all_done.lower() in ['y', 'yes']:
            Msg.console(f" -> {_blue}Good Bye!", wait=1)
            try:
                execute(f'umount -R /mnt')
                execute(f'shutdown now') 
            except:
                execute(f'shutdown now') 
        else:
            Msg.console(f" -> {_blue}Do a manual shutdown when ready.", wait=1)

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

            # Msg.console(f":: {_green}Starting pacman...", wait=0)
            # Msg.console(f" -> {_blue}Will install:\n{pkgs_list}", wait=0)
            # run_pacman = execute(f"pacman -Syu --noconfirm --needed {pkgs_list}")
            # Msg.console(f" -> {_blue}Pacman exit code: {run_pacman.returncode}", wait=0)

        # pacman(mode)

        ### Temporary solution due to few failure.
        # while True:
            # if input(f":: {_green}Re-run pacman [Y/n]? {_RESET}").lower() in ['y', 'yes']:
                # pacman(mode)
            # else:
                # break

        ## [ GIT REPOSITORIES ]

        Msg.console(f":: {_green}Fetching AlterEGO tools, config and other stuff...", wait=0)

        Msg.console(f" -> {_blue}Pulling {gitTOOLS}.", wait=0)
        git(gitTOOLS, localTOOLS)

        if mode == 'beast' or mode == 'nice':
            Msg.console(f" -> {_blue}Pulling {gitEGO}.", wait=0)
            git(gitEGO, localEGO)

        ## [ TIMEZONE & CLOCK ]

        installer.set_time()

        ## [ LOCALE ]

        Msg.console(f":: {_green}Generating locale...", wait=0)

        execute(f'sed -i "s/#en_US.UTF-8/en_US.UTF-8/" /etc/locale.gen')
        with open('/etc/locale.conf', 'w') as locale_conf:
            locale_conf.write('LANG=en_US.UTF-8')
        os.putenv('LANG', 'en_US.UTF-8')
        execute(f'locale-gen')

        ## [ NETWORK CONFIGURATION ]

        Msg.console(f":: {_green}Setting up network...", wait=0)

        with open('/etc/hostname', 'w') as etc_hostname:
            etc_hostname.write(hostname)
        with open('/etc/hosts', 'w') as etc_hosts:
            etc_hosts.write(f'''
                            127.0.0.1	localhost
                            ::1		localhost
                            127.0.1.1	{hostname}.localdomain	{hostname}
                            ''')

        Msg.console(f" -> {_blue}Enabling NetworkManager daemon...", wait=0)
        execute(f'systemctl enable NetworkManager.service')

        ## [ POPULATING /etc/skel ]

        if mode == 'beast' or mode == 'nice':
            Msg.console(f":: {_green}Populating /etc/skel...", wait=0)
            src = f"{localEGO}/config/"
            dst = f"/etc/skel/"
            copy_recursive(src, dst)

        ## [ USERS and PASSWORDS ]

        Msg.console(f":: {_green}Configuring users and passwords...", wait=0)
        Msg.console(f" -> {_blue}Setting password for root user.", wait=0)
        execute(f"passwd", input=f'{root_passwd}\n{root_passwd}\n')

        if mode == 'beast' or mode == 'nice':
            Msg.console(f" -> {_blue}Creating user {user}", wait=0)
            execute(f"useradd -m -g users -G wheel {user}") 
            Msg.console(f" -> {_blue}Setting password for {user}", wait=0)
            execute(f"passwd {user}", input=f"{user_passwd}\n{user_passwd}\n")

            Msg.console(f" -> {_blue}Enabling sudoers for {user}", wait=0)
            execute(f'sed -i "s/# %wheel ALL=(ALL) NOPASSWD: ALL/%wheel ALL=(ALL) NOPASSWD: ALL/" /etc/sudoers')

        ## [ SHARED RESOURCES ]

        if mode == 'beast':
            Msg.console(f":: {_green}Deploying shared resources...", wait=0)
            shared_resources()
            shared_bin()
            shared_wordlist()
            shared_reverse_shell()
            # -- assets
            copy_recursive(os.path.join(localEGO, 'share', 'assets'), os.path.join(usr_local, 'share', 'assets'))
            # -- backgrounds
            copy_recursive(os.path.join(localEGO, 'share', 'backgrounds'), os.path.join(usr_local, 'share', 'backgrounds'))

        ## [ SWAPFILE ]

        Msg.console(f"{_green}Creating a 1G swapfile...", wait=0)

        execute(f"fallocate -l 1G /swapfile")
        os.chmod('/swapfile', 0o600)
        execute(f"mkswap /swapfile")
        execute(f"swapon /swapfile")

        with open('/etc/fstab', 'a') as swap_file:
            swap_file.write("/swapfile none swap defaults 0 0")

        ## [ YAY ]

        if mode == 'beast' or mode == 'nice':
            Msg.console(f":: {_green}Installing YAY...", wait=0)
            execute(f"git clone https://aur.archlinux.org/yay.git", cwd='/opt')
            execute(f"chown -R {user}:users /opt/yay")
            execute(f"su {user} -c 'makepkg -si --needed --noconfirm'", cwd='/opt/yay')

            Msg.console(f":: {_green}Installing AUR packages...", wait=0)
            pkgs_list = ' '.join(packages('yay'))
            Msg.console(f" -> {_blue}Will be installed:\n{pkgs_list}", wait=0)
            execute(f"sudo -u {user} /bin/bash -c 'yay -S --noconfirm {pkgs_list}'")

        ## [ SDDM ]

        #### Disabled for now. Still prefer to login in the traditional way.
        # if mode == 'beast':
            # Msg.console(f":: {_green}Deploying sddm and starting the service...", wait=5)
            # shutil.copy(os.path.join(localEGO, 'global', 'etc', 'sddm.conf'), '/etc/sddm.conf')
            # copy_recursive(os.path.join(localEGO, 'global', 'usr', 'share', 'sddm'), '/usr/share/sddm')
            # execute(f'systemctl enable sddm.service')

        ## [ GENERATING mandb ]

        Msg.console(f":: {_green}Generating mandb...", wait=0)
        execute(f"mandb")

        ## [ SETTING JAVA DEFAULT ]

        #### Burpsuite not running with java 16.
        #### Will need to install jre11-openjdk.
        #### $ sudo archlinux-java set java-11-openjdk

        if mode == 'beast':
            Msg.console(f":: {_green}Fixing Java...", wait=0)
            execute(f"archlinux-java set java-11-openjdk")

        ## [ BOOTLOADER ]

        Msg.console(f":: {_green}Installing and configuring the bootloader...", wait=0)
        execute(f'grub-install /dev/sda')
        execute(f'grub-mkconfig -o /boot/grub/grub.cfg')

        ## [ VIRTUALBOX SERVICES ]

        if mode == 'beast' or mode == 'nice':
            Msg.console(f":: {_green}Starting vbox service...", wait=0)
            execute(f'systemctl start vboxservice.service')
            execute(f'systemctl enable vboxservice.service')

    ## { TESTING }_____________________________________________________________

    if args.rerun:
        eval(args.rerun)

if __name__ == '__main__':
    main()

## { NOTES }___________________________________________________________________

    ## [ MODES ]
    #### MINIMAL <- CLI / BASIC only
    #### UNDERGROUND <- CLI / HACH
    #### - pac_cli_hack
    #### - aur_cli_hack
    

## { FIN }_____________________________________________________________________

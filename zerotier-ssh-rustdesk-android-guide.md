# ZeroTier + SSH (+ RustDesk) Setup Guide (Android <-> PC)

This guide explains how to securely access your desktop from Android over ZeroTier using SSH (Termux), with RustDesk as an optional remote desktop layer.

## 1) Create a ZeroTier network

1. Open [ZeroTier Central](https://my.zerotier.com/)
2. Sign in and click **Create A Network**
3. Copy your **Network ID** (16-hex string)

## 2) Install ZeroTier on PC (Ubuntu/Debian)

```bash
curl -s https://install.zerotier.com | sudo bash
sudo systemctl enable --now zerotier-one
sudo zerotier-cli join <YOUR_NETWORK_ID>
sudo zerotier-cli listnetworks
```

Then authorize the device in ZeroTier Central:

- Open your network -> `Members`
- Set `Auth` for your PC

Get PC ZeroTier IP:

```bash
ip -4 a | rg zt
```

## 3) Install ZeroTier on Android

1. Install **ZeroTier One** on Android
2. Open app -> **Join Network**
3. Paste `<YOUR_NETWORK_ID>`
4. In ZeroTier Central, set `Auth` for Android device

## 4) Set up SSH server on PC (recommended)

Install and start OpenSSH server:

```bash
sudo apt update
sudo apt install -y openssh-server
sudo systemctl enable --now ssh
sudo systemctl status ssh --no-pager
```

Optional: restrict SSH to your ZeroTier interface IP only (replace `<YOUR_ZT_IP>`):

```bash
printf '\n# Listen only on ZeroTier\nListenAddress <YOUR_ZT_IP>\n' | sudo tee -a /etc/ssh/sshd_config
sudo sshd -t && sudo systemctl restart ssh
```

Notes:

- Put `ListenAddress` in `/etc/ssh/sshd_config` (server config), not `/etc/ssh/ssh_config` (client config).
- If firewall is enabled, allow SSH (ideally on ZeroTier interface only).

## 5) Install SSH client in Termux (Android)

Install Termux from F-Droid/GitHub release (Play Store build is outdated), then:

```bash
pkg update && pkg upgrade -y
pkg install -y openssh
ssh -V
```

Generate key on Android:

```bash
ssh-keygen -t ed25519 -C "android-termux"
```

Copy key to PC:

```bash
cat ~/.ssh/id_ed25519.pub
```

Append that public key to PC `~/.ssh/authorized_keys`, then on PC:

```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

Optional Termux SSH host shortcut (`~/.ssh/config`):

```sshconfig
Host homepc
    HostName <YOUR_ZT_IP>
    User <YOUR_PC_USERNAME>
    Port 22
    IdentityFile ~/.ssh/id_ed25519
```

Connect from Termux:

```bash
ssh <YOUR_PC_USERNAME>@<YOUR_ZT_IP>
# or: ssh homepc
```

## 6) Install RustDesk on PC (optional, from GitHub)

RustDesk releases:

- [https://github.com/rustdesk/rustdesk/releases](https://github.com/rustdesk/rustdesk/releases)

Direct Ubuntu/Debian x86_64 .deb (example):

- [https://github.com/rustdesk/rustdesk/releases/download/1.4.6/rustdesk-1.4.6-x86_64.deb](https://github.com/rustdesk/rustdesk/releases/download/1.4.6/rustdesk-1.4.6-x86_64.deb)

Install:

```bash
wget -O /tmp/rustdesk.deb "https://github.com/rustdesk/rustdesk/releases/download/1.4.6/rustdesk-1.4.6-x86_64.deb"
sudo apt update
sudo apt install -y /tmp/rustdesk.deb || sudo apt -f install -y
```

Run:

```bash
rustdesk
```

In RustDesk settings:

- Set permanent password
- Enable unattended access
- Note RustDesk ID

## 7) Install RustDesk on Android (optional)

If Play Store app is unavailable in your region:

1. Open [RustDesk Releases](https://github.com/rustdesk/rustdesk/releases)
2. Download signed APK matching architecture (usually `aarch64`, file pattern `*-signed.apk`)
3. Install APK (enable "Install unknown apps" temporarily if needed)

## 8) Connect Android to PC

SSH path (recommended for terminal/dev work):

1. Ensure ZeroTier is connected on both devices
2. Open Termux on Android
3. Run `ssh <YOUR_PC_USERNAME>@<YOUR_ZT_IP>` (or `ssh homepc`)
4. Work directly in shell/tmux/neovim/CLI tools

RustDesk path (for full GUI desktop):

1. Ensure ZeroTier is connected on both devices
2. Open RustDesk on Android
3. Enter PC RustDesk ID
4. Enter your unattended password
5. Control desktop and use Cursor GUI

## 9) Security checklist

- Keep ZeroTier network private
- Authorize only your own devices
- Enable 2FA on ZeroTier account
- Prefer SSH keys over password auth
- Consider disabling SSH password auth after key login works
- Use strong RustDesk unattended password
- Keep desktop awake while remote session is needed


# BakeBot Setup Guide

This guide walks you through installing, configuring, and running BakeBot using the GUI.

## 1) Prerequisites
- Windows 10/11 (Linux/macOS also work)
- Python 3.10 or newer
- Twitch account for your bot

Optional (recommended)
- A Twitch Developer Application (to use OAuth Wizard easily)
- A virtual environment (venv)

## 2) Install
1. Open PowerShell in the project folder
2. Create and activate a virtual environment (optional)
   - `py -3 -m venv .venv`
   - `.\.venv\Scripts\Activate`
3. Install dependencies
   - `pip install -r requirements.txt`

## 3) Launch the GUI
- `python -m bot.gui`
- Your browser opens to `http://127.0.0.1:5000`

If it doesn’t open, copy the URL from the terminal.

## 4) Get a Twitch Chat Token
- Click “OAuth Wizard” in the top nav.
- Approve the scopes `chat:read` and `chat:edit`.
- The GUI will capture the token (you can paste it manually if needed).

## 5) Configure
Open the Configuration tab and set:
- Twitch OAuth Token: `oauth:xxxxxx`
- Twitch Channel: your channel name (lowercase)
- Optional:
  - `PREFIX` (default `!`)
  - `WEB_HOST` (use `0.0.0.0` for LAN/public, `127.0.0.1` for local only)
  - `WEB_PORT` (default `8080`)
  - `PUBLIC_BASE_URL` (after you port-forward or set up a tunnel)

Click “Save Configuration”.

## 6) Start the Bot
- Go to the Control tab and click “Start Bot”.
- Watch the status pill and the Logs page for progress.

## 7) Open Leaderboard
- Click “Open Leaderboard” or visit `http://localhost:8080/leaderboard`.

## 8) Share Publicly (optional)
- Either port-forward your router or use a tunnel (ngrok/cloudflared).
- Then set `PUBLIC_BASE_URL` in the GUI so the bot shares the public link.

Next steps
- See [Commands](./COMMANDS.md) for a full command list.
- See [Web & Hosting](./WEB.md) for public hosting options.
- See [Troubleshooting](./TROUBLESHOOTING.md) for common fixes.

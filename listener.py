import os
import subprocess
from wakeonlan import send_magic_packet
from telethon import TelegramClient, events
# ADDED GROUP_ID TO THE IMPORT BELOW
from config import API_ID, API_HASH, PC_MAC, PC_IP, GROUP_ID 
import commands as cmd

# === TELEGRAM CLIENT ===
client = TelegramClient("tablet_session", API_ID, API_HASH)

# === PC POWER & RESTART ===
def wake_pc():
    send_magic_packet(PC_MAC)
    print(f"🟢 {cmd.WAKE_PC} successful")
    return "✅ Magic Packet sent!"

def restart_pc():
    print(f"🔄 {cmd.RESTART_PC} triggered")
    return "🔄 Restarting PC..."

def sleep_pc():
    print(f"😴 {cmd.SLEEP_PC} triggered")
    return "😴 Putting PC to sleep..."

# === SYSTEM CONTROL ===
def lock_pc():
    print(f"🔒 {cmd.LOCK_PC} triggered")
    return "🔒 PC Locked"

def logoff_pc():
    print(f"👤 {cmd.LOGOFF_PC} triggered")
    return "👤 Logging off user..."

# === SYSTEM INFO ===
def ping_pc():
    # Use -c 1 for Linux/Termux
    status = os.system(f"ping -c 1 {PC_IP} > /dev/null 2>&1")
    return "🖥️ PC is Online" if status == 0 else "🌑 PC is Offline"

# === APP/GAME LAUNCHES ===
def run_steam():
    print(f"🎮 {cmd.RUN_STEAM} triggered")
    return "🚀 Launching Steam..."

def run_gta():
    print(f"🚗 {cmd.RUN_GTA} triggered")
    return "🚀 Launching GTA V..."

# === AUTOMATION ===
def run_backup():
    print(f"📂 {cmd.RUN_BACKUP} triggered")
    return "📂 Starting Backup script..."

# === MESSAGE HANDLER ===
@client.on(events.NewMessage(chats=GROUP_ID))
async def handler(event):
    # SAFETY: Only respond if the message is from YOU
    sender = await event.get_sender()
    me = await client.get_me()
    
    if sender.id != me.id:
        return

    msg = event.raw_text.lower().strip()
    reply = None

    # Routing logic
    if msg == cmd.WAKE_PC:
        reply = wake_pc()
    elif msg == cmd.PC_STATUS:
        reply = ping_pc()
    elif msg == cmd.SLEEP_PC:
        reply = sleep_pc()
    elif msg == cmd.RESTART_PC:
        reply = restart_pc()
    elif msg == cmd.LOCK_PC:
        reply = lock_pc()
    elif msg == cmd.LOGOFF_PC:
        reply = logoff_pc()
    elif msg == cmd.RUN_STEAM:
        reply = run_steam()
    elif msg == cmd.RUN_GTA:
        reply = run_gta()
    elif msg == cmd.RUN_BACKUP:
        reply = run_backup()
    elif msg == cmd.PING:
        reply = "pong"
    else:
        reply = f"❓ Unknown command: {msg}"

    if reply:
        await event.reply(reply)

# === START LISTENER ===
print(f"📡 Tablet listener active. Monitoring Group ID: {GROUP_ID}")
client.start()
client.run_until_disconnected()
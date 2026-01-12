import os
import subprocess
from wakeonlan import send_magic_packet
from telethon import TelegramClient, events
from config import API_ID, API_HASH, PC_MAC, PC_IP, GROUP_ID 
import commands as cmd
import requests

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
    try:
        requests.get(f"http://{PC_IP}:5000/sleep", timeout=3)
        return "😴 Sleep command sent to PC!"
    except:
        return "❌ PC is not responding (Is the receiver script running?)"

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
def launch_steam():
    try:
        # The tablet just "calls" the PC's office
        requests.get(f"http://{PC_IP}:5000/steam", timeout=3)
        return "🎮 Launching Steam on PC..."
    except:
        return "❌ PC unreachable"

def run_gta():
    print(f"🚗 {cmd.RUN_GTA} triggered")
    return "🚀 Launching GTA V..."

def launch_roboquest():
    requests.get(f"http://{PC_IP}:5000/roboquest", timeout=3)
    return "🤖 Booting Roboquest..."

def launch_strinova():
    requests.get(f"http://{PC_IP}:5000/strinova", timeout=3)
    return "☄️ Launching Strinova..."

def launch_l4d2():
    requests.get(f"http://{PC_IP}:5000/l4d2", timeout=3)
    return "🧟 Opening Left 4 Dead 2..."

def launch_l4d():
    requests.get(f"http://{PC_IP}:5000/l4d", timeout=3)
    return "🧟 Opening Left 4 Dead 1..."

def launch_kovaaks():
    requests.get(f"http://{PC_IP}:5000/kovaaks", timeout=3)
    return "🎯 Practice time: Kovaak's..."

def launch_darksouls():
    requests.get(f"http://{PC_IP}:5000/darksouls", timeout=3)
    return "🔥 Prepare to Die: Dark Souls..."

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
        reply = launch_steam()
    elif msg == cmd.RESTART_PC:
        reply = restart_pc()
    elif msg == cmd.RUN_GTA:
        reply = run_gta()
    elif msg == "run roboquest":
        reply = launch_roboquest()
    elif msg == "run strinova":
        reply = launch_strinova()
    elif msg == "run l4d2":
        reply = launch_l4d2()
    elif msg == "run l4d":
        reply = launch_l4d()
    elif msg == "run kovaaks":
        reply = launch_kovaaks()
    elif msg == "run dark souls":
        reply = launch_darksouls()
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
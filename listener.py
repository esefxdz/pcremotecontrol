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
    try:
        requests.get(f"http://{PC_IP}:5000/restart", timeout=3)
        return "🔄 Restart command sent to PC!"
    except:
        return "❌ PC unreachable"

def sleep_pc():
    try:
        requests.get(f"http://{PC_IP}:5000/sleep", timeout=3)
        return "😴 Sleep command sent to PC!"
    except:
        return "❌ PC is not responding (Is the receiver script running?)"

# === SYSTEM INFO ===
def ping_pc():
    try:
        response = requests.get(f"http://{PC_IP}:5000/status", timeout=2)
        if response.status_code == 200:
            return "🖥️ PC is Online (Receiver Active)"
        return "⚠️ PC is ON but Receiver is Closed"
    except:
        return "🌑 PC is Offline"

# === APP/GAME LAUNCHES ===
def launch_steam():
    try:
        requests.get(f"http://{PC_IP}:5000/steam", timeout=3)
        return "🎮 Launching Steam on PC..."
    except:
        return "❌ PC unreachable"

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

def launch_doom():
    requests.get(f"http://{PC_IP}:5000/doom", timeout=3)
    return "👹 Ripping and tearing: DOOM..."

def launch_drg():
    requests.get(f"http://{PC_IP}:5000/drg", timeout=3)
    return "⛏️ Rock and Stone! Deep Rock Galactic..."

def launch_apex():
    requests.get(f"http://{PC_IP}:5000/apex", timeout=3)
    return "🏃 Dropping in: Apex Legends..."

def launch_phasmo():
    requests.get(f"http://{PC_IP}:5000/phasmo", timeout=3)
    return "👻 Hunting ghosts: Phasmophobia..."

def launch_hitman():
    requests.get(f"http://{PC_IP}:5000/hitman", timeout=3)
    return "💼 Contract accepted: Hitman..."

# === MESSAGE HANDLER ===
@client.on(events.NewMessage(chats=GROUP_ID))
async def handler(event):
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
    elif msg == cmd.RUN_STEAM:
        reply = launch_steam()
    elif msg == cmd.RUN_ROBOQUEST:
        reply = launch_roboquest()
    elif msg == cmd.RUN_STRINOVA:
        reply = launch_strinova()
    elif msg == cmd.RUN_L4D2:
        reply = launch_l4d2()
    elif msg == cmd.RUN_L4D:
        reply = launch_l4d()
    elif msg == cmd.RUN_KOVAAKS:
        reply = launch_kovaaks()
    elif msg == cmd.RUN_DOOM:
        reply = launch_doom()
    elif msg == cmd.RUN_DRG:
        reply = launch_drg()
    elif msg == cmd.RUN_APEX:
        reply = launch_apex()
    elif msg == cmd.RUN_PHASMO:
        reply = launch_phasmo()
    elif msg == cmd.RUN_HITMAN:
        reply = launch_hitman()
    else:
        reply = f"❓ Unknown command: {msg}"

    if reply:
        await event.reply(reply)

# === START LISTENER ===
print(f"📡 Tablet listener active. Monitoring Group ID: {GROUP_ID}")
client.start()
client.run_until_disconnected()
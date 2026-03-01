import time
import requests
from bs4 import BeautifulSoup
from telegram import Bot

# ====== CONFIG ======
URL = "https://visacatcher.bot/appointments/abu-dhabi"
BOT_TOKEN = 7983497912:AAF8IJ55S77pnlfdNyx9e8QcDeX1LC4PzP8
CHAT_ID = 5062141854
CHECK_INTERVAL = 20   # seconds (free plan ke liye 20 safe hai)
# ====================

bot = Bot(token=BOT_TOKEN)

last_status = None
status_message_id = None


def check_slots():
    global last_status
    global status_message_id

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(URL, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    page_text = soup.get_text()

    if "No appointments available" in page_text:
        current_status = "❌ No Slots"
    else:
        current_status = "🚨 SLOT POSSIBLE"

    current_time = time.strftime("%H:%M:%S")

    message_text = (
        "Visa Monitor - Abu Dhabi\n\n"
        f"Status: {current_status}\n"
        f"Last Checked: {current_time}\n"
        f"Interval: {CHECK_INTERVAL} sec"
    )

    # First time send message
    if status_message_id is None:
        msg = bot.send_message(chat_id=CHAT_ID, text=message_text)
        status_message_id = msg.message_id
    else:
        bot.edit_message_text(
            chat_id=CHAT_ID,
            message_id=status_message_id,
            text=message_text
        )

    # Slot just opened alert
    if last_status == "❌ No Slots" and current_status == "🚨 SLOT POSSIBLE":
        bot.send_message(chat_id=CHAT_ID, text="🔥 SLOT JUST OPENED! BOOK FAST!")

    last_status = current_status


while True:
    try:
        check_slots()
        time.sleep(CHECK_INTERVAL)
    except Exception as e:
        print("Error:", e)
        time.sleep(60)

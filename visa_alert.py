import time
import requests
from bs4 import BeautifulSoup
from telegram import Bot

BOT_TOKEN = "7983497912:AAF8IJ55S77pnlfdNyx9e8QcDeX1LC4PzP8"
CHAT_ID = "5062141854"

URL = "https://visacatcher.bot/appointments/abu-dhabi"
CHECK_INTERVAL = 20

bot = Bot(token=BOT_TOKEN)

last_status = None
status_message_id = None

def check_slots():
    global last_status
    global status_message_id

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(URL, headers=headers, timeout=10)
        html = response.text

        if "No appointments available" in html:
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

        if status_message_id is None:
            msg = bot.send_message(chat_id=CHAT_ID, text=message_text)
            status_message_id = msg.message_id
        else:
            bot.edit_message_text(
                chat_id=CHAT_ID,
                message_id=status_message_id,
                text=message_text
            )

        if last_status == "❌ No Slots" and current_status == "🚨 SLOT POSSIBLE":
            bot.send_message(chat_id=CHAT_ID, text="🔥 SLOT JUST OPENED! BOOK FAST!")

        last_status = current_status

    except Exception as e:
        print("Error:", e)


while True:
    check_slots()
    time.sleep(CHECK_INTERVAL)

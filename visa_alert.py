from telegram import Bot

BOT_TOKEN = "7983497912:AAF8IJ55S77pnlfdNyx9e8QcDeX1LC4PzP8"
CHAT_ID = "5062141854"

bot = Bot(token=BOT_TOKEN)

bot.send_message(chat_id=CHAT_ID, text="Bot test successful ✅")

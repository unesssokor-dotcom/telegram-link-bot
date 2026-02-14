import telebot
import json
import os

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

DATA_FILE = "products.json"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Welcome ✅\nUse:\n/add name | link\n/get name")

@bot.message_handler(commands=['add'])
def add_product(message):
    try:
        text = message.text.replace("/add ", "")
        name, link = text.split("|")
        name = name.strip().lower()
        link = link.strip()

        data = load_data()
        data[name] = link
        save_data(data)

        bot.reply_to(message, f"✅ Saved: {name}")
    except:
        bot.reply_to(message, "❌ Format غلط\nاستعمل:\n/add product name | link")

@bot.message_handler(commands=['get'])
def get_product(message):
    name = message.text.replace("/get ", "").strip().lower()
    data = load_data()

    if name in data:
        bot.reply_to(message, data[name])
    else:
        bot.reply_to(message, "❌ Product ما لقيتش")

bot.infinity_polling()

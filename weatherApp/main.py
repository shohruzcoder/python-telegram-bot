from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, ConversationHandler, Filters, MessageHandler
from data import token, weather_api
import requests

toshkent, andijon, namangan, fargona, sirdaryo, samarqand, termiz, guliston, navoiy, buxoro, urganch, nukus = "Toshkent", "Andijon", "Namangan", "Farg'ona", "Sirdaryo", "Samarqand", "Termiz", "Guliston", "Navoiy", "Buxoro", "Urganch", "Nukus"

btns = ReplyKeyboardMarkup([["Shaharni o'zgartirish πΊπΏ"], ["Bot haqida β"]], resize_keyboard=True)

STATE_REGION = 1
STATE_BTN = 2


inline_buttons = [
    [
        InlineKeyboardButton(toshkent, callback_data="Toshkent"),
        InlineKeyboardButton(andijon, callback_data="Andijon")
    ],
    [
        InlineKeyboardButton(namangan, callback_data="Namangan"),
        InlineKeyboardButton(fargona, callback_data="Fargona")
    ],
    [
        InlineKeyboardButton(sirdaryo, callback_data="Sirdaryo"),
        InlineKeyboardButton(samarqand, callback_data="Samarqand")
    ],
    [
        InlineKeyboardButton(termiz, callback_data="Termiz"),
        InlineKeyboardButton(guliston, callback_data="Guliston")
    ],
    [
        InlineKeyboardButton(navoiy, callback_data="Navoiy"),
        InlineKeyboardButton(buxoro, callback_data="Buxoro")
    ],
    [
        InlineKeyboardButton(urganch, callback_data="Urganch"),
        InlineKeyboardButton(nukus, callback_data="Nukus")
    ]
]




def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_html(f"Assalomu aleykum <b>{update.effective_user.first_name}</b> \nSiz bu bot yordamida\nβοΈ Ob-Havodan xabaringiz bo'ladi.\n \nShu shaharlardan birini tanlang π", reply_markup=InlineKeyboardMarkup(inline_buttons))
    return STATE_REGION


def change_reg(update, context):
    update.message.reply_text("Sizga qaysi Shahar kerak β", reply_markup=InlineKeyboardMarkup(inline_buttons))
    return STATE_REGION

def info(update, context):
    update.message.reply_html(f"Bu Bot βοΈ Ob-havo haqida ma'lumot beradi.\n \nBu botni yozgan dasturchi: π§βπ» @shohruz_coder π§βπ»")

def f_help(update, context):
    update.message.reply_html(f"<b>{update.effective_user.first_name}</b> sizga qanday yordam kerakβ\nBotda bir kamchilik bo'lsa adminga murojaat qiling βοΈβοΈβοΈ\nAdmin: π§βπ» @shohruz_coder π§βπ» ")


def inline_btn(update, context):

    query = update.callback_query

    weather_all = "https://api.openweathermap.org/data/2.5/weather?q=" + query.data + "&appid=" + weather_api

    json_data = requests.get(weather_all).json()
    cound = json_data['weather'][0]["main"]
    temp = int(json_data["main"]["temp"] - 273.15)
    temp_max = int(json_data["main"]["temp_max"] - 273.15)
    temp_min = int(json_data["main"]["temp_min"] - 273.15)
    wind = json_data["wind"]["speed"]
    country = json_data["sys"]["country"]

    if query.data == "Toshkent" or query.data == "Urganch" or query.data == "Nukus":
        query.message.delete()
        query.message.reply_html(f"<b>πΊπΏ {country} {query.data}</b> shahari bugungi βοΈ Ob-havo \n \nπ‘ Temp: <b>{temp}</b>Β°C\nπ‘ Temp-max: <b>{temp_max}</b>Β°C\nπ‘ Temp-min: <b>{temp_min}</b>Β°C\nπ¬  Shamol tezligi: <b>{wind}</b> m/s", reply_markup=btns)
    else:
        query.message.delete()
        query.message.reply_html(f"<b>πΊπΏ {country} {query.data}</b> shahari bugungi βοΈ Ob-havo \n \nπ‘ Temp: <b>{temp}</b>Β°C\nπ‘ Temp-max: <b>{temp_max}</b>Β°C\nπ‘ Temp-min: <b>{temp_min}</b>Β°C\nπ¬  Shamol tezligi: <b>{wind}</b> m/s", reply_markup=btns)

    return STATE_BTN



conv_handler = ConversationHandler(
        entry_points = [CommandHandler('start', start)],
        states={
            STATE_REGION:[CallbackQueryHandler(inline_btn)],
            STATE_BTN:[
                MessageHandler(Filters.regex("^(Shaharni o'zgartirish πΊπΏ)$"), change_reg),
                MessageHandler(Filters.regex("^(Bot haqida β)$"), info)
            ]
        },
        fallbacks=[CommandHandler('start', start)]
    )


updater = Updater(token)

updater.dispatcher.add_handler(conv_handler)

# updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', f_help))
# updater.dispatcher.add_handler(CallbackQueryHandler(inline_btn))

updater.start_polling()
updater.idle()

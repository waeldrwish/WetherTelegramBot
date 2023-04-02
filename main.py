import telebot
from decouple import config
from telebot import types
import requests
import pycountry

BOT_TOKEN = config('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# تحديد الأوامر المتاحة
commands = ['/start', '/help', '/weather']

@bot.message_handler(commands=["start","help"])
def welcome(message):
    # إنشاء InlineKeyboardMarkup
    markup = types.InlineKeyboardMarkup(row_width=1)
    # إضافة الأزرار إلى القائمة
    for cmd in commands:
        markup.add(types.InlineKeyboardButton(cmd, callback_data=cmd))
    bot.send_message(message.chat.id, "مرحبًا بك في بوت تجريبي! الأوامر المتاحة هي:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == '/start':
        bot.send_message(call.message.chat.id, "أهلاً بك في البوت")
    elif call.data == '/help':
        bot.send_message(call.message.chat.id, "هذا البوت يوفر خدمة الطقس للمدن العالمية.")
    elif call.data == '/weather':
        bot.send_message(call.message.chat.id, "أدخل اسم المدينة للحصول على تقرير الطقس.")

@bot.message_handler(func=lambda message: True)
def isMsg(message):
    try:
        country_code = pycountry.countries.search_fuzzy(message.text)[0].alpha_2
        if country_code.lower() != 'aq':  # exclude Antarctica
            url = f"https://wttr.in/{message.text.lower()}?format=%C\n%t\n%H\n%w"
            response = requests.get(url)
            if response.status_code == 200:
                bot.reply_to(message,"******************\n"+response.text.strip()+"\n******************\n\n شكرا لاستعمالكم خدمتنا")
            else:
                bot.reply_to(message, "حدث خطأ أثناء جلب تقرير الطقس")
    except:
        bot.reply_to(message, "يرجى إدخال اسم مدينة صحيح")

bot.polling()

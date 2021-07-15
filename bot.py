import pyowm
import telebot
from telebot import types
from tokens import *  # my owm tokens in another file
from IndividualID import *


owm = pyowm.OWM(owm_token)
bot = telebot.TeleBot(bot_token)  # @appvenderbot


@bot.message_handler(commands=['settings'])
def settings(message):
    print("Id: " + str(message.from_user.id) + "\nFirst Name: " +
          str(message.from_user.first_name) + "\nText: " + str(message.text) + "\n")
    #lang = translator.detect(message.text)
    # res = translator.translate("Меня может редактировать только мой создатель!!", dest = lang.lang)   res.text
    bot.send_message(
        message.chat.id, "Меня может редактировать только мой создатель!!")


@bot.message_handler(commands=['commands'])
def commands(message):
    print("Id: " + str(message.from_user.id) + "\nFirst Name: " +
          str(message.from_user.first_name) + "\nText: " + str(message.text) + "\n")
    #lang = translator.detect(message.text)
    #res = translator.translate("У меня присутствуют такие команды как:", dest = lang.lang)
    bot.send_message(
        message.chat.id, "У меня присутствуют такие команды как:\n1)/start(/go)\n2)/settings\n3)/help\n4)/weather\n5)/language")


@bot.message_handler(commands=['language'])
def commands(message):
    print("Id: " + str(message.chat.id) + "\nFirst Name: " +
          str(message.from_user.first_name) + "\nText: " + str(message.text) + "\n")

    markuplang = types.InlineKeyboardMarkup(row_width=2)
    EN = types.InlineKeyboardButton("Английский", callback_data='EN')
    RU = types.InlineKeyboardButton("Русский", callback_data='RU')

    markuplang.add(EN, RU)

    bot.send_message(
        message.chat.id, "На каком языке вам удобнее общатся?", reply_markup=markuplang)


@bot.message_handler(commands=['start', 'go'])
def start(message):
    print("Id: " + str(message.from_user.id) + "\nFirst Name: " +
          str(message.from_user.first_name) + "\nText: " + str(message.text) + "\n")
    bot.send_message(message.chat.id, "Привет {0.first_name}!".format(
        message.from_user), parse_mode='HTML')
    bot.send_message(
        message.chat.id, "Я <b>Пинки</b>, приятно познакомится)", parse_mode='HTML')


@bot.message_handler(commands=['help'])
def help(message):
    print("Id: " + str(message.from_user.id) + "\nFirst Name: " +
          str(message.from_user.first_name) + "\nText: " + str(message.text) + "\n")
    bot.send_message(
        message.chat.id, "Я <b>Пинки</b>, бот созданный одним человеком)\nСписок команд: /commands", parse_mode='HTML')


@bot.message_handler(commands=['weather'])
def weather(message):
    print("Id: " + str(message.from_user.id) + "\nFirst Name: " +
          str(message.from_user.first_name) + "\nText: " + str(message.text) + "\n")
    msg = "Введи название своего города пожалуйста."

    bot.register_next_step_handler(
        bot.send_message(message.chat.id, msg), prognoz)


@bot.message_handler(content_types=['text'])
def talk(message):
    #lang = translator.detect(message.text)
    print("Id: " + str(message.from_user.id) + "\nFirst Name: " +
          str(message.from_user.first_name) + "\nText: " + str(message.text) + "\n")

    if message.from_user.id == GayId:
        if "ы" in (str.lower(message.text)) or "s" in (str.lower(message.text)) or "і" in (str.lower(message.text)):
            bot.send_message(message.chat.id, "Соси яйца")

    if "привет" in (str.lower(message.text)) or "ку" in (str.lower(message.text)) or "куку" in (str.lower(message.text)) or "hello" in (str.lower(message.text)):
        bot.send_message(
            message.chat.id, "Привет {0.first_name}!".format(message.from_user))

    elif "я" in (str.lower(message.text)) and "твой" in (str.lower(message.text)) and "создатель" in (str.lower(message.text)):
        if message.from_user.id == CreatorId:
            bot.send_message(
                message.chat.id, "Я рада видеть своего создателя))")
        else:
            bot.send_message(message.chat.id, "Не ври мне!!!")

    elif "пока" in (str.lower(message.text)):
        bot.send_message(message.chat.id, "Удачи тебе!")

    elif "как дела" in (str.lower(message.text)) or "как ты" in (str.lower(message.text)):

        markup = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
        item2 = types.InlineKeyboardButton("Не очень", callback_data='bad')

        markup.add(item1, item2)

        bot.send_message(
            message.chat.id, "У меня всё отлично)\nА ты как?", reply_markup=markup)

    elif "ты работаешь" in (str.lower(message.text)):
        bot.send_message(
            message.chat.id, "Я рада что могу функционировать правильно))")

    elif "ты бот" in (str.lower(message.text)):
        bot.send_message(message.chat.id, "Я и обидется могу!")

    elif "ты не бот" in (str.lower(message.text)):
        bot.send_message(message.chat.id, "Я рада что меня считают человеком)")

    elif "кто ты" in (str.lower(message.text)) or "ты кто" in (str.lower(message.text)):
        bot.send_message(message.chat.id, "Я <b>Пинки</b>))",
                         parse_mode='HTML')

    elif "ля ты крыса" in (str.lower(message.text)):
        bot.send_message(message.chat.id, "А может ты крыса?")

    else:
        bot.send_message(message.chat.id, "Я не знаю что ответить...")


@bot.message_handler(content_types=['text'])
def prognoz(message):
    print("Id: " + str(message.from_user.id) + "\nFirst Name: " +
          str(message.from_user.first_name) + "\nText: " + str(message.text) + "\n")
    try:
        observation = owm.weather_at_place(message.text)
        w = observation.get_weather()
        temp = w.get_temperature('celsius')["temp"]

        answer = "В городе " + message.text + " сейчас " + w.get_detailed_status() + \
            "\n"
        answer += "Температура в районе " + str(temp) + " C°" + "\n\n"

        if temp < 10:
            answer += "Сейчас ппц как холодно, одевайся как танк!"
        elif temp < 20:
            answer += "Сейчас прохладно, одень куртку."
        else:
            answer += "Температура норм, одевай что хочешь."

        bot.send_message(message.chat.id, answer)
    except:
        bot.send_message(
            message.chat.id, "Такого города не существуе, или я его ещё не знаю)\nПожалуйста введите другой город.")


@bot.callback_query_handler(func=lambda call: call.data == 'EN' or call.data == 'RU')
def calback_inline(call):
    try:
        if call.message:
            if call.data == 'RU':
                bot.send_message(call.message.chat.id,
                                 "Хорошо, теперь буду общатся с вами на русском")

            elif call.data == 'EN':
                bot.send_message(
                    call.message.chat.id, "Ok, now I will communicate with you in English")

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="На каком языке вам удобнее общатся?", reply_markup=None)
            bot.answer_callback_query(
                callback_query_id=call.id, show_alert=False, text="Данная функция не работает!")

    except Exception as e:
        print(repr(e))


@bot.callback_query_handler(func=lambda call: call.data == 'good' or call.data == 'bad')
def calback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, "Вот и хорошо)")

            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, "Бывает и хуже)")

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="У меня всё отлично)\nА ты как?", reply_markup=None)

    except Exception as e:
        print(repr(e))


bot.polling(none_stop=True)

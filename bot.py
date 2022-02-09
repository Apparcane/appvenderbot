import pyowm
import telebot
from time import sleep
from telebot import types
from tokens import *  # my owm tokens in another file
from IndividualID import *
from ongoing import *
import json

owm = pyowm.OWM(owm_token)
bot = telebot.TeleBot(bot_token)  # @appvenderbot

@bot.message_handler(commands=['start', 'go'])
def start(message):

    with open('./json/data.json', 'r+', encoding = 'utf-8') as data_file:   
        users = json.load(data_file)
        for p in users['user']:
            i = p['nums'] + 1

    for p in users['user']:
        if message.from_user.username != p['username'] or message.chat.id != p['chat_id']:

            with open('./json/data.json', 'w+', encoding = 'utf-8') as data_file:
                users['user'].append({
                    'nums' : i,
                    'username' : message.from_user.username,
                    'chat_id' : message.chat.id,
                    'first_name' : message.from_user.first_name,
                    'last_name' : message.from_user.last_name
                })

                json.dump(users, data_file, indent = 4)


    # print(message)
    print("Id: " + str(message.from_user.id) + "\nFirst Name: " +
          str(message.from_user.first_name) + "\nText: " + str(message.text) + "\n")
    bot.send_message(message.chat.id, "Привет {0.first_name}!".format(
        message.from_user), parse_mode='HTML')
    bot.send_message(
        message.chat.id, "Я <b>Пинки</b>, приятно познакомится)", parse_mode='HTML')

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
        message.chat.id, "У меня присутствуют такие команды как:\n1)/start(/go)\n2)/settings\n3)/help\n4)/weather\n5)/language\n6)/ongoing")


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

@bot.message_handler(commands=['ongoing'])
def ongoing_commands(message):
    print("Id: " + str(message.from_user.id) + "\nFirst Name: " +
          str(message.from_user.first_name) + "\nText: " + str(message.text) + "\n")
    bot.register_next_step_handler(
                    bot.send_message(message.chat.id, 'Введине номер страницы 1-8:'), choose_page)

@bot.message_handler(content_types=['text'])
def talk(message):
    #lang = translator.detect(message.text)
    print("Id: " + str(message.from_user.id) + "\nFirst Name: " +
          str(message.from_user.first_name) + "\nText: " + str(message.text) + "\n")

    if "привет" in (str.lower(message.text)) or "ку" in (str.lower(message.text)) or "куку" in (str.lower(message.text)) or "hello" in (str.lower(message.text)):
        if message.from_user.id == CreatorId:
            bot.send_message(
                message.chat.id, "Я рада видеть вас создатель))")
        else:
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

    elif "онгоинг" in (str.lower(message.text)):
        anime = types.InlineKeyboardMarkup(row_width=2)
        item1 = types.InlineKeyboardButton("Все", callback_data='all')
        item2 = types.InlineKeyboardButton(
            "Ввести значение", callback_data='choose')

        anime.add(item1, item2)

        bot.send_message(
            message.chat.id, "Показать список аниме онгоингов?", reply_markup=anime)

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


@bot.message_handler(content_types=['text'])
def choose_page(message):
    print("Id: " + str(message.from_user.id) + "\nFirst Name: " +
          str(message.from_user.first_name) + "\nText: " + str(message.text) + "\n")
    try:
        answer = ''
        for i in ongoing(int(message.text)):
            answer = str(answer) + str(i) + str('\n')

        bot.send_message(message.chat.id, answer)
    except:
        bot.send_message(
            message.chat.id, "К сожалению нет страницы с таким номером.")


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


@bot.callback_query_handler(func=lambda call: call.data == 'all' or call.data == 'choose')
def calback_inline(call):
    try:
        if call.message:
            if call.data == 'all':
                bot.send_message(call.message.chat.id, "Одну секунду ...")

                answer = ''
                clock = 0

                for i in ongoing_all(1):
                    answer = str(answer) + str(i) + str('\n')
                    clock = clock + 1
                    if clock % 11 == 0:
                        bot.send_message(call.message.chat.id, answer)
                        clock = 1
                        answer = ''
                        sleep(2)

                bot.send_message(call.message.chat.id, answer)

            elif call.data == 'choose':
                bot.register_next_step_handler(
                    bot.send_message(call.message.chat.id, 'Введине номер страницы 1-8:'), choose_page)

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Показать список аниме онгоингов?", reply_markup=None)

    except Exception as e:
        print(repr(e))


bot.polling(none_stop=True)

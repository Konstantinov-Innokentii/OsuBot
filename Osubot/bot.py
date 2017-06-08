# -*- coding: utf-8 -*-

from Osubot.config import token
import telebot
import json
from Osubot.alchemy import *
from telebot import types
from Osubot.consts import *


bot = telebot.TeleBot(token)

#Creating custom keyboards
#TODO: refactor the keyboard for different user_cases

keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
button_schedule = types.KeyboardButton(text='/schedule')
button_help = types.KeyboardButton(text='/help')
button_registration = types.KeyboardButton(text='/registration')
keyboard.add(button_schedule, button_help, button_registration)

"""
Dictionary for user_status in registration
"""
user_status = {}


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, start_mess, reply_markup=keyboard)


@bot.message_handler(commands=['registration'])
def registration(message):
    bot.send_message(message.chat.id, reg_mess)
    user_status[message.chat.id] = "USER_REGISTRATING"


@bot.message_handler(func=lambda message: user_status.get(message.chat.id) == "USER_REGISTRATING")
def user_registration(message):
    if User.get_user_by_id(message.chat.id) is None:
        s.add(User(message.text, message.chat.id))
        s.commit()
        user_status[message.chat.id] = "USER_REGISTRATED"
        bot.send_message(message.chat.id, "Вы зарегистрированы, ваша группа {}.".format(
            User.get_group(message.chat.id)))
    else:
        User.get_user_by_id(message.chat.id).group_id = message.text
        bot.send_message(message.chat.id, "Вы зарегистрированы, ваша группа {}.".format(
            User.get_group(message.chat.id)))
        s.commit()
        user_status[message.chat.id] = "USER_REGISTRATED"


@bot.message_handler(commands=["schedule"])
def send_schedule(message):

    try:
        path = '/home/flamingshalom/PycharmProjects/OSUschedulebot/schedule/{}.json'.format(
            User.get_group(message.chat.id)).replace(" ", "")
    except AttributeError:
        bot.send_message(message.chat.id, "Вы не зарегестрированы")
        return
    try:
        data = open(path, 'r')
    except FileNotFoundError:
        bot.send_message(message.chat.id, "Неверно указана группа.")
        return
    data_json = data.readlines()
    try:
        parsed_data = json.loads((data_json[1]))
    except IndexError:
        bot.send_message(message.chat.id, "Нет расписания на сегодняшний день")
        return
    if range(len(parsed_data["Пара"]) != 0):
        for i in range(len(parsed_data["Пара"])):
            bot.send_message(message.chat.id,"Пара: {}.Дисциплина: {}.Аудитория: {}.Тип: {} Групповые занятияв:{}".format(parsed_data["Пара"][i],
                             parsed_data["Дисциплина"][i], parsed_data["Аудитория"][i], parsed_data["Тип"][i],""), reply_markup=keyboard)
    else:
            bot.send_message(message.chat.id, "Групповые занятия:{} ".format(parsed_data["Групповые занятия"][0]+parsed_data["Групповые занятия"][1]+parsed_data["Групповые занятия"][2]+parsed_data["Групповые занятия"][3]),
                             reply_markup=keyboard)
            bot.send_message(message.chat.id, "Групповые занятия:{} ".format(
                     parsed_data["Групповые занятия"][4] + parsed_data["Групповые занятия"][5] + parsed_data["Групповые занятия"][6] + parsed_data["Групповые занятия"][7]),
                     reply_markup=keyboard)


@bot.message_handler(commands=["help"])
def send_info(message):
    bot.send_message(message.chat.id, help_mess, reply_markup=keyboard)


@bot.message_handler(commands=["test"])
def get_id(message):
    bot.send_message(message.chat.id, User.get_group(message.chat.id))


if __name__ == '__main__':
    bot.polling(none_stop=True)

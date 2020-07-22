#!/usr/bin/python3
import requests as req
import time, sys, os, json
import datetime as dt
import threading as TH
import telebot
from myaudio import voice_send
from myphoto import photo_send


'''
bot_name: "DSPLabs_HH_by_Spiritgyx",
bot_username: "DSPLabs_HH_bot",
token: "1264077369:AAG3rgZ-HknD4mme-u2P1AKr0hC9RTi0E5Y"
'''

TOKEN = '1264077369:AAG3rgZ-HknD4mme-u2P1AKr0hC9RTi0E5Y'
GET_URL = 'https://api.telegram.org/file/bot%s/%s'  # %(TOKEN, file_path)
DIRS = ['photos', 'voice']

for d in DIRS:
    if not os.path.exists(d) and not os.path.isdir(d):
        os.mkdir(d)

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    print(str(message))
    bot.send_message(message.chat.id, "Этот бот сделан для выполнения заданий от DSP Labs\nАвтор: Марданов Ринат")

@bot.message_handler(content_types=['voice'])
def voice_message(message):
    f = bot.get_file(message.voice.file_id)
    file = req.get(GET_URL % (TOKEN, f.file_path))
    print(f.file_path)
    jj = file.content
    with open(f.file_path, mode='wb') as ff:
        ff.write(jj)
    voice_send(message.from_user.id, f.file_path, bot.send_message, message,
               'mimetype: %s\nfile_id: %s\nfile_size: %s\n' % \
               (message.voice.mime_type, message.voice.file_id, message.voice.file_size)
               )

@bot.message_handler(content_types=['photo'])
def photo_message(message):
    p = message.photo
    p.sort(key=lambda x: x.file_size)
    f = bot.get_file(p[0].file_id)
    file = req.get(GET_URL % (TOKEN, f.file_path))
    jj = file.content
    with open(f.file_path, mode='wb') as ff:
        ff.write(jj)
    photo_send(message.from_user.id, f.file_path, bot.send_message, message,
               'file_id: %s\nfile_size: %d\nwidth: %d\nheight: %d\n'%
               (p[0].file_id, p[0].file_size, p[0].width, p[0].height)
               )


print('Bot started!')
bot.polling()

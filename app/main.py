import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import sys
import json

from commads_bot.botMessage import *

def mainFunction():
    if len(sys.argv) < 1:
        print("no have token")
        exit()
    TOKEN = sys.argv[1]

    bot = telebot.TeleBot(token=TOKEN)

    

    # выгрузка json-файла

    def loadjsonPa(file):
        with open(file,'r', encoding='utf-8') as Jfile:
            return json.load(Jfile)



    def getTeamInlineKeyBoard():
        statTeamKeyBoard = InlineKeyboardMarkup()
        statTeamKeyBoard.row_width = 1
        with open('player.json','r', encoding='utf-8') as file:
            data = [item["name"] for item in json.load(file)]
        for i in range(len(data)):
            statTeamKeyBoard.add(InlineKeyboardButton(data[i],callback_data=f"statTeam_{i}"))
        
        return statTeamKeyBoard


    def getTeamMatchesnlineKeyBoard():

        statTeamKeyBoard = InlineKeyboardMarkup()
        statTeamKeyBoard.row_width = 1
        with open('matches.json','r', encoding='utf-8') as file:
            data = [item["date"] for item in json.load(file)]
        for i in range(len(data)):
            statTeamKeyBoard.add(InlineKeyboardButton(data[i],callback_data=f"matchTeam_{i}"))
        
        return statTeamKeyBoard


    @bot.callback_query_handler(func=lambda call: call.data.startswith("matchTeam_"))
    def callback_query(call):
        numMatch = call.data.split("_",1)[1]
        
        try:
            data = loadjsonPa('matches.json')[int(numMatch)]
            bot.send_message(call.message.chat.id,teamMatchstr(data))

        except Exception as e:
            bot.send_message(call.message.chat.id,f"подождите немного.... {e}")
            

    @bot.callback_query_handler(func=lambda call: call.data.startswith("statTeam_"))
    def callback_query(call):

        num = call.data.split("_",1)[1]

        try:

            data = loadjsonPa('player.json')[int(num)]
            
            bot.send_photo(call.message.chat.id,data["image"],caption=statTeamstr(data=data),reply_markup=None)
        except Exception as e:
              bot.send_message(call.message.chat.id,"подождите немного....")

 
    #работа бота

    @bot.callback_query_handler(func=lambda call: call.data.startswith("statGame_"))
    def callback_query(call):
        key = call.data.split("_",1)[1]

        data = loadjsonPa('players.json')
        try:
            bot.send_photo(call.message.chat.id,"https://bigfoto.name/photo/uploads/posts/2023-02/1676631269_bigfoto-name-p-futbolnaya-ploshchadka-na-dache-83.jpg",
                           
                           caption=statGamestr(data=data,key=key),reply_markup=None
                           )
            
            
        except Exception as e:
            bot.send_message(call.message.chat.id,f" ОШИБКА{e}")


  
    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_message(message.chat.id,startMessage(),reply_markup=None)

    #статистика команды
    @bot.message_handler(commands=["statTeam"])
    def statTeam(message):
        keyboardInline = getTeamInlineKeyBoard()

        
        bot.send_message(message.chat.id,"это статистика команды",reply_markup=keyboardInline)

    #статистика игр, проведенных командой
    @bot.message_handler(commands=["statGame"])
    def statGame(message):
        data = loadjsonPa('players.json')

        try:
            bot.send_message(message.chat.id,statGamestr(data=data),reply_markup=None)
            
        except Exception as e:
            bot.send_message(message.chat.id,f" ОШИБКА{e}")
        bot.send_message(message.chat.id,"это статистика игр")


    @bot.message_handler(commands=["matchs"])
    def matchGame(message):
        matchKeyboard = getTeamMatchesnlineKeyBoard()
        
        bot.send_message(message.chat.id,"n",reply_markup=matchKeyboard)

    bot.polling(none_stop=True)




if __name__ == '__main__':

    mainFunction()


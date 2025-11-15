import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import sys
import json
from datetime import datetime, timedelta
import os
from logicBot.loadParse import FootballParserManager
from commads_bot.botMessage import *

JSON_FILE_MATCH = 'matches.json' 
JSON_FILE_PLAYERS = 'players.json'
JSON_FILE_STATIC_GAMES = 'staticGame.json'


dataMatch = None
dataPlayers = None
dataStaticGame   = None
dataUser = None
INTERVAL = timedelta(hours=24)


def adutoUpdateData():
    global dataStaticGame
    global dataMatch
    global dataPlayers
    if dataStaticGame is None or datetime.now() - dataStaticGame["time_key"] > INTERVAL :
        if not os.path.exists(JSON_FILE_STATIC_GAMES) or not os.path.exists(JSON_FILE_PLAYERS) or not os.path.exists(JSON_FILE_MATCH) or datetime.now() - datetime.fromtimestamp(os.path.getmtime(JSON_FILE_STATIC_GAMES))> INTERVAL :

            print("Обновляем JSON через парсер")
            FootballParserManager().edit_json()
                
            
        

            

        with open(JSON_FILE_STATIC_GAMES, 'r', encoding='utf-8') as f:
            
            dataStaticGame = json.load(f)
        with open(JSON_FILE_PLAYERS, 'r', encoding='utf-8') as f:
                dataPlayers = json.load(f)
        with open(JSON_FILE_MATCH, 'r', encoding='utf-8') as f:
                dataMatch = json.load(f)
def mainFunction():
    global dataStaticGame
    global dataMatch
    global dataPlayers
    if len(sys.argv) < 1:
        print("no have token")
        exit()
    TOKEN = sys.argv[1]

    bot = telebot.TeleBot(token=TOKEN)


    # выгрузка json-файла





    def loadjsonPa(file):
        
        if os.path.exists(file):
            
            last_modified = datetime.fromtimestamp(os.path.getmtime(file))
            now = datetime.now()
            update_interval = timedelta(hours=24)
            if now - last_modified < update_interval:
                with open(file,'r', encoding='utf-8') as Jfile:
                    data = json.load(Jfile)
                    if isinstance(data,list):
                        data.append(datetime.now())
                        return data
                    data["time_key"] = datetime.now()
                    return data
            try:    
                FootballParserManager().starts()
            except Exception as e:
                print (f"ne poluchilos {e} ")



    def getTeamInlineKeyBoard():
        statTeamKeyBoard = InlineKeyboardMarkup()
        statTeamKeyBoard.row_width = 1
        with open(JSON_FILE_PLAYERS,'r', encoding='utf-8') as file:
            data = [item["name"] for item in json.load(file)]
        for i in range(len(data)):
            statTeamKeyBoard.add(InlineKeyboardButton(data[i],callback_data=f"statTeam_{i}"))
        
        return statTeamKeyBoard


    def getTeamMatchesnlineKeyBoard():

        statTeamKeyBoard = InlineKeyboardMarkup()
        statTeamKeyBoard.row_width = 1
        with open(JSON_FILE_MATCH,'r', encoding='utf-8') as file:
            data = [item["date"] for item in json.load(file)]
        for i in range(len(data)):
            statTeamKeyBoard.add(InlineKeyboardButton(data[i],callback_data=f"matchTeam_{i}"))
        
        return statTeamKeyBoard

    #работа бота
    @bot.callback_query_handler(func=lambda call: call.data.startswith("matchTeam_"))
    def callback_query(call):
        global dataMatch
        numMatch = call.data.split("_",1)[1]
        try:
            print(dataMatch[1] )
        except :
            print ("tre")
        
            
        if dataMatch is None:
            dataMatch = loadjsonPa('matches.json')[int(numMatch)]
        bot.send_message(call.message.chat.id,teamMatchstr(dataMatch[int(numMatch)]))

        
            

    @bot.callback_query_handler(func=lambda call: call.data.startswith("statTeam_"))
    def callback_query(call):
        global dataPlayers
        num = call.data.split("_",1)[1]

        try:
            if dataPlayers is None :
                dataPlayers = loadjsonPa(JSON_FILE_PLAYERS)
            
            bot.send_photo(call.message.chat.id,dataPlayers[int(num)]["image"],caption=statTeamstr(data=dataPlayers[int(num)]),reply_markup=None)
        except Exception as e:
              bot.send_message(call.message.chat.id,f"подождите немного.... {e}")

 
    

    @bot.callback_query_handler(func=lambda call: call.data.startswith("statGame_"))
    def callback_query(call):
        key = call.data.split("_",1)[1]
        if dataStaticGame is None or dataStaticGame["time_key"] > datetime.now():

            dataStaticGame = loadjsonPa(JSON_FILE_STATIC_GAMES)
        try:
            bot.send_photo(call.message.chat.id,"https://bigfoto.name/photo/uploads/posts/2023-02/1676631269_bigfoto-name-p-futbolnaya-ploshchadka-na-dache-83.jpg",
                           
                           caption=statGamestr(data=dataStaticGame,key=key),reply_markup=None
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
        global dataStaticGame
        if dataStaticGame is None :
            dataStaticGame = loadjsonPa(JSON_FILE_STATIC_GAMES)
        
        try:
            bot.send_message(message.chat.id,statGamestr(data=dataStaticGame),reply_markup=None)
            
        except Exception as e:
            bot.send_message(message.chat.id,f" ОШИБКА{e}")
        bot.send_message(message.chat.id,"это статистика игр")


    @bot.message_handler(commands=["matchs"])
    def matchGame(message):
        matchKeyboard = getTeamMatchesnlineKeyBoard()
        
        bot.send_message(message.chat.id,"n",reply_markup=matchKeyboard)
    


    bot.polling(none_stop=True)




if __name__ == '__main__':
    adutoUpdateData()
    print(dataStaticGame)
    #print(h)
    mainFunction()


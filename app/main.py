import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton,InputMediaPhoto
import sys
import json
import threading
import time
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
INTERVAL = timedelta(seconds=15)


def adutoUpdateData():
    global dataStaticGame
    global dataMatch
    global dataPlayers
    while True:
        
        print("Работа\n\n\n")
        if dataStaticGame is None or datetime.now() - dataStaticGame["time_key"] > INTERVAL :
            if not os.path.exists(JSON_FILE_STATIC_GAMES) or not os.path.exists(JSON_FILE_PLAYERS) or not os.path.exists(JSON_FILE_MATCH) or datetime.now() - datetime.fromtimestamp(os.path.getmtime(JSON_FILE_STATIC_GAMES))> INTERVAL :
                print("Работа2\n\n\n")
                print("Обновляем JSON через парсер")
                FootballParserManager().starts()

                    
                
            

                
            # if not os.path.exists(JSON_FILE_STATIC_GAMES):
            #     return
            with open(JSON_FILE_STATIC_GAMES, 'r', encoding='utf-8') as f:
                print("Работа3\n\n\n")
                dataStaticGame = json.load(f)
                dataStaticGame["time_key"] = datetime.now()
            with open(JSON_FILE_PLAYERS, 'r', encoding='utf-8') as f:
                    print("Работа4\n\n\n")
                    dataPlayers = json.load(f)
            with open(JSON_FILE_MATCH, 'r', encoding='utf-8') as f:
                    print("Работа5\n\n\n")
                    dataMatch = json.load(f)
        time.sleep(60*60*24)

def start_automatic_task():
    thread = threading.Thread(target=adutoUpdateData)
    thread.daemon = True  # Позволяет прервать поток при завершении основного процесса
    thread.start()


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

    def getSwitchPlayers(num):
        global dataPlayers
        prevNextPlayer = InlineKeyboardMarkup(row_width=3)
        prevPlayer = InlineKeyboardButton(text=f"   <------\n \n{dataPlayers[num-1]["name"]} ",callback_data=f"statTeame_{num-1}") if num-1 >=0 else None
        nextPlayer = InlineKeyboardButton(text=f"   \n \n{dataPlayers[num+1]["name"]}------>    ",callback_data=f"statTeame_{num+1}") if num+1 < len(dataPlayers) else None

        prevNextPlayer.row(prevPlayer,nextPlayer) if prevPlayer is not None and nextPlayer  is not None else " "
        prevNextPlayer.add(nextPlayer) if nextPlayer  is not None and prevPlayer is None else " "
        prevNextPlayer.add(prevPlayer) if prevPlayer  is not None and nextPlayer is None else " "

        return prevNextPlayer

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
            dataMatch = loadjsonPa('matches.json')

        bot.send_message(call.message.chat.id,teamMatchstr(dataMatch[int(numMatch)]))

        
    @bot.callback_query_handler(func=lambda call: call.data.startswith("statTeame_"))       
    def callback_query_handler(call):
        global dataPlayers
        num = int(call.data.split("_", 1)[1])
        keyboard = getSwitchPlayers(num)
        
        try:
            med = InputMediaPhoto(dataPlayers[num]["image"], caption=statTeamstr(data=dataPlayers[num]))
            bot.edit_message_media(media=med, chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception as e:
            bot.send_message(call.message.chat.id,statTeamstr(data=dataPlayers[num]),reply_markup=keyboard)

        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboard)
        

    @bot.callback_query_handler(func=lambda call: call.data.startswith("statTeam_"))
    def callback_query(call):
        global dataPlayers
        num = int(call.data.split("_",1)[1])
        
        try:
            if dataPlayers is None :
                dataPlayers = loadjsonPa(JSON_FILE_PLAYERS)

            prevNextPlayer = getSwitchPlayers(num)
            
            
            bot.send_photo(call.message.chat.id,dataPlayers[num]["image"],caption=statTeamstr(data=dataPlayers[num]),reply_markup=prevNextPlayer)
            
            
        except Exception as e:
              bot.send_message(call.message.chat.id,statTeamstr(data=dataPlayers[num]),reply_markup=prevNextPlayer)
              print(e)

 
    

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

    @bot.message_handler(commands=["fan_club"])
    def fanClubMessage():
        pass

    @bot.message_handler(commands=["matchs"])
    def matchGame(message):
        matchKeyboard = getTeamMatchesnlineKeyBoard()
        
        bot.send_message(message.chat.id,"n",reply_markup=matchKeyboard)
    


    bot.polling(none_stop=True)




if __name__ == '__main__':
    start_automatic_task()
    mainFunction()


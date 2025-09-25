import telebot
from telebot.types import InlineKeyboardMarkup ,InlineKeyboardButton

class MainMenu:
    def __init__(self,bot:telebot.TeleBot):
        self.bot = bot
    

    def start(self,message):
        fan_club = ["garage","split","glass"]
        keyboard = InlineKeyboardMarkup(row_width=2)
        for butt in fan_club:
            button = InlineKeyboardButton(text=butt)
            
        self.bot.send_message(message.chat.id,"""привет, куда хочешь вступить.\n 
                              это футбольный клуб,где собираются разные дяденьки\n
                              чтобы поболеть за свою команду, а также быть в курсе
                               всех событий своей любимой команды """)
    
        
        pass
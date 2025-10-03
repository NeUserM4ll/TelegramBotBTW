import telebot
from telebot.types import InlineKeyboardMarkup ,InlineKeyboardButton

class MainMenu:
    def __init__(self,bot:telebot.TeleBot):
        self.bot = bot
    

    def start(self):
       return '''
        Привет это telegram-бот, где Вы можете получать актуальную статистику футбольного клуба "ПАРИ НН"
        тут реализованы сдедующие команды :\n\n
        /statTeam - информация про команду (статистику)
        /statGame - Статистика по играм (поражения, победы, ничьи)
        /matchs - последние матчи команды \n\n\n
        /fanClub - тг группы для фанатов данного клуба
        В общем все, что нужно бот найдет!!

'''
    def statTeam(self):
        pass

    
        

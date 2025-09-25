import telebot
import sys

def mainFunction():
    if len(sys.argv) < 1:
        print("no have token")
        exit()
    TOKEN = sys.argv[1]

    bot = telebot.TeleBot(token=TOKEN)

    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_message(message.chat.id,"привет")

    bot.polling(none_stop=True)

if __name__ == '__main__':
    mainFunction()


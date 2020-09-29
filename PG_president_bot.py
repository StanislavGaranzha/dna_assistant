'''
Бот, который уведомляет о новых документах президента на pravo.gov.ru.
'''
import telebot

import config
import dna_parser

bot = telebot.TeleBot(config.TOKEN_PRESIDENT)

@bot.message_handler(commands=['start_president'])
def start_gov_command(message):
    bot.send_message(message.chat.id, 'бот президента запущен')
    parser = dna_parser.PravoGovParser('president')
    parser.pravo_gov_parse(bot, message)

if __name__ == "__main__":
    bot.infinity_polling()

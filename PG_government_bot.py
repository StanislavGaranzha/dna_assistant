'''
Бот, который уведомляет о новых документах правительства на pravo.gov.ru.
'''
import telebot

import config
import dna_parser

bot = telebot.TeleBot(config.TOKEN_GOVERNMENT)

@bot.message_handler(commands=['start_gov'])
def start_gov_command(message):
    bot.send_message(message.chat.id, 'бот правительства запущен')
    parser = dna_parser.PravoGovParser('government')
    parser.pravo_gov_parse(bot, message)

if __name__ == "__main__":
    bot.infinity_polling()

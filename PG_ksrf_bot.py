'''
Бот, который уведомляет о новых документах КС РФ на pravo.gov.ru.
'''
import telebot

import config
import dna_parser

bot = telebot.TeleBot(config.TOKEN_KSRF)

@bot.message_handler(commands=['start_ksrf'])
def start_gov_command(message):
    bot.send_message(message.chat.id, 'бот Конституционного суда запущен')
    parser = dna_parser.PravoGovParser('court')
    parser.pravo_gov_parse(bot, message)

if __name__ == "__main__":
    bot.infinity_polling()

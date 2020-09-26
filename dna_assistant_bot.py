import telebot

import config
import dna_parser

bot = telebot.TeleBot(config.TOKEN)
'''
Уведомляет о новых документах правительства и всех ФОИВ на pravo.gov.ru.
'''

@bot.message_handler(commands=['start_foiv'])
def start_foiv_command(message):
    bot.send_message(message.chat.id, 'бот ФOИВ запущен')
    parser = dna_parser.PravoGovParser('federal_authorities')
    parser.pravo_gov_parse(bot, message)

@bot.message_handler(commands=['start_gov'])
def start_fov_command(message):
    bot.send_message(message.chat.id, 'бот правительства запущен')
    parser = dna_parser.PravoGovParser('government')
    parser.pravo_gov_parse(bot, message)

if __name__ == "__main__":
    bot.infinity_polling()

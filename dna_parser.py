import bs4
import requests
import time


class PravoGovParser:
  '''
  Парсер находит и отправляет через ТГ-бота информацию о новых документах
  в федеральном законодательстве.
  '''
  URL_DICT = {
    'federal_authorities': 'ФОИВ',
    'president': 'Президент',
    'government': 'Правительство',
    'court': 'Конституционный суд',
  }

  def __init__(self, url: str):
    self.body = self.URL_DICT[url]
    self.base_url = 'http://publication.pravo.gov.ru'
    self.url = self.base_url + f'/Search/Period/{url}?type=daily'

  def get_url_docs(self, url: str):
    '''
    Вернуть множество из адресов документов с запрашиваемой страницы.
    '''
    request = requests.get(url)
    page_code = bs4.BeautifulSoup(request.text, 'html.parser')
    a_tag_list = page_code.select('div.td.vis > a.choosedocument')
    url_docs = {
      self.base_url + a_tag.attrs['href'] for a_tag in a_tag_list
    }
    return url_docs

  def get_urls_img_and_doc(self, urls: set):
    '''
    Найти адрес картинки первой страницы по адресу документа.
    Вернуть множество из кортежей с двумя адресами в каждом.
    '''
    urls_img_and_doc = set()
    for url_doc in urls:
      try:
        time.sleep(5)
        request = requests.get(url_doc)
        page_code = bs4.BeautifulSoup(request.text, 'html.parser')
        img_tag = page_code.select('.documentImage')
        url_img = self.base_url + img_tag[0].attrs['src']
        urls_img_and_doc.add((url_img, url_doc))
      except Exception as exc:
        print(f'{exc} при запросе адреса {url_doc}', time.ctime())
        continue
    return urls_img_and_doc

  def pravo_gov_parse(self, bot, message):
    '''
    Находить и отправлять через ТГ-бота информацию о новых документах
    на сайте pravo.gov.ru. Частота обновления - 10 мин.
    Информация включает адрес документа и картинку его первой страницы.
    '''
    round = 0
    print(f'Парсер {self.body} запущен')
    while True:
      try:
        current_urls = self.get_url_docs(self.url)
        round += 1
        if not round % 24: # тестовое сообщение каждые 4 часа (10 мин * 24)
          msg = f'Тест: парсер {self.body} работает в штатном режиме'
          bot.send_message(message.chat.id, msg)
      except Exception as exc:
        msg = f'Не получилось создать текущий список, {exc}, {time.ctime()}'
        bot.send_message(message.chat.id, msg)
        continue
      time.sleep(600)
      flag = True
      while flag:
        try:
          new_urls = self.get_url_docs(self.url)
          diff_urls = new_urls.difference(current_urls)
        except Exception as exc:
          msg = f'Не получилось создать список для сравнения, {exc}'
          bot.send_message(message.chat.id, msg)
          continue

        if diff_urls:
          time.sleep(2)
          urls_img_and_doc = self.get_urls_img_and_doc(diff_urls)
          for url_img, url_doc in urls_img_and_doc:
            try:
              time.sleep(2)
              bot.send_photo(message.chat.id, url_img)
            except Exception as exc:
              msg = f'Не получилось передать картинку {url_img}'
              bot.send_message(message.chat.id, msg)
            time.sleep(2)
            bot.send_message(message.chat.id, url_doc)
          time.sleep(2)
          flag = False

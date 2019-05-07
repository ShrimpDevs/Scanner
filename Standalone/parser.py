import time
import requests
import settings
import datetime
from bs4 import BeautifulSoup
from collections import OrderedDict
 
# для статистики
allCount = 0  # количество сайтов
currCount = 0  # текущее количество обработанных сайтов
linkCount = 0  # количество ссылок
parsedLinkCount = 0  # количество обработанных ссылок
withPrivacy = 0  # количество сайтов с политикой конфиденциальности
abadoned = 0  # количество не работающих сайтов
withSSL = 0  # количество сайтов с SSL

class Parser():

    def currentDateTime(self, mode):
        today = datetime.datetime.today()
        if mode == 'date':
            return today.strftime('%Y.%m.%d %H:%M:%S')
        if mode == 'time':
            return today.strftime('%H:%M:%S')

    #Получаем список ссылок с страницы
    def getLinks(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        links = []
        for i in soup.findAll('a'):
            link = str(i.get('href'))
            links.append(link)
        return links

    def toLogFile(self, time, text):
            f = open('log.txt','a')
            if time == 'time':
                f.write(self.currentDateTime('time'), text + '\n')
            if time == 'date':
                f.write(self.currentDateTime('date'), text + '\n')
            f.close()

    def main(self):
        self.toLogFile('date','Начало сканирования')
        # ссылки с файла в список
        path = settings.testFilePath
        f = open(path, 'r')
        lines = [line.strip() for line in f]
        f.close()

        url_list = []

        # перебор списка сайтов
        for url in lines:

            #uniq_list_links = list(OrderedDict.fromkeys(url_list).keys())
            #links_of_pages = []
            #count = 1
            #for x in url_list:
            #    get_x = requests.get(url + x)
            #    bsoup = BeautifulSoup(get_x.text, 'lxml')
            #    all_hrefs = bsoup.findAll('a')
            #    for link in all_hrefs:
            #        if link not in uniq_list_links:
            #            links_of_pages.append(url + str(link.get('href')))
            #            print(count)
            #            count += 1
            #        else:
            #            continue
            #        
            #print(len(links_of_pages))
            #print(list(OrderedDict.fromkeys(links_of_pages).keys()))
            pass

        self.toLogFile('date','Завершение сканирования')    
        f = open(settings.statsFilePath, 'a')
        f.write('Количество сайтов: ' + str(allCount))
        f.write('Количество обработанных сайтов: ' + str(currCount))
        f.write('Количество ссылок: ' + str(linkCount))
        f.write('Количество обработанных ссылок: ' + str(parsedLinkCount))
        f.write('Количество сайтов с политикой: ' + str(withPrivacy))
        f.write('Количество не работающих сайтов: ' + str(abadoned))
        f.write('Количество сайтов с SSL: ' + str(withSSL))
        f.close()


parser = Parser()
parser.main()
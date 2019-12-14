# -*- coding: utf-8 -*-
import time
import requests
import datetime
from bs4 import BeautifulSoup
from collections import OrderedDict


class Parser():
    # для статистики
    allCount = 0            # количество сайтов
    count = 0               # количество обработанных сайтов
    linkCount = 0           # количество ссылок
    parsedLinkCount = 0     # количество обработанных ссылок
    withPrivacy = 0         # количество сайтов с политикой конфиденциальности
    withTerms = 0           # количество сайтов с условиями обслуживания
    abadoned = 0            # количество не работающих сайтов
    withSSL = 0             # количество сайтов с SSL

    def currentDateTime(self, mode):
        today = datetime.datetime.today()
        if mode == 'date':
            return today.strftime('%Y.%m.%d %H:%M:%S')
        if mode == 'time':
            return today.strftime('%H:%M:%S')

    # Получаем список ссылок с страницы
    def getLinks(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        links = []
        for i in soup.findAll('a'):
            link = str(i.get('href'))
            links.append(link)
        return links

    def toLogFile(self, time, text):
        string = ''
        if time == 'time':
            string = self.currentDateTime('time') + ':' + text + '\n'
        if time == 'date':
            string = self.currentDateTime('date') + ':' + text + '\n'

        print(string.replace('\n', ''))
        f = open('log.txt', 'a+')
        f.write(string)
        f.close()

    def main(self):

        policyKeys = ['Политика конфиденциальности', 'Условия обработки персональных данных',
                      'Privacy Policy', 'Privacy Statement', 'Privacy notice', 'Datenschutz-Bestimmungen',
                      'Datenschutzerklärung', 'Datenschutzbestimmungen', 'Politique de confidentialité',
                      'Política de privacidad', 'Privacybeleid', 'Personvernpolicy', 'Retningslinjer for personvern',
                      'Polityka prywatności', 'Politica de confidentialitate', 'Integritetspolicy', 'Privaatsuspoliitika']

        termsKeys = ['Условия обслуживания', 'Условия использования', 'Условия и положения', 'Правила и условия',
                     'Условия предоставления услуг', 'Terms and Conditions', 'Terms & Conditions', 'Terms of Service', 'Nutzungsbedingungen',
                     'Términos de servicio', 'Términos y Condiciones', 'Termini e condizioni', 'Termini di servizio']

        # формирование ключевых слов
        keywords = []
        for i in policyKeys:
            keywords.append(i)
            keywords.append(i.lower())
            keywords.append(i.upper())

        keywords_terms = []
        for i in termsKeys:
            keywords_terms.append(i)
            keywords_terms.append(i.lower())
            keywords_terms.append(i.upper())

        self.toLogFile('date', 'Начало сканирования')
        startDate = datetime.datetime.now()

        # ссылки с файла в список
        # path = settings.resourcesFilePath
        path = 'international.txt'
        f = open(path, 'r')
        url_list = [line.strip() for line in f]
        f.close()

        # убрать возможные дубликаты
        url_list = list(dict.fromkeys(url_list))

        self.allCount = len(url_list)

        # перебор списка сайтов
        for url in url_list:
            self.count += 1
            countText = str(self.count) + '/' + str(self.allCount)
            try:
                self.toLogFile('time', countText)
                self.toLogFile('time', url)

                # инициализирование
                headers = {'User-Agent': 'Mozilla/5.0'}
                r = requests.get(url, headers=headers, timeout=30)

                # проверка на response code
                if r.status_code != 200:
                    responceText = 'HTTP Response: ' + r.response_code
                    self.toLogFile('time', responceText)
                    self.abadoned += 1
                    continue
                else:
                    self.toLogFile('time', 'HTTP Response: 200')

                # проверка на SSL
                if 'https' in r.url:
                    self.toLogFile('time', 'Обнаружен SSL-сертификат.')
                    self.withSSL += 1

                # подготовка объекта для парсинга
                soup = BeautifulSoup(r.text, 'html.parser')

                # проверки на наличие политики
                privacyLinks = []

                for link in soup.findAll('a', text=keywords):
                    privacyLinks.append(link.get('href'))

                # проверка на уникальность
                privacyLinksBuff = []
                for i in privacyLinks:
                    # корректность ссылки
                    if 'http' not in i.replace('https', 'http'):
                        if i[0] == '/':
                            i = url + i
                        else:
                            i = url + '/' + i
                    privacyLinksBuff.append(i.replace('https', 'http'))

                privacyLinks = list(dict.fromkeys(privacyLinksBuff))

                if len(privacyLinks) > 0:
                    self.withPrivacy += 1
                    privacyText = 'Ссылка на политику:' + privacyLinks[0]
                    self.toLogFile('time', privacyText)
                else:
                    self.toLogFile('time', 'Политика не найдена.')

                ###########################################
                # проверки на наличие условий обслуживания
                termsLinks = []

                for link in soup.findAll('a', text=keywords_terms):
                    termsLinks.append(link.get('href'))

                # проверка на уникальность
                termsLinksBuff = []
                for i in termsLinks:
                    # корректность ссылки
                    if 'http' not in i.replace('https', 'http'):
                        if i[0] == '/':
                            i = url + i
                        else:
                            i = url + '/' + i
                    termsLinksBuff.append(i.replace('https', 'http'))

                termsLinks = list(dict.fromkeys(termsLinksBuff))

                if len(termsLinks) > 0:
                    self.withTerms += 1
                    termsText = 'Ссылка на условия обслуживания:' + \
                        termsLinks[0]
                    self.toLogFile('time', termsText)
                else:
                    self.toLogFile('time', 'Условия обслуживания не найдены.')

            except:
                self.toLogFile('time', 'Неизвестная ошибка.')
                self.abadoned += 1

            # вывод статистики в файл
            f = open('stats.txt', 'w')
            f.write('Количество сайтов: ' + str(self.allCount) + '\n')  # +++
            f.write('Количество обработанных сайтов: ' +
                    str(self.count) + '\n')  # +++
            f.write('Количество сайтов с условиями обслуживания: ' +
                    str(self.withTerms) + '\n')  # ---
            # f.write('Количество обработанных ссылок: ' + str(self.parsedLinkCount) + '\n')  # ---
            f.write('Количество сайтов с политикой: ' +
                    str(self.withPrivacy) + '\n')  # +++
            f.write('Количество не работающих сайтов: ' +
                    str(self.abadoned) + '\n')  # +++
            f.write('Количество сайтов с SSL: ' +
                    str(self.withSSL) + '\n')  # +++
            f.close()

        self.toLogFile('date', 'Завершение сканирования')
        # расчет времени сканирования
        finishDate = datetime.datetime.now()
        c = finishDate - startDate
        time = divmod(c.days * 86400 + c.seconds, 60)
        print('\nВремя сканирования:', time[0], 'мин.', time[1], 'сек.\n')

        # вывод статистики в консоль
        f = open('stats.txt')
        for line in f:
            print(line.replace('\n', ''))
        f.close()


if __name__ == '__main__':
    parser = Parser()
    parser.main()

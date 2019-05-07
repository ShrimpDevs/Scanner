# для статистики
allCount = 0  # количество сайтов
currCount = 0  # текущее количество обработанных сайтов
linkCount = 0  # количество ссылок
parsedLinkCount = 0  # количество обработанных ссылок
withPrivacy = 0  # количество сайтов с политикой конфиденциальности
abadoned = 0  # количество не работающих сайтов
withSSL = 0  # количество сайтов с SSL

# ссылки с файла в список
f = open('C:\\Projects\\Git\\Scanner\\resources.txt', 'r')
lines = [line.strip() for line in f]
f.close()

# перебор списка
for l in lines:
    print(l)

f = open('C:\\Projects\\Git\\Scanner\\stats.txt', 'w')
f.write('Количество сайтов: ' + str(allCount))
f.write('Текущее количество обработанных сайтов: ' + str(currCount))
f.write('Количество ссылок: ' + str(linkCount))
f.write('Количество обработанных ссылок: ' + str(parsedLinkCount))
f.write('Количество сайтов с политикой: ' + str(withPrivacy))
f.write('Количество не работающих сайтов: ' + str(abadoned))
f.write('Количество сайтов с SSL: ' + str(withSSL))
f.close()

from bs4 import BeautifulSoup
import requests


def pars(title):
    a = 'fail'
    if title == "BabyBus":
        res = requests.get('https://www.babybus.com/global/ru/index')
        soup = BeautifulSoup(res.text, 'lxml')
        a = str(soup.find_all('div', class_='index_cont__8GUDo'))
        a = a[len('[<div class="index_cont__8GUDo">   '):-len('</div>]')]
    if title == 'Играемся':
        res = requests.get('https://www.igraemsa.ru/')
        soup = BeautifulSoup(res.text, 'lxml')
        a = str(soup.find_all('p'))
        a = a[len('[<p>В играх новые знания усваиваются гораздо легче! Именно поэтому <b>детские'
                  ' развивающие игры</b> – это прекрасный способ сделать процесс обучения ребёнка увлекательным'
                  ' и более эффективным.</p>, <p>'):-1284]
    if title == 'Саго Мини':
        a = 'Коллекция из более чем 40 обучающих игр «Мир Sago Mini: Игры для детей» предназначена для дошкольников' \
            ' от 2 до 5 лет. Вместе с героями Sago — Харви, Джинджей, Робином и Джеком — малыши исследуют космос, ' \
            'встретятся с динозаврами, построят робота, совершат глубоководное погружение, научатся управлять ' \
            'пожарной машиной и т.д. Кроме того, в «Мир Sago Mini: Игры для детей» можно создать до 5 собственных' \
            ' персонажей и придумывать собственные истории. Открытый мир игры поощряет детей использовать воображение' \
            ' и креативность на полную мощь! У вас, как у родителей, есть выбор: присоединиться к детским' \
            ' развлечениям или следить за игрой через специальное приложение Sago Mini Parents, которое ежедневно' \
            ' предоставляет фотоснимки, видео и обновления.'
    if title == 'Вульфмания':
        res = requests.get('https://wulfmania.com/')
        soup = BeautifulSoup(res.text, 'lxml')
        b = str(soup.find_all('p', limit=5)).split('</p>, <p>')
        b = ''.join(b).split('\n')
        a = []
        for i in range(len(b)):
            b[i] = b[i].strip()
            if b[i] != '</p>]' and b[i] != '[<p>':
                a.append(b[i])
        f = a[0]
        b = a[1:]
        a = f
        for i in range(len(b) - 1):
            op = b[i].endswith('!')
            if b[i + 1] == '' and op is not True:
                a = a + b[i] + '. '
            elif b[i + 1] != '' and op is not True:
                a = a + b[i] + ' '
            elif b[i + 1] == '' and op is True:
                a = a + b[i]
        a += '.'
    if title == 'Айкьюша':
        res = requests.get('https://iqsha.ru/')
        soup = BeautifulSoup(res.text, 'lxml')
        a = soup.find_all('p', limit=5)
        b = a[1:]
        a = b
        for i in range(len(a)):
            if str(a[i]).startswith('<p>') and str(a[i]).endswith('</p>'):
                a[i] = str(a[i])[3:-4]
        a = ''.join(a)
        a = a.split('\n')
        for i in range(len(a)):
            a[i] = a[i].strip()
            if i == 0:
                b = a[i][:len(
                    'Задания и упражнения на сайте нацелены на всестороннее развитие детей разных возрастных групп.')]
                c = a[i][
                    len('Задания и упражнения на сайте нацелены на всестороннее развитие детей разных возрастных групп.<span class="purple">'):len(
                        'Задания и упражнения на сайте нацелены на всестороннее развитие детей разных возрастных групп.<span class="purple">Для малышей от 2 до 4 лет')]
                d = a[i][
                    len('Задания и упражнения на сайте нацелены на всестороннее развитие детей разных возрастных групп.<span class="purple">Для малышей от 2 до 4 лет</span>'):]
                a[i] = b + ' ' + c + d
            if i == 1:
                b = a[i][:len('стимулирующие тягу к знаниям и позволяющие легко усваивать новый материал.')]
                c = a[i][
                    len('стимулирующие тягу к знаниям и позволяющие легко усваивать новый материал.<span class="purple">'):len(
                        'стимулирующие тягу к знаниям и позволяющие легко усваивать новый материал.<span class="purple">Для детей-дошкольников от 5 до 7 лет')]
                d = a[i][
                    len('стимулирующие тягу к знаниям и позволяющие легко усваивать новый материал.<span class="purple">Для детей-дошкольников от 5 до 7 лет</span>'):]
                a[i] = b + ' ' + c + d
        a = ' '.join(a)
    if title == 'Математика и Логика для детей':
        res = requests.get('https://5mod.ru/programmy/razvlecheniya/20415-matematika-i-logika-dlja-detej-181-mod-polnaja-versija.html?ysclid=lgcd3yvvak21525195')
        soup = BeautifulSoup(res.text, 'lxml')
        a = str(soup.find_all('div', itemtype="description"))
        a = a[a.find('-') + 2:-20].capitalize()
    if title == 'Сказки и головоломки для детей':
        res = requests.get('https://5mod.ru/igry/child-game/20080-skazki-i-razvivajuschie-igry-dlja-detej-malyshej-2110-mod-polnaja-versija.html')
        soup = BeautifulSoup(res.text, 'lxml')
        a = str(soup.find_all('div', itemtype="description"))
        a = a[a.find('-') + 2:-20].capitalize()
    if title == 'ЛогикЛайк':
        a = 'ЛогикЛайк — первая и единственная онлайн-платформа для развития логики и математических способностей' \
            ' во всем русскоязычном интернете. Комплекс включает все известные способы решения задач и основывается ' \
            'на современных подходах к обучению детей. Наша первостепенная задача — развить у ребенка логическое' \
            ' мышление, научить рассуждать и не бояться сложных задач.'
    if title == 'Тиллионлайн':
        a = 'Oбучающая онлайн-платформа для занятий с дошкольниками. Сервис предлагает интересные задания в игровой' \
            ' форме. Весь процесс малыша сопровождает новый друг – ' \
            'зайчик Тилли. Малыши быстро вовлекаются в новое занятие в том числе благодаря красивой яркой анимации ' \
            'и качественной озвучке. Индивидуально составленный план учитывает все особенности ребенка.'
    if title == 'Дети-Онлайн':
        a = 'Oбширная платформа, где родители находят всё, что необходимо для развития ребенка: аудиосказки; сказки;' \
            ' раскраски; песни; стихотворения; басни; уроки рисования; поделки; раннее развитие; мультфильмы. ' \
            'Весь необходимый контент можно скачать и использовать в занятиях с ребенком. Примечательно, что здесь' \
            ' собраны самые свежие серии любимых мультфильмов, раскрасок по мотивам известных фильмов и прочее.' \
            ' Представлен контент не только для дошкольников, но и для ребят постарше. Платформа абсолютно бесплатна,' \
            ' все материалы выложены в открытый доступ.'
    if title == 'Талантикум':
        a = 'Талантикум позиционируется как занимательная онлайн-академия для детей от 2-х лет. Видео-курсы' \
            ' разработаны специально для всестороннего развития детей, активного вовлечения в новые сферы жизни, ' \
            'наконец, социализации. Родители могут выбрать как один курс, так и все сразу. Система не перегружает ' \
            'ребенка, даже если он занимается всеми предложенными активностями.'
    if title == 'Сказбука':
        res = requests.get('https://skazbuka.com/')
        soup = BeautifulSoup(res.text, 'lxml')
        a = str(soup.find_all('div', class_="t480__descr t-descr t-descr_md", limit=3)).split('<div class="t480__descr '
                                                                                              't-descr t-descr_md" field="'
                                                                                              'descr" style="">')
        a = a[1:]
        for i in range(len(a)):
            if a[i] != a[-1]:
                a[i] = a[i][:-8]
            else:
                a[i] = a[i][:-7]
        a = ' '.join(' '.join(a).split('<br/>'))
    return a


'''# пример запроса меток
res = requests.get('https://kanobu.ru/games/popular')
soup = BeautifulSoup(res.text, 'lxml')
a = str(soup.find_all('div', class_='knb-cell'))
games = []  # метки игры на сайте
a = a.split('href="')
a.pop(0)
for i in a:
    i = i[7:-1]
    index = i.find("/")
    games.append(i[0:index])
games = list(set(games))
print(games)'''

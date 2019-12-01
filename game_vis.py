# импортирую графическую библиотеку
from tkinter import *

# константы
windowWidth = 700
windowHeight = 600
# локальный сдвиг клавиатуры, виселицы по оси х (удобно, если слева необходимо будет что-то вставить)
delta = 40
# локальный сдвиг слова (для еффекта центрирования)
wordDelta = -120
#алфавит языка, на котором происходит игра (при желании можно играть на другом яызке, заменив алфавит)
alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
#клавиатура
btn = {}
#кол-во раундов в игре
games = 6

# статус игры
firstPlayerScore = 0
secondPlayerScore = 0
# отгадывает первый игрок
isFirstPlayer = False
# ход первого игрока
isFirstPlayerMove = True
# текущий раунд
currentRound = 0

#создание главного окна
root = Tk()
root.title("Виселица")
#полотно (то, на чем рисуется)
canvas = Canvas(root, width=windowWidth, height=windowHeight)
canvas.pack()


# создаем стартовую кнопку
btn01 = Button()
# кнопка Готово/Дальше
btn02 = Button()
# кнопка для правил
btn03 = Button()
# кнопка для выхода
btn04 = Button()

# прорисовка заднего фона (тетрадный лист)
def but():
    # размеры клеточек
    widthOfRect = 16
    heightOfRect = 16
    y = 0
    while y < windowHeight:
        x = 0
        while x < windowWidth:
            # внутренние квадратики
            canvas.create_rectangle(x, y, x + widthOfRect, y + heightOfRect, fill="white", outline="blue")
            x += widthOfRect
        y += heightOfRect
    # красная линия
    canvas.create_line(5 * widthOfRect, 0, 5 * widthOfRect, windowHeight, width=1, fill="red")

# прорисовка виселицы
def drawGallows():
    canvas.create_line(10, 400, 10, 8, width=4)
    canvas.create_line(10, 10, 200, 10, width=4)
    canvas.create_line(10, 100, 100, 10, width=4)
    canvas.create_line(delta + 100, 60, delta + 100, 10, width=5, fill="brown")

# прорисовка головы
def head():
    canvas.create_oval(delta + 79, 60, delta + 120, 100, width=4, fill="white")
    root.update()

# прорисовка туловища
def body():
    canvas.create_line(delta + 100, 100, delta + 100, 200, width=4)
    root.update()

# прорисовка правой руки
def handR():
    canvas.create_line(delta + 100, 100, delta + 145, 200, width=4)
    root.update()

# прорисовка левой руки
def handL():
    canvas.create_line(delta + 100, 100, delta + 45, 200, width=4)
    root.update()

# прорисовка правой ноги
def legR():
    canvas.create_line(delta + 100, 200, delta + 145, 300, width=4)
    root.update()

# прорисовка левой ноги
def legL():
    canvas.create_line(delta + 100, 200, delta + 45, 300, width=4)
    root.update()

# правила
def drawRules():
    faq = '''

        Один из игроков загадывает слово — пишет на бумаге первую
        и последнюю букву слова и отмечает места для остальных 
        букв, например чертами (существует также вариант, когда
        изначально все буквы слова неизвестны). Также рисуется 
        виселица с петлёй. Согласно традиции русских 
        лингвистических игр, слово должно быть именем 
        существительным, нарицательным в именительном падеже 
        единственного числа, либо множественного числа при 
        отсутствии у слова формы единственного числа. Второй игрок 
        предлагает букву, которая может входить в это слово. 
        Если такая буква есть в слове, то компьютер пишет её 
        над соответствующими этой букве чертами — столько раз, 
        сколько она встречается в слове. Если такой буквы нет, то к 
        виселице добавляется круг в петле, изображающий голову. 
        Второй игрок продолжает отгадывать буквы до тех пор, пока не 
        отгадает всё слово. За каждый неправильный ответ первый 
        игрок добавляет одну часть туловища к виселице (обычно их 6: 
        голова, туловище, 2 руки и 2 ноги). Если туловище в виселице
        нарисовано полностью, то отгадывающий игрок проигрывает, 
        считается повешенным. Если игроку удаётся угадать слово, он 
        выигрывает и может загадывать слово. Игра до 6 раундов.
    '''
    canvas.create_text(350, 250, text=faq, fill="black", font=("Helvetica", "15", "bold"))

# переменные для ввода
startWord = ""
countOfLetters = 0

# метод отображения счета
def drawScore():
    # очищаю надписи с соответсвующими тегами
    canvas.delete("first_score")
    canvas.delete("second_score")
    canvas.delete("move")
    # создаю надписи
    canvas.create_text(380, 40, text="Первый:", fill="blue", font=("Helvetica", "25"), tag="first")
    canvas.create_text(375, 80, text="Второй:", fill="blue", font=("Helvetica", "25"), tag="second")
    canvas.create_text(370, 120, text="Ходит:", fill="blue", font=("Helvetica", "25"), tag="moving_text")
    canvas.create_text(470, 40, text=str(firstPlayerScore), fill="red", font=("Helvetica", "25"), tag="first_score")
    canvas.create_text(470, 80, text=str(secondPlayerScore), fill="red", font=("Helvetica", "25"), tag="second_score")
    canvas.create_text(480, 120, text="Первый" if isFirstPlayerMove else "Второй", fill="red", font=("Helvetica", "25"), tag="move")

# метод ввода
def input():
    global btn01; btn01.destroy()
    global btn03; btn03.destroy()
    global btn04; btn04.destroy()

    # слово, которое вводиться (сделал отдельной переменной, чтобы с ней можно было проводить различные манипуляции)
    global startWord; startWord = ""
    global countOfLetters; countOfLetters = 1
    # отрисовка фона, виселицы, счета
    but()
    drawGallows()
    drawScore()

    # кнопка, по нажатию на которую начинает угадывать другой игрок
    global btn02
    btn02 = Button(root, text="Готово", width=10, height=2, command=lambda: arr())
    btn02.place(x=570, y=542)
    btn02["bg"] = "red"
    btn02["state"] = "disabled"

    # функция заполнения
    def fillingOut(v):
        global countOfLetters
        global startWord
        # в условиях ограничения по кол-ву букв в слове
        if len(startWord) < 16:
            # отрисовываем буквы
            canvas.create_text(delta + wordDelta + 150 + 32 * countOfLetters, 370, text=v, fill="blue", font=("Helvetica", "22"))
            startWord += str(v)
            countOfLetters+=1
        if len(startWord) > 1:
            btn02["state"] = "normal"

    # создание графической клавиатуры
    def gen(u, x, y):
        btn[u] = Button(root, text=u, width=5, height=2, command=lambda: fillingOut(u), font=("Helvetica", "9"))
        btn[u].place(x=str(x), y=str(y))

    # отрисовка 3-х рядов клавиатуры
    x = delta
    y = 410
    for i in alphabet[0:12]:
        gen(i, x, y)
        x += 50
    x = delta + 20
    for i in alphabet[12:23]:
        gen(i, x, y + 44)
        x += 50
    x = delta + 40
    for i in alphabet[23:33]:
        gen(i, x, y + 88)
        x += 50

# метод отгадывания слова
def arr():
    # меняю исполнителя текущего хода
    global isFirstPlayerMove
    isFirstPlayerMove = not isFirstPlayerMove
    # кнопка Дальше/Готово, делаю недоступным к нажатию
    global btn02
    btn02["state"] = "disabled"

    # отрисовка фона, виселицы, счета
    but()
    drawGallows()
    drawScore()

    # назначаю слово для угадывания
    word = startWord
    # вычисляю величину смещения по кол-ву букв в слове
    wordDelta = (8 - len(word))*10
    # список букв в слове
    wo = word[0:]
    # лист букв для отрисовки
    wor = []
    # для отрисовки на нужном месте по оси х
    c = 0
    for i in wo:
        wor.append(i)
        canvas.create_text(delta + wordDelta + 150 + 32*c, 370, text="_", fill="blue", font=("Helvetica", "22"))
        c+=1

    # список чисел от 0 до длины слова
    list1 = [i for i in range(len(word))]
    # ошибки
    er = []
    # победные буквы (угаданные)
    win = []

    # метод окончания раунда
    def finish():
        # кнопку Далее делаю недоступной
        global btn02
        btn02["state"] = "disabled"
        # увеличиваю текущий раунд
        global currentRound
        currentRound += 1

        #отрисовка счета
        drawScore()
        # если было сыграно необходимое кол-во раундов
        if currentRound == games:
            # удаляю текст Угадал/Не угадал
            canvas.delete("roundText")
            # показываю победителя или сообщаю о ничьей
            if firstPlayerScore > secondPlayerScore:
                canvas.create_text(450, 250, text="Победил первый", fill="green", font=("Helvetica", "34"))
            elif firstPlayerScore < secondPlayerScore:
                canvas.create_text(450, 250, text="Победил второй", fill="green", font=("Helvetica", "34"))
            else:
                canvas.create_text(450, 250, text="Ничья", fill="green", font=("Helvetica", "34"))
            # предлагаю выйти в меню
            global btn01
            btn01 = Button(root, text="В меню", width=10, height=2, command=lambda: menu())
            btn01.place(x=10, y=542)
            btn01["bg"] = "red"
        else:
            # перехожу на следующего угадывающего
            global isFirstPlayer
            isFirstPlayer = not isFirstPlayer
            # предлагаю перейти к следующему раунду
            btn02["state"] = "norm"
            btn02 = Button(root, text="Дальше", width=10, height=2, command=lambda: input())
            btn02.place(x=570, y=542)
            btn02["bg"] = "red"

    # метод проверки правильности буквы (есть ли она в слове)
    def a(v):
        # если буква в слове
        if v in wor:
            # показываю ее над черточкой и помечаю на клавиатуре букву зеленой (больше ее нельзя нажать)
            ind = wor.index(v)
            b2 = list1[ind]
            wor[ind] = '1'

            x1, y1 = coord(b2)
            win.append(v)
            canvas.create_text(x1, y1, text=wo[ind], fill="blue", font=("Helvetica", "18"))
            btn[v]["bg"] = "green"
            btn[v]["state"] = "disabled"

            if not v in word:
                btn[v]["state"] = "disabled"
            # для пометки всех букв заменяю каждое первое вхождение буквы на 1 в слове
            while v in wor:
                win.append(v)
                ind2 = wor.index(v)
                wor[ind2] = '1'
                b2 = list1[ind2]
                x1, y1 = coord(b2)
                canvas.create_text(x1, y1, text=wo[ind2], fill="blue", font=("Helvetica", "18"))

            # если угаданы все буквы
            if len(win) == len(word):
                canvas.create_text(450, 250, text="Решено!", fill="green", font=("Helvetica", "34"), tag="roundText")
                # увеличиваю кол-во отгаданых слов соответсвующего игрока
                if isFirstPlayer:
                    global firstPlayerScore
                    firstPlayerScore+=1
                else:
                    global secondPlayerScore
                    secondPlayerScore+=1

                # делаю клавиатуру недоступной к нажатию и завершаю раунд
                for i in alphabet:
                    btn[i]["state"] = "disabled"
                finish()
        else:
            # помечаю данную кнопку на клавиатуре красным (больше недоступно к нажатию)
            er.append(v)
            btn[v]["bg"] = "red"
            btn[v]["state"] = "disabled"
            # по номеру ошибки дорисовываю соответствующую часть тела
            if len(er) == 1:
                head()
            elif len(er) == 2:
                body()
            elif len(er) == 3:
                handL()
            elif len(er) == 4:
                handR()
            elif len(er) == 5:
                legL()
            else:
                legR()
                # если последняя часть тела - раунд проигран
                lose()
            # после отрисовки обновляю окно (для корректной отрисовки)
            root.update()

    # координата соответсвующей буквы слова на canvas
    def coord(b2):
        i = 0
        while 1:
            if b2 == i:
                x1, y1 = delta + wordDelta + 150 + i * 32, 370
                break
            i += 1
        return x1, y1

    # клавиатура (также как и в input (можно усложнить логику и вынести в отдельный метод))
    def gen(u, x, y):
        btn[u] = Button(root, text=u, width=5, height=2, command=lambda: a(u), font=("Helvetica", "9"))
        btn[u].place(x=str(x), y=str(y))

    # отрисовка 3-х рядов клавиатуры
    x = delta
    y = 410
    for i in alphabet[0:12]:
        gen(i, x, y)
        x += 50
    x = delta + 20
    for i in alphabet[12:23]:
        gen(i, x, y + 44)
        x += 50
    x = delta + 40
    for i in alphabet[23:33]:
        gen(i, x, y + 88)
        x += 50

    # метод проиграша раунда
    def lose():
        canvas.create_text(450, 250, text="Не решено!", fill="red", font=("Helvetica", "34"), tag="roundText")
        # показываю буквы, которые не были отгаданы
        wordCopy = word
        for i in word:
            if not i in win:
                x1, y1 = coord(wordCopy.index(i))
                canvas.create_text(x1, y1, text=i, fill="red", font=("Helvetica", "18"))
                index = wordCopy.index(i)
                wordCopy = wordCopy[:index] + '1' + wordCopy[index + 1:]

        for i in alphabet:
            btn[i]["state"] = "disabled"
        finish()

# правила
def rules():
    # чищу кнопки из меню
    global btn01;btn01.destroy()
    global btn03;btn03.destroy()
    global btn04;btn04.destroy()

    # отрисовка фона и правил соответсвенно
    but()
    drawRules()
    # кнопка выхода назад в меню
    btn03 = Button(root, text="Назад", width=15, height=2, command=lambda: menu(), font=("Helvetica", "10"))
    btn03.place(x=15, y=545)
    btn03["bg"] = "red"

# меню
def menu():
    # вызываю глобальные переменные, чтобы в дальнейшем в данном методе не считало локальным
    global firstPlayerScore;global secondPlayerScore;global isFirstPlayer;global isFirstPlayerMove;global currentRound;
    firstPlayerScore = 0
    secondPlayerScore = 0
    isFirstPlayer = False
    isFirstPlayerMove = True
    currentRound = 0
    # очищаю все
    global root; global canvas;
    canvas.destroy()
    canvas = Canvas(root, width=windowWidth, height=windowHeight)
    canvas.pack()
    global btn01;btn01.destroy()
    global btn02;btn02.destroy()
    global btn03;btn03.destroy()
    global btn04;btn04.destroy()

    # начинаю отрисовывать
    but()
    drawGallows()
    head(); legL(); legR(); handL(); handR(); body();
    canvas.create_text(480, 50, text="Виселица", fill="black", font=("Helvetica", "60"), tag="menuText")
    btn01 = Button(root, text="Начать", width=15, height=2, command=lambda: input(), font=("Helvetica", "25"))
    btn01.place(x=325, y=142)
    btn01["bg"] = "red"
    btn03 = Button(root, text="Правила", width=15, height=2, command=lambda: rules(), font=("Helvetica", "25"))
    btn03.place(x=325, y=265)
    btn03["bg"] = "red"
    btn04 = Button(root, text="Выйти", width=15, height=2, command=lambda: root.destroy(), font=("Helvetica", "25"))
    btn04.place(x=325, y=388)
    btn04["bg"] = "red"

#запускаю меню
menu()
root.mainloop()
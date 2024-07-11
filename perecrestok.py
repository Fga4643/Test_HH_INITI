# ©Copyright by Fga4643
import time  # Внесено для таймеров
import threading  # Внесено для эмуляции разных устройств
import random  # Внесено для тестирования, не нужно в экспулатации
'''
Светофоры пешеходов на одной стороне разделены на главный и подчиненный
Включаются одновременно, так как если проход возможен, значит возможен в обе стороны
Управляющий светофор всего 1, так как иначе придется решать задачу
синхронизации, что значительно усложнит код и обслуживание.
Для проверки включен модуль random, который будет изображать количество людей на
светофорах
waited - кол-во людей на светофоре
soobch - потоки связи, каждый отвечает за свой светофор
svetofors - цвет светофора [0,1,2]-красный, желтый, зеленый соответственно
cars - машины
chel - люди
'''
waited_cars = [6, 0, 7, 0]  # Зрение дорожных светофоров
waited_chel = [0, 0, 4, 3, 0, 0, 0, 0]  # Зрение пешеходных светофоров

soobch_cars = [[0, 0, 0, 0, 0, 0, 0, 0], "",
               "", "", ""]  # Потоки общения для светофоров

soobch_chel = [[0, ""], [0, ""], [0, ""], [
    0, ""], [0, ""], [0, ""], [0, ""], [0, ""]]  # Потоки общения для пешеходных
svetofors_cars = [0, 0, 0, 0]  # Светофор машин
svetofors_chel = [0, 0, 0, 0, 0, 0, 0, 0]  # Светофор пешеходов
timer = 5  # Начальный таймер
timer_min = 5  # Минимальный таймер


def sveto_cars(svetofor_ind):
    while True:
        reche = []  # Создание пустого списка для записи
        # Вычисление количества ожидающих машин для коэффицента
        koif = waited_cars[svetofor_ind]
        if svetofor_ind != 0:  # Выполняется всеми кроме первого светофора, выведено отдельно
            # Для "отдельной" эмуляции поведения не управлябщего
            soobch_cars[0][svetofor_ind] = koif
            # светофора
        else:
            soobch_cars[0][svetofor_ind] = koif
            # Поиск максимальной очереди, "коэффицента"
            index_max = (soobch_cars[0]).index(max(soobch_cars[0]))
            if index_max > timer:  # Если длина очереди больше возможного проезда, удлиняется желтый
                index_max = timer_min + index_max // 4  # Динамическая длина желтого света
            if index_max < 4:  # Если из дорожных светофоров
                reche.append(index_max)  # Запись кого изменил
                # Включение светофора с наибольшей очередью
                soobch_cars[index_max + 1] = "vklu"
                # Поиск параллельного пешеходного
                peche_ind = [6, 7, 4, 5][index_max]
                cars_ind = (index_max + 2) % 4
                # сверка с пешеходным, который может помешать второй полосе
                if soobch_cars[0][cars_ind] >= soobch_cars[0][peche_ind]:
                    reche.append(cars_ind)  # Запись кого изменил
                    # Включение светофора параллельного наибольшей очереди
                    soobch_cars[cars_ind + 1] = "vklu"
                else:
                    reche.append(peche_ind)  # Запись кого изменил
                    # Включение пешеходного параллельного наибольшей очереди
                    soobch_chel[(peche_ind - 4) * 2][1] = "vklu"
            else:
                reche.append(index_max)  # Запись кого изменил
                # Включение пешеходного с наибольшей очередью
                soobch_chel[(index_max - 4) * 2][1] = "vklu"
                started = [[2, 5, 6, 7], [3, 4, 7, 6], [
                    0, 4, 5, 7], [1, 4, 5, 6]][index_max - 4]  # Поиск коэффицентов всех взаимомешающих путей
                koefii = started.copy()  # Копия нашей выборки
                for i in range(4):
                    # Заполнение коэффицентов по путям
                    koefii[i] = [soobch_cars[0][koefii[i]], koefii[i]]
                koefii.sort()  # Сортировка по возрастанию коэффицентов
                if koefii[-1][1] < 4:  # Если наибольший коэффицент у дороги
                    reche.append(koefii[-1][1])  # Запись кого изменил
                    # Включается дорога параллельная изанчальной
                    soobch_cars[koefii[-1][1]] = "vklu"
                else:
                    # Выбор всех пешеходных светофоров за счет изначальной сортировки списка
                    sveto_spis = started[1:]
                    # Внесение всех изменяемых светофоров
                    reche.extend(sveto_spis)
                    for i in sveto_spis:
                        # Включение пешеходных
                        soobch_chel[(i - 4) * 2][1] = "vklu"
            # Эта часть выключает все светофоры, которые не внесены в список измененных
            for i in range(8):
                if i not in reche:
                    if i < 4:
                        # Выключение дорожного светофора
                        soobch_cars[i + 1] = "vikl"
                    else:
                        # Выключение пешеходного светофора
                        soobch_chel[(i - 4) * 2][1] = "vikl"
        # Если должен включиться и не включен
        if soobch_cars[svetofor_ind + 1] == "vklu" and svetofors_cars[svetofor_ind] != 2:
            svetofors_cars[svetofor_ind] = 1  # Включение желтого
            time.sleep(timer)  # Таймер желтого
            svetofors_cars[svetofor_ind] = 2  # Включение зеленого
        # Если должен выключиться и не выключен
        elif soobch_cars[svetofor_ind + 1] == "vikl" and svetofors_cars[svetofor_ind] != 0:
            svetofors_cars[svetofor_ind] = 1  # Включение желтого
            time.sleep(timer)  # Таймер желтого
            svetofors_cars[svetofor_ind] = 0  # Включение красного
        time.sleep(1)  # Можно убрать, внес для снижения нагрузки на железо


def sveto_chels(svetofor_ind):
    koif = 0  # Коэффицент занятости
    koif_par = 0  # Коэффицент занятости второго светофора
    while True:
        koif = waited_chel[svetofor_ind]  # Вычисление коэффицента
        if svetofor_ind % 2 == 0:  # Проверка главный ли из пары
            # Дублирование сигнала на ведомый
            soobch_chel[svetofor_ind + 1][1] = soobch_chel[svetofor_ind][1]
            # просмотр коэффицента ведомого
            koif_par = soobch_chel[svetofor_ind + 1][0]
            koif += koif_par  # вычисление парного коэффицента
            # Сообщение коэффицента главному светофору с множителем
            soobch_cars[0][svetofor_ind // 2 + 4] = koif // 2
        else:  # Если не главный
            # сообщение главному из пары своей занятости
            soobch_chel[svetofor_ind][0] = koif

        # включение по сигналу зеленого
        if soobch_chel[svetofor_ind][1] == "vklu" and svetofors_chel[svetofor_ind] != 2:
            time.sleep(timer)  # Таймер для выключение дорожного зеленого
            svetofors_chel[svetofor_ind] = 2  # Включение зеленого
        elif soobch_chel[svetofor_ind][1] == "vikl":  # включение по сигналу красного
            svetofors_chel[svetofor_ind] = 0  # Включение красного
        time.sleep(1)  # Можно убрать, внес для снижения нагрузки на железо


def yprav_imp():  # Внесено для эмуляции жизни
    while True:
        for i in range(len(waited_cars)):
            waited_cars[i] = random.randint(0, 10)  # Сколько машин на дороге
        for i in range(len(waited_cars)):
            # Сколько людей на каждом светофоре
            waited_chel[i] = random.randint(0, 15)
        time.sleep(15)


# Эта часть эмцлирует разные устройства, запуская потоки с функциями
pecheh_svet = []
for i in range(8):  # Включение пешеходных
    pecheh_svet.append(threading.Thread(
        target=sveto_chels, args=[i]))  # Заполнение потока
    pecheh_svet[-1].start()  # Включение потока
time.sleep(2)
cars_svet = []
for i in range(4):  # Включение дорожных
    cars_svet.append(threading.Thread(target=sveto_cars, args=[i]))
    cars_svet[-1].start()  # Включение потока
# Эмцлирующая функция тоже в потоке
testing = threading.Thread(target=yprav_imp)
testing.start()  # Старт потока
while True:
    print("Дорожные против часовой", *soobch_cars[0][:4])
    print("Пешеходные дублированные против часовой", *soobch_cars[0][4:])
    print(f"    {svetofors_chel[7]}|   |   |{svetofors_chel[6]}")
    print(
        f"  {svetofors_chel[0]}  | {svetofors_cars[0]} |   |  {svetofors_chel[5]}")
    print("-----+       +-----")
    print(f"              {svetofors_cars[3]}     ")
    print("------       ------")
    print(f"    {svetofors_cars[1]}            ")
    print("-----+       +-----")
    print(
        f"  {svetofors_chel[1]}  |   | {svetofors_cars[2]} |  {svetofors_chel[4]}")
    print(f"    {svetofors_chel[2]}|   |   |{svetofors_chel[3]}")

    print("_________")
    time.sleep(1)
# Эмуляции проезда не сделал, так как увы это усложнит код и не приведет к улучшению функционала
# ©Copyright by Fga4643

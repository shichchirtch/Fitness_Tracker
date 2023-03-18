import datetime as DT
from pprint import pprint
from random import randint

print("Вашему вниманию предлагается инновационный Фитнесс-Трекер TRACE-1\nСледуйте инструкциям !")
pattern = '%d.%m.%Y'
fitness_dairy = []
min_speed, max_speed =0, 7200  # м\ч
limit_distance = 86400
FORMAT = "%H:%M:%S"  # Запишите формат полученного времени.

def check_size_step(step):
    if 30 < step < 130:
        return step
    print("Something goes wrong ! Take another attempt !")
    check_weight(input("Введите среднюю длину вашего шага в см\n"))

one_step = check_size_step(int(input("Введите среднюю длину вашего шага в см\n")))

def check_weight(ves):
    if isinstance(ves, int) and 30 < ves < 120:
        return ves
    else:
        print('Ошибка данных\nВведите свой вес !\n')
        check_weight(int(input()))

def check_height(rost: int):
    if isinstance(rost, int) and 100 < rost < 220:
        return rost
    else:
        print('Ошибка данных\nВвведите свой рост в см !\n')
        check_height(int(input()))


def enter_start_day():
    first_day = input('Введите дату начала измерений в формате "ДД.ММ.ГГГГ\n')  # 18.03.2023
    try:
        dt_obj = DT.datetime.strptime(first_day, pattern)
        return dt_obj
    except Exception:
        print('Неверный формат даты\n')
        enter_start_day()


WEIGHT = check_weight(int(input("Введите ваш вес в кг\n")))  # Вес.
HEIGHT = check_height(int(input("Введите ваш рост в см\n")))  # Рост.
K_1, K_2 = 0.035, 0.029  # Коэффициент для подсчета калорий.


def proceeding_counting(us_dict):
    """Функция очищает словарь и рекурсивно вызывает form_new_data"""
    print("Если вы хотите продолжить работу с трекером нажмите пробел")
    choice = input()
    if choice == ' ':
        us_dict.clear()
        new_day = start_day + DT.timedelta(hours=24)
        print(new_day.date())
        us_dict[new_day] = (0, 0)
        form_new_data()
        # return us_dict
    else:
        print("Спасибо, что воспользовались нашим трекером !")
        return

def count_total_distance(user_dict):
    '''Функция возвращает количество шагов уже сделанное за день'''
    s = sum(map(lambda x:x[1], user_dict.values()))
    return int(s / one_step)


start_day = enter_start_day()
day_dict = {start_day: (0, 0)}


def get_spent_calories(dist: int, current_time):
    """Получить значения потраченных калорий."""
    mean_speed = dist / current_time / 1000
    spent_calories = (K_1 * WEIGHT + (mean_speed ** 2 / HEIGHT) * K_2 * WEIGHT) * current_time * 60
    return int(spent_calories)


def form_new_data():
    """Функция формирует случайным образом данные для времени и количества шагов"""
    print(f'Контроль номер {len(day_dict)}')
    press_time_button = randint(60, 43200)  # Время от 1 минуты до 12 часов
    # print('промежуток времени в секундах со времени последнего нажатия = ', press_time_button)
    td_obj = DT.timedelta(seconds=press_time_button)
    time_in_hours = round(td_obj.seconds / 3600, 2)
    last_pressing_time = sorted(day_dict)[-1]
    time_in_seconds = last_pressing_time.hour * 3600 + last_pressing_time.minute * 60 + last_pressing_time.second
    if time_in_seconds + td_obj.seconds > 86399 : #or count_total_distance(day_dict) > limit_distance:
        print('\nв сутках кончилось время или превышен предел физической нагрузки\n'.upper())
        show_message_for_last_day()
        fitness_dairy.append(day_dict.copy())
        proceeding_counting(day_dict)
    else:
        print("эти сутки ещё продолжаются")
        press_time = last_pressing_time + td_obj
        middle_speed_for_this_period = randint(min_speed, max_speed)
        distanse_for_this_period = round(middle_speed_for_this_period * round(press_time_button / 3600, 2), 2)
        number_of_steps = int(distanse_for_this_period // round(one_step / 100, 0))
        day_dict[press_time] = (number_of_steps, get_spent_calories(int(number_of_steps * one_step / 100), time_in_hours))
        print('Если хотите посмотреть результаты за этот спринт нажмите 1')
        temp = input()
        if temp == '1':
            show_my_results_till_now(day_dict)
            form_new_data()
        else:
            form_new_data()

def show_my_results_till_now(us_dict):
    '''Функция показывает значения во время контроля '''
    calor = step = 0
    for time, res in us_dict.items():
        step += res[0]
        calor += res[1]
    last_time = sorted(us_dict)[-1].time()
    dist = round(step * one_step / 100000, 2)
    print(f'На {last_time} часов пройдено {dist} км ({step} шагов)\nизрасходовано {calor}  калорий !\n')
    return dist

def show_message_for_last_day():
    dist = show_my_results_till_now(day_dict)
    if dist > 25.5:
        print("Отличный результат! Цель достигнута.")
    elif dist > 16.9:
        print("Неплохо! День был продуктивным.")
    elif dist > 10:
        print("Маловато, но завтра наверстаем!")
    else:
        print("Лежать тоже полезно. Главное — участие, а не победа!")

form_new_data()

pprint(fitness_dairy)

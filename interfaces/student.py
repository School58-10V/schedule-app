import datetime


class StudentInterface:
    def __init__(self):
        pass

    def authorization(self):
        username, password = input('Ваш логин'), input('Ваш пароль')

    def schedule(self):
        pass

    def replacements(self):
        pass

    def holidays(self):
        choice = int(input('Введите: 1 для выбора нужного года; 2 для показа ближайших каникул; 0 для выхода из команды.\n'))
        while choice != 0:
            if choice == 1:
                year = int(input('Введите нужный год.\n'))
                if not self.__check_year(year):
                    while not self.__check_year(year):
                        year = int(input('Неверный ввод. Попробуйте ввести год снова.\n'))
                print(self.__get_holidays_for_year(year))
                break
            elif choice == 2:
                print(self.__get_near_holidays())
                break
            else:
                print('Неверный ввод. Попробуйте снова.\n')
                choice = int(input(
                    'Введите: 1 для выбора нужного года; 2 для показа ближайших каникул; 0 для выхода из команды.\n'))
        self.main_loop()
        pass

    def my_next_lesson(self):
        pass

    def get_class_teacher(self):
        pass

    def teacher_info(self):
        pass

    def __check_year(self, year):  # проверка на наличие timetable на год
        return True

    def __get_holidays_for_year(self, year):  # вывод NoLearningPeriod, связ. с таймтеблом
        return f'каникулы на {year} год'

    def __get_near_holidays(self):
        day = datetime.date.today()
        return f'следующие каникулы с {day}'


a = StudentInterface()
a.holidays()

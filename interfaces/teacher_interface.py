from __future__ import annotations
from typing import TYPE_CHECKING

from tabulate import tabulate

if TYPE_CHECKING:
    from adapters.db_source import DBSource


class TeacherInterface:
    __menu = tabulate([(1, "Посмотреть раписание"),
                       (2, "Узнать замену"),
                       (3, "Найти ученика"),
                       (4, "Посмотреть классы, которые я веду"),
                       (5, "Найти учителя"),
                       (6, "Посмотреть информацию о моем классе"),
                       (7, "Посмотреть информацию о каникулах"),
                       (8, "Мой следующий урок")], ['Опция', 'Команда'], tablefmt='grid')

    def __init__(self, db_source: DBSource, teacher_id: int):
        self.__db_source = db_source
        self.__teacher_id = teacher_id
        # Список, который хранит все методы для удобного вызова (его в общем, надо сюда)
        self.__lst = [self.__timetable, self.__replacement, self.__student_search, self.__my_classes,
                      self.__teacher_search, self.__my_class, self.__holidays,
                      self.__next_lesson]  # убрал дубль self.__timetable
        self.__days = {
            1: "понедельник",
            2: "вторник",
            3: "среда",
            4: "четверг",
            5: "пятница",
            6: "суббота",
            7: "воскресенье",
            0: "выход"
        }

    def __check_input(self, string: str, message: str = None) -> str:
        #  Метод, который проверяет, что ввод корректен (не пустой хотя бы)
        pass

    @staticmethod
    def clever_input(valid: list):
        # Проверяет, что пользователь ввел то, что нужно (правильные значения передаются в аргументах)
        valid.append('exit')
        user_input = input().lower().strip()
        while user_input not in valid:
            print(f"Неверный ввод! Варианты верного ввода: {valid}")
            user_input = input().lower().strip()
        return user_input

    # def __check_password(self, login: str, password: str) -> bool:
    #     # Метод, который проверяет, что пароль совпадает с паролем в базе
    #     pass не нужен, тк у нас нет авторизации здесь

    def run(self):
        # login = input().strip()
        # # login = self.__check_input(login, 'Введите логин') (Проверяем на правильность)
        # password = input().strip()
        # # password = self.__check_input(password, 'Введите пароль')
        # if self.__check_password(login, password) is False:
        #     return None
        flag = True
        while flag:
            flag = self.__show_menu()

    def __show_menu(self):
        print('Меню:', self.__menu, sep='\n')  # У кого хорошо с фантазией? Кто сможет это красиво оформить?
        flag = True
        n = 0
        while flag:
            string = input()
            try:
                num = int(string)  # Переводим
                # Вызываем функцию, название которой лежит в списке (да, так оно вызываеться!!!!)
                self.__lst[num - 1]()
                return True
            except (IndexError, ValueError):  # Если неправильный ввод, то либо увеличиваем счетчик
                if string == 'exit':  # Или другое слово, которое означает конец использования
                    print('Пока')
                    n = 3
                else:
                    n += 1
                    print('Введите еще раз')
            if n == 3:  # Пользователь ввел неправильные данные уже три раза!!! Забанить его!!!
                return False
        return True

    def __timetable(self):
        # Метод, который отвечает за расписание
        # print(0, 1)  # для теста, чтобы как-то обозначить
        print("Вы смотрите расписание.\n"
              "1 - на неделю\n"
              "2 - на конкретный день\n"
              "3 - на сегодня")
        self.__timetable_method_flag = self.clever_input(['3', '1', '2'])
        if self.__timetable_method_flag == '1':
            print("вы посмотрели расписание на неделю")
        elif self.__timetable_method_flag == '2':
            param = input('''на какой день вы хотите посмотреть расписание?
                    1 - понедельник
                    2 - вторник
                    3 - среда
                    4 - четверг
                    5 - пятница
                    6 - суббота
                    7 - воскресенье
                    0 - выход
                  ''')
            try:
                param = int(param)
            except ValueError:
                print("Попробуйте снова!")
            if 0 < param <= 7:
                print(f"вы посмотрели расписание на {self.__days[param]}")
            elif param == 0:
                print("выход")
        elif self.__timetable_method_flag == '3':
            print("расписаие на текущий день")
        elif self.__timetable_method_flag == 'exit':
            print("выход")

    def __student_search(self):
        print("""Поиск ученика
        1-где ученик сейчас
        2-расписание ученика""")
        self.__student_search_method_flag = self.clever_input(['2', '1'])
        if self.__student_search_method_flag == '1':
            print('кабинет в котором сейчас ученик:')
        elif self.__student_search_method_flag == '2':
            print('расписание ученика:')
        elif self.__student_search_method_flag == 'exit':
            print('Вы решили закончить просмотр, не начав')

    def __replacement(self):
        print("""
        Посмотреть замену:
        1 - На сегодня
        2 - На неделе
        (Выберите номер)
        """)
        # Метод, который отвечает за замены
        self.__replacement_method_flag = self.clever_input(['2', '1'])
        if self.__replacement_method_flag == '1':
            print("Вы посмотрели замена на сегодня")
            pass
        elif self.__replacement_method_flag == '2':
            print("Вы посмотрели замена на неделю")
            pass
        elif self.__replacement_method_flag == 'exit':
            print("Вы решили закончить просмотр, не начав")
            pass

    def __my_classes(self):
        print("""Просмотреть классы:
    1 - На сегодня
    2 - На неделю
    (Выберите вариант)""")
        self.__my_classes_method_flag = self.clever_input(['2', '1'])
        if self.__my_classes_method_flag == '2':
            print('классы сегодня')
        elif self.__my_classes_method_flag == '1':
            print('классы на неделю')
        elif self.__my_classes_method_flag == 'exit':
            print('Вы решили закончить просмотр, не начав')

    def __teacher_search(self):
        self.__teacher_search_method_flag = self.clever_input(['1'])
        if self.__teacher_search_method_flag == '1':
            pass
        elif self.__teacher_search_method_flag == 'exit':
            pass

    def __my_class(self):
        print("Смотрим информацию о вашем классе. Нажмите enter, чтобы продолжить")
        self.__my_class_method_flag = self.clever_input([''])  # тут пустой список передавать нельзя,
        # т.к будет бесконечный цикл, пока пользователь не введет exit. Надо будет передавать либо пустую
        # строку и пользователя просить нажать enter, или что-то еще придумать
        if self.__my_class_method_flag == 'exit':
            print("Вы вышли из просмотра информации о вашем классе")
            pass

    def __holidays(self):
        print("Посмотреть каникулы:"
              "1: Посмотреть ближайшие каникулы"
              "2: Посмотреть каникулы на определённый год")
        self.__holidays_method_flag = self.clever_input(['2', '1'])
        if self.__holidays_method_flag == '1':
            print("Вы посмотрели ближайшие каникулы")
        elif self.__holidays_method_flag == '2':
            print("Вы ввели год и посмотрели каникулы на этот год")
        elif self.__holidays_method_flag == 'exit':
            print("Вы вышли из каникул")

    def __next_lesson(self):
        print("Следующий урок. Нажмите enter, чтобы продолжить")
        self.__next_lesson_method_flag = self.clever_input([''])  # Та же ситуация
        if self.__next_lesson_method_flag == 'exit':
            print("Вы вышли из следующего урока")

# if __name__ == '__main__':
#    from adapters.db_source import DBSource
# db_source = DBSource(host='postgresql.aakapustin.ru', user='schedule_app',
#                     password='VYRL!9XEB3yXQs4aPz_Q', dbname='schedule_app')
# test_intf = TeacherInterface(db_source, 1)
# test_intf.run()

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from adapters.db_source import DBSource


class TeachersInterface:

    def __init__(self, db_source: DBSource):
        self.__db_source = db_source
        self.teacher_id = None
        # Список, который хранит все методы для удобного вызова (его в общем, надо сюда)
        self.lst = [self.__timetable, self.__replacement, self.__student_search, self.__my_classes,
                    self.__teacher_search, self.__my_class, self.__holidays,
                    self.__next_lesson]  # убрал дубль self.__timetable

    def __check_input(self, string: str, message: str = None) -> str:
        #  Метод, который проверяет, что ввод корректен (не пустой хотя бы)
        pass

    @staticmethod
    def clever_input(valid: list):
        # Проверяет, что пользователь ввел то, что нужно (правильные значения передаются в аргументах)
        valid.append('exit')
        user_input = input()
        while user_input not in valid:
            user_input = input()
        return user_input

    def __check_password(self, login: str, password: str) -> bool:
        # Метод, который проверяет, что пароль совпадает с паролем в базе
        pass

    def run(self):
        login = input().strip()
        # login = self.__check_input(login, 'Введите логин') (Проверяем на правильность)
        password = input().strip()
        # password = self.__check_input(password, 'Введите пароль')
        if self.__check_password(login, password) is False:
            return None
        flag = True
        while flag:
            flag = self.__show_menu()

    def __show_menu(self):
        print('Меню:')  # У кого хорошо с фантазией? Кто сможет это красиво оформить?
        flag = True
        n = 0
        while flag:
            string = input()
            try:
                num = int(string)  # Переводим
                # Вызываем функцию, название которой лежит в списке (да, так оно вызываеться!!!!)
                self.lst[num]()
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
        # print(0, 1) для теста, чтобы как-то обозначить
        self.__timetable_method_flag = self.clever_input(['0', '1', '2'])
        if self.__timetable_method_flag == '0':
            pass
        elif self.__timetable_method_flag == '1':
            pass
        elif self.__timetable_method_flag == '2':
            pass
        elif self.__timetable_method_flag == 'exit':
            pass

    def __student_search(self):
        # Метод, который отвечает за поиск студентов
        self.__student_search_method_flag = self.clever_input(['0', '1'])
        if self.__student_search_method_flag == '0':
            pass
        elif self.__student_search_method_flag == '1':
            pass
        elif self.__student_search_method_flag == 'exit':
            pass

    def __replacement(self):
        # print(2, 3)
        # Метод, который отвечает за замены
        self.__replacement_method_flag = self.clever_input(['0', '1'])
        if self.__replacement_method_flag == '0':
            pass
        elif self.__replacement_method_flag == '1':
            pass
        # Есть еще предложение обрабатывать это сразу в методе
        # clever_input и пусть он возвращает тогда то, что не обрабатывается в этих методах.
        # Тогда метод просто не будет ничего делать, а метод clever_input будет сам прощаться с пользователем
        elif self.__student_search_method_flag == 'exit':
            pass

    def __my_classes(self):
        self.__my_classes_method_flag = self.clever_input(['0', '1'])
        if self.__my_classes_method_flag == '0':
            pass
        elif self.__my_classes_method_flag == '1':
            pass
        elif self.__my_classes_method_flag == 'exit':
            pass

    def __teacher_search(self):
        self.__teacher_search_method_flag = self.clever_input(['0'])
        if self.__teacher_search_method_flag == '0':
            pass
        elif self.__teacher_search_method_flag == 'exit':
            pass

    def __my_class(self):
        self.__my_class_method_flag = self.clever_input([''])  # тут пустой список передавать нельзя,
        # т.к будет бесконечный цикл, пока пользователь не введет exit. Надо будет передавать либо пустую
        # строку и пользователя просить нажать enter, или что-то еще придумать
        if self.__my_class_method_flag == 'exit':
            pass

    def __holidays(self):
        self.__holidays_method_flag = self.clever_input(['0', '1'])
        if self.__holidays_method_flag == '0':
            pass
        elif self.__holidays_method_flag == '1':
            pass
        elif self.__holidays_method_flag == 'exit':
            pass

    def __next_lesson(self):
        self.__next_lesson_method_flag = self.clever_input([''])  # Та же ситуация
        if self.__next_lesson_method_flag == 'exit':
            pass

#
# if __name__ == '__main__':
#     from adapters.db_source import DBSource
#
#     db_source = DBSource(host='postgresql.aakapustin.ru', user='schedule_app',
#                          password='VYRL!9XEB3yXQs4aPz_Q', dbname='schedule_app')
#     test_intf = TeachersInterface(db_source)
#     test_intf.run()
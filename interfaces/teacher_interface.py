from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from adapters.db_source import DBSource


class TeachersInterface:

    def __init__(self, db_source: DBSource):
        self.__db_source = db_source
        self.teacher_id = None
        # Список, который хранит все методы для удобного вызова (его в общем, надо сюда)
        self.lst = [self.__timetable, self.__replacement, self.__timetable, self.__student_search, self.__my_classes]

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

    def __check_password(self) -> bool:
        # Метод, который проверяет, что пароль совпадает с паролем в базе
        pass

    def run(self):
        login = input().strip()
        # login = self.__check_input(login, 'Введите логин') (Проверяем на правильность)
        password = input().strip()
        # password = self.__check_input(password, 'Введите пароль')
        if self.__check_password() is False:
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
            except (IndexError, ValueError):  # Если неправильный ввод, то либо уыеличиваем счетчик
                if string == 'Все':  # Или другое слово, которое означает конец использования
                    print('Пока')
                    n = 3
                else:
                    n += 1
                    print('Введите еще раз')
            if n == 3:  # Пользователь ввел неправельные данные уже три раза!!! Забанить его!!!
                return False
        return True

    def __timetable(self):
        # Метод, который отвечает за расписание
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
        # Метод, который отвечает за замены
        self.__replacement_method_flag = self.clever_input(['0', '1'])
        if self.__replacemente_method_flag == '0':
            pass
        if self.__replacement_method_flag == '1':
            pass

    def __my_classes(self):
        self.__my_classes_method_flag = self.clever_input(['0', '1'])
        if self.__my_classes_method_flag == '0':
            pass
        elif self.__my_classes_method_flag == '1':
            pass
        elif self.__my_classes_method_flag == 'exit':
            pass
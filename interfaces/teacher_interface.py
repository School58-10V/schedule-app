from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from adapters.db_source import DBSource


class TeachersInterface:
    lst = []

    def __init__(self, db_source: DBSource):
        self.__db_source = db_source
        self.teacher_id = None

    def __check_input(self, string: str, message: str = None) -> str:
        pass

    def __check_password(self) -> bool:
        pass

    def run(self):
        login = input().strip()
        # login = self.__check_input(login, 'Введите логин')
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
            if n == 3:
                return False
        return True

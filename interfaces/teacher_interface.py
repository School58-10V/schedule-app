from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from adapters.db_source import DBSource


class TeachersInterface:
    def __init__(self, db_source: DBSource):
        self.__db_source = db_source

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

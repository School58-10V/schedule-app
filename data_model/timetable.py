from __future__ import annotations
import json
from typing import Optional, List


class TimeTable:
    def __init__(self, year: int = None, timetable_id: int = None):
        # Год - период времени
        self.__table_id = timetable_id
        self.__year = year

    def get_table_id(self) -> int:
        return self.__table_id

    def get_year(self) -> int:
        return self.__year

    def __str__(self):
        return f"Timetable(table_id={self.__table_id}, year={self.__year})"

    def __serialize_to_json(self):
        return json.dumps({"table_id": self.__table_id,
                           "year": self.__year}, ensure_ascii=False)

    def save(self, folder: str = 'tests/saves'):
        with open(f"../{folder}/TimeTable.json", mode="w", encoding='utf-8') as data_file:
            data_file.write(self.__serialize_to_json())

    @staticmethod
    def parse(file_timetable) -> List[(Optional[str], Optional[TimeTable])]:
        f = open(file_timetable, encoding='utf-8')
        lines = f.read().split('\n')
        lines = [i.split(';') for i in lines]
        res = []

        for elem in lines:
            try:
                year = int(elem[0])
                table_id = int(elem[1])
                res.append((None, TimeTable(year=year, timetable_id=table_id)))
            except IndexError as error:
                exception_text = f"Строка {lines.index(elem) + 2} не добавилась в [res]"
                print(exception_text, f'Ошибка {error}\n', sep='\n')
                res.append((exception_text, None))
            except TypeError as error:
                exception_text = f"Строка {lines.index(elem) + 2} не добавилась в [res]"
                print(exception_text, f'Ошибка {error}\n', sep='\n')
                res.append((exception_text, None))
            except Exception as error:
                exception_text = f"Неизвестная ошибка в TimeTable.parse():\n{error}"
                print(exception_text + '\n')
                res.append((exception_text, None))
        return res

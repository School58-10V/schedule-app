import json
from typing import Optional


class TeachersOnLessonRows:
    """
        Класс учителя в LessonRow. Используется для m2m отношения между
        Teacher и LessonRow
                      teacher_id - Идентификационный номер учителя
                   lesson_row_id - Идентификационный номер ряда уроков
        teacher_on_lesson_row_id - Идентификационный номер учителя на ряд уроков
    """

    def __init__(self, teacher_id: int, lesson_row_id: int, teacher_on_lesson_row_id: Optional[int] = None):
        self.__teacher_id = teacher_id
        self.__lesson_row_id = lesson_row_id
        self.__teacher_on_lesson_row_id = teacher_on_lesson_row_id

    def get_teacher_id(self) -> int:
        return self.__teacher_id

    def get_lesson_row_id(self) -> int:
        return self.__lesson_row_id

    def get_teacher_on_lesson_row_id(self) -> Optional[int]:
        return self.__teacher_on_lesson_row_id

    def __str__(self) -> str:
        return f'TeachersOnLessonRows(teacher_id: {self.__teacher_id},' \
               f' lesson_row_id: {self.__lesson_row_id},' \
               f' teacher_on_lesson_row_id: {self.__teacher_on_lesson_row_id})'

    def __serialize_to_json(self, records: list) -> str:
        # Добавляем новый объект в список
        records.append({"teacher_id": self.__teacher_id,
                        "lesson_row_id": self.__lesson_row_id,
                        "teacher_on_lesson_row_id": self.__teacher_on_lesson_row_id})

        return json.dumps(records, ensure_ascii=False, indent=4)

    def save(self, folder: str = 'db'):
        record = []
        try:
            # Проверка, существует ли файл и есть ли в нем запись
            data_file = open(f"../{folder}/teachers_on_lesson_rows.json", mode="r", encoding='utf-8')
            # Если да, то запоминаем и открываем файл на запись
            record = json.loads(data_file.read())
            data_file.close()
            data_file = open(f"../{folder}/teachers_on_lesson_rows.json", mode="w", encoding='utf-8')
        except FileNotFoundError:
            data_file = open(f"../{folder}/teachers_on_lesson_rows.json", mode="w", encoding='utf-8')
        except json.decoder.JSONDecodeError:
            data_file = open(f"../{folder}/teachers_on_lesson_rows.json", mode="w", encoding='utf-8')
            record = []
        # Записываем в файл новый список с добавленым объектом
        data_file.write(self.__serialize_to_json(record))
        data_file.close()

    @staticmethod
    def parse(file_location: str):
        file = open(file_location, 'r', encoding='utf-8')
        lines = file.read().split('\n')[1:]
        file.close()
        res = []
        for i in lines:
            j = i.split(';')
            try:
                teacher_id = int(j[0])
                lesson_row_id = int(j[1])
                teacher_on_lesson_row_id = int(j[2])

                res.append((None, TeachersOnLessonRows(teacher_id=teacher_id, lesson_row_id=lesson_row_id,
                                                       teacher_on_lesson_row_id=teacher_on_lesson_row_id)))
            except IndexError as error:
                exception_text = f"Строка {lines.index(i) + 2} не добавилась в [res]"
                print(exception_text, f'Ошибка {error}\n', sep='\n')
                res.append((exception_text, None))
            except TypeError as error:
                exception_text = f"Строка {lines.index(i) + 2} не добавилась в [res]"
                print(exception_text, f'Ошибка {error}\n', sep='\n')
                res.append((exception_text, None))
            except Exception as error:
                exception_text = f"Неизвестная ошибка в TeachersOnLessonRows.parse():\n{error}"
                print(exception_text + '\n')
                res.append((exception_text, None))
        return res

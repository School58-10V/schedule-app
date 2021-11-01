# start_time начало урока
# end_time конец урока
# day дата
# teacher_id замена
# lesson_id урок
# group_id группа учеников
# subject предмет
# state состояние
# notes примечания


class Lesson:
    def __init__(self, start_time: int, end_time: int, day: int, teacher_id: int, group_id: int,
                 subject_id: int, notes: str, lesson_id: int = None):
        self.__start_time = start_time
        self.__end_time = end_time
        self.__day = day
        self.__teacher_id = teacher_id
        self.__lesson_id = lesson_id
        self.__group_id = group_id
        self.__subject_id = subject_id
        self.__state = True
        self.__notes = notes

    def toggle_state(self):
        self.__state = not self.__state

    def get_start_time(self):
        return self.__start_time

    def get_end_time(self):
        return self.__end_time

    def get_day(self):
        return self.__day

    def get_teacher_id(self):
        return self.__teacher_id

    def get_lesson_id(self):
        return self.__lesson_id

    def get_group_id(self):
        return self.__group_id

    def get_subject(self):
        return self.__subject_id

    def get_state(self):
        return self.__state

    def get_notes(self):
        return self.__notes

    @staticmethod
    def parse(file_location) -> List[(Optional[str], Optional[Location])]:
        f = open(file_location, encoding='utf-8')
        lines = f.read().split('\n')[1:]
        lines = [i.split(';') for i in lines]
        res = []

        for i in lines:
            try:
                start_time = i[0]
                end_time = i[1]
                day = i[2]
                teacher_id = i[3]
                lesson_id = i[4]
                group_id = i[5]
                subject_id = i[6]
                notes = i[7]
                res.append((None, Lesson(start_time, end_time, day, teacher_id, group_id,
                                         subject_id, notes, lesson_id)))
            except IndexError as e:
                exception_text = f"Строка {lines.index(i) + 2} не добавилась в [res]"
                print(exception_text)
                print(e)
                res.append((exception_text, None))
            except Exception as e:
                exception_text = f"Неизвестная ошибка в Lesson.parse():\n{e}"
                print(exception_text)
                res.append((exception_text, None))

        return res

    def __str__(self):
        return f'Lesson(day = {self.__day}, start_time = {self.__start_time}, end_time = {self.__end_time}, notes =  {self.__notes}) '

    def __serialize_to_json(self):
        return json.dumps({"start_time": self.__start_time,
                           "end_time": self.__end_time,
                           "day": self.__day,
                           "teacher_id": self.__teacher_id,
                           "lesson_id": self.__lesson_id,
                           "group_id": self.__group_id,
                           "subject_id": self.__subject_id,
                           "state": self.__state,
                           "notes": self.__notes}, ensure_ascii=False)

    def save(self, file_way="./db/locations.json"):
        with open(file_way, mode="w", encoding='utf-8') as data_file:
            data_file.write(self.__serialize_to_json())

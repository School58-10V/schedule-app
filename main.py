class StudentInGroup:
    """
        Класс ученика в группе. Используется для m2m отношения между
        Group и Student
    """

    def __init__(self, student_id: int, group_id: int, student_group_id: int = None):
        self.__student_id = student_id
        self.__group_id = group_id
        self.__student_group_id = student_group_id

    def get_student_id(self):
        return self.__student_id

    def get_group_id(self):
        return self.__group_id

    def get_student_group_id(self):
        return self.__student_group_id

        @staticmethod
    def parse(file_location) -> List[(Optional[str], Optional[Location])]:
        f = open(file_location, encoding='utf-8')
        lines = f.read().split('\n')[1:]
        lines = [i.split(';') for i in lines]
        res = []

        for i in lines:
            try:
                student_id = i[0]
                group_id = i[1]
                student_group_id = i[2]
                res.append((None, StudentInGroup(student_id, group_id,student_group_id)))
            except IndexError as e:
                exception_text = f"Строка {lines.index(i) + 2} не добавилась в [res]"
                print(exception_text)
                print(e)
                res.append((exception_text, None))
            except Exception as e:
                exception_text = f"Неизвестная ошибка в Student_in_group.parse():\n{e}"
                print(exception_text)
                res.append((exception_text, None))

        return res

    def __str__(self):
        return f''

    def __serialize_to_json(self):
        return json.dumps({student_id:self.__student_id,
                group_id:self.__group_id
                student_group_id:self.__student_group_id}, ensure_ascii=False)

    def save(self, file_way="./db/locations.json"):
        with open(file_way, mode="w", encoding='utf-8') as data_file:
            data_file.write(self.__serialize_to_json())

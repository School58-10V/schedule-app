class Student:
    """
        Класс ученика.
    """

    def __init__(
            self, full_name: str, date_of_birth: str, student_id: int = None,
            contacts: str = None, bio: str = None
    ):
        self.__full_name = full_name
        self.__date_of_birth = date_of_birth
        self.__student_id = student_id
        self.__contacts = contacts
        self.__bio = bio

    def get_full_name(self):
        return self.__full_name

    def get_date_of_birth(self):
        return self.__date_of_birth

    def get_id(self):
        return self.__student_id

    def get_contacts(self):
        return self.__contacts

    def get_bio(self):
        return self.__bio

    @staticmethod
    def parse(file_location) -> List[(Optional[str], Optional[Location])]:
        f = open(file_location, encoding='utf-8')
        lines = f.read().split('\n')[1:]
        lines = [i.split(';') for i in lines]
        res = []

        for i in lines:
            try:
                full_name = i[0]
                date_of_birth = i[1]
                student_id = i[2]
                contacts = i[3]
                bio = i[4]

                res.append(
                    (None, Lesson(full_name, date_of_birth, student_id, contacts, bio)))
            except IndexError as e:
                exception_text = f"Строка {lines.index(i) + 2} не добавилась в [res]"
                print(exception_text)
                print(e)
                res.append((exception_text, None))
            except Exception as e:
                exception_text = f"Неизвестная ошибка в Student.parse():\n{e}"
                print(exception_text)
                res.append((exception_text, None))

        return res

    def __str__(self):
        return f'Student(full_name = {self.__full_name}, date_of_birth = {self.__date_of_birth}, contacts = {self.__contacts}, bio =  {self.__bio}) '

    def __serialize_to_json(self):
        return json.dumps({"full_name": self.__full_name,
                           "date_of_birth": self.__date_of_birth,
                           "student_id": self.__student_id,
                           "contacts": self.__contacts,
                           "bio": self.__bio}, ensure_ascii=False)

    def save(self, file_way="./db/student.json"):
        with open(file_way, mode="w", encoding='utf-8') as data_file:
            data_file.write(self.__serialize_to_json())

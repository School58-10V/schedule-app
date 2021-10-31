import json


class Subject:
    """
              name - Название предмета
        subject_id - Идентификационный номер предмета

    """
    def __init__(self, name: str = None, subject_id: int = None):
        self.__subject_name = name
        self.__subject_id = subject_id

    def get_subject_id(self) -> int:
        return self.__subject_id

    def get_subject_name(self) -> str:
        return self.__subject_name

    @staticmethod
    def parse(file_location: str):
        file = open(file_location, 'r', encoding='utf-8')
        lines = file.read().split('\n')[1:]
        file.close()
        # lines = [i.split(';') for i in lines] Зачем отдельно проходить циклом для split,
        # если можно сделать все в одном цикле?
        res = []
        for i in lines:
            j = i.split(';')
            try:
                name_subject = j[0]
                # Будет ли в файле csv id предмета?
                subject_id = int(j[1])
                res.append((None, Subject(name=name_subject, subject_id=subject_id)))
            except IndexError as error:
                exception_text = f"Строка {lines.index(i) + 2} не добавилась в [res]"
                print(exception_text, f'Ошибка {error}\n', sep='\n')
                res.append((exception_text, None))
            except TypeError as error:
                exception_text = f"Строка {lines.index(i) + 2} не добавилась в [res]"
                print(exception_text, f'Ошибка {error}\n', sep='\n')
                res.append((exception_text, None))
            except Exception as error:
                exception_text = f"Неизвестная ошибка в Subject.parse():\n{error}"
                print(exception_text + '\n')
                res.append((exception_text, None))
        return res

    def __str__(self):
        return f'Subject(subject_name={self.__subject_name})'

    def __serialize_to_json(self, records: list) -> str:
        # Добавляем новый объект в список
        records.append({"subject_id": self.__subject_id,
                        "subject_name": self.__subject_name})

        return json.dumps(records, ensure_ascii=False, indent=4)

    def save(self, folder: str = 'db'):
        record = []
        try:
            # Проверка, существует ли файл и есть ли в нем запись
            data_file = open(f"../{folder}/subject.json", mode="r", encoding='utf-8')
            # Если да, то запоминаем и открываем файл на запись
            record = json.loads(data_file.read())
            data_file.close()
            data_file = open(f"../{folder}/subject.json", mode="w", encoding='utf-8')
        except FileNotFoundError:
            data_file = open(f"../{folder}/subject.json", mode="w", encoding='utf-8')
        except json.decoder.JSONDecodeError:
            data_file = open(f"../{folder}/subject.json", mode="w", encoding='utf-8')
            record = []
        # Записываем в файл новый список с добавленым объектом
        data_file.write(self.__serialize_to_json(record))
        data_file.close()

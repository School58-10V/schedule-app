# group - 01
# lesson - 02
# lesson_row - 03
# location - 04
# no_learning_period - 05
# student - 06
# student_in_group - 07
# subject_lesson - 08
# teacher - 09
# teachers_on_lesson_rows - 10
# timetable - 11
import json


@staticmethod
def serialize_records_to_json(records: list, indent: int = None) -> str:
    return json.dumps(records, ensure_ascii=False, indent=indent)


def insert(self, collection_name: str, document: dict) -> dict:
    # читает файл, изменяет айди, записывает новый файл с доп объектом
    with open(f"./db/{collection_name}.json", mode="w", encoding='utf-8') as data_file:
        current_records = self.__read_json_db(collection_name)
        document["_object_id"] = int(id_class + len(f"./db/{collection_name}.json"))
        current_records.append(document)
        target_json = self.__class__.serialize_records_to_json(current_records)
        data_file.write(target_json)


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



def insert(self, collection_name: str, document: dict) -> dict:
    current_records = self.__read_json_db(collection_name)
    document["_object_id"] = int(id_class + len(f"./db/{collection_name}.json"))
    current_records.append(self.__dict__())
    target_json = self.__class__.serialize_records_to_json(current_records)



    @staticmethod
    def serialize_records_to_json(records: list, indent: int = None) -> str:
        return json.dumps(records, ensure_ascii=False, indent=indent)

    @classmethod
    def __read_json_db(cls, db_path) -> list:
        try:
            with open(f"{db_path}/{cls.__name__}.json",
                      mode="r", encoding='utf-8') as data_file:
                record = json.loads(data_file.read())
                return record
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            return []

    def save(self, output_path: str = './db'):
        current_records = self.__read_json_db(output_path)
        current_records.append(self.__dict__())
        target_json = self.__class__.serialize_records_to_json(current_records)
        with open(f"{output_path}/{type(self).__name__}.json", mode="w", encoding='utf-8') as data_file:
            data_file.write(target_json)

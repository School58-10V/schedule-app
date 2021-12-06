from data_model.student import Student
from adapters.file_source import FileSource

data = FileSource('../db')
student = Student.get_by_id(1061638802407770, data)
print(student.get_all_groups())

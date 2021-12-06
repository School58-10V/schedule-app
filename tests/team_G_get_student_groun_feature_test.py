from data_model.student import Student
from adapters.file_source import FileSource

data = FileSource('../db')
student = Student(db_source=data, full_name='', date_of_birth=6)
student.save()
print(student.get_all_student_group())

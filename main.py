from data_model.teacher import Teacher
from data_model.student import Student
from data_model.student_in_group import StudentInGroup

# учитель:
res = Teacher.parse("test_file.csv")
print(*res)
# не выдает ошибки, хотя поле с номером пропущено (на след раз почему-то выдал надо проверить 0_0)
teacher1 = Teacher('Иван Петрович', 3, 227, None, None)
teacher1.save()

res = Student.parse('test_file2.csv')
print(*res)
student1 = Student('Name Surname', '01.02.12', 3, None, None)
student1.save()

res = StudentInGroup.parse('test_file3.csv')
print(*res)
student_in_group1 = StudentInGroup(1, 101, 3)
student_in_group1.save()
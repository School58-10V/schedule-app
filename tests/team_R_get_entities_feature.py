from data_model.teacher import Teacher
from data_model.student import Student
from data_model.student_in_group import StudentInGroup


res = Teacher.get_all("../data_examples/teacher.json")
print(res)
for i in res:
    print(i)
res_id = Teacher.get_by_id(123, "../data_examples/teacher.json")
print(res_id)

print("----------")

res = Student.get_all("../data_examples/student.json")
print(res)
for i in res:
    print(i)
res_id = Student.get_by_id(678, "../data_examples/student.json")
print(res_id)

print("----------")

res = StudentInGroup.get_all("../data_examples/student_in_group.json")
print(res)
for i in res:
    print(i)
res_id = StudentInGroup.get_by_id(345, "../data_examples/student_in_group.json")
print(res_id)

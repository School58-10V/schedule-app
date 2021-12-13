from data_model.teacher import Teacher
from data_model.student import Student
from data_model.students_for_groups import StudentsForGroups


res = Teacher.get_all("../data_examples")
print(res)
for i in res:
    print(i)
res_id = Teacher.get_by_id(123, "../data_examples")
print(res_id)

print("----------")

res = Student.get_all("../data_examples")
print(res)
for i in res:
    print(i)
res_id = Student.get_by_id(678, "../data_examples")
print(res_id)

print("----------")

res = StudentsForGroups.get_all("../data_examples")
print(res)
for i in res:
    print(i)
res_id = StudentsForGroups.get_by_id(345, "../data_examples")
print(res_id)

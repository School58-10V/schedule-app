from data_model.teacher import Teacher


res = Teacher.get_all("../data_examples/teacher.json")
print(res)
for i in res:
    print(i)
res_id = Teacher.get_by_id(123, "../data_examples/teacher.json")
print(res_id)

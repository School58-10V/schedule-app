from data_model.Teacher import Teacher

res = Teacher.parse("test_file.csv")
print(*res)
# не выдает ошибки, хотя поле с номером пропущено
teacher1 = Teacher('Иван Петрович', 3, 227, None, None)
teacher1.save()
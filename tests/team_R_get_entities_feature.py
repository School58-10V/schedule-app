from data_model.teacher import Teacher


# учитель:
res = Teacher.get_all("./data_examples/test_file.csv")
res = Teacher.get_by_id("./data_examples/test_file.csv", 123)
print(*res)
# не выдает ошибки, хотя поле с номером пропущено (на след раз почему-то выдал надо проверить 0_0)
teacher1 = Teacher('Иван Петрович', 3, 227, None, None)
teacher1.save()

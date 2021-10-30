from data_model.subject_lesson import Subject


subject1 = Subject('Art', 1)
subject1.save()

subject2 = Subject()
subjects = subject2.parse('../data_examples/subject_test.csv')
print(subject2)
subject2.save()

subject3 = subjects[0][1]
print(subject3)
subject3.save()

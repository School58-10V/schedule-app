import datetime

from adapters.db_source import DBSource

a = DBSource(user='schedule_app', password='VYRL!9XEB3yXQs4aPz_Q', host='postgresql.aakapustin.ru')

# тесты для функций-геттеров в DBSource
# не будет
student_list = a.get_all('Students')
print(student_list)
s1 = a.get_by_id('Students', student_list[0]['object_id'])
print(s1)
s2 = a.get_by_query('Students', {'object_id': student_list[0]['object_id'], 'full_name': 'Хромов Михаил Романович', 'date_of_birth': datetime.date(2005, 2, 22), 'bio': 'тот чел который тот самый да'})
print(s2)
assert s1 == s2[0]

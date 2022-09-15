from db_source import DBSource
from tests.test_class_team_Raviolli import TestClass

db_source = DBSource(host="postgresql.aakapustin.ru",
                     password="VYRL!9XEB3yXQs4aPz_Q",
                     user="schedule_app",
                     options="-c search_path=dbo,public")
test_class = TestClass(db_source=db_source)
lst = test_class.run(lst=[2, 2, 4], class_letter='Raviolli', grade=11)
for i in sorted(list(lst.keys())):
    print(i)
    print(*lst[i], sep='\n')
    print()

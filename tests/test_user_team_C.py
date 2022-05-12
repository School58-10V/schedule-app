from data_model.user import User
from services.db_source_factory import DBFactory

db_source = DBFactory(options="-c search_path=dbo,auth")
new_user = User(db_source=db_source.get_db_source(), login='login3', name='name2',
                password='1qwerty_password')
print(new_user.get_password_hash())
print(new_user.compare_hash('1qwerty_password'))
print(new_user.compare_hash('false_password'))
new_user.save()
new_user1 = User.get_by_login(login='login3', db_source=db_source.get_db_source())
print(new_user1.__dict__())
print(User.get_all(db_source=db_source.get_db_source()))
new_user1.delete()
print(new_user1)


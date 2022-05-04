from data_model.user import User
from services.db_source_factory import DBFactory

db_source = DBFactory(options="-c search_path=dbo,auth")
new_user = User(db_source=db_source.get_db_source(), login='login2', name='name2',
                hash_password='1qwerty_password')
print(new_user.get_password_hash())
new_user.password_to_hash()
print(new_user.get_password_hash())
print(new_user.compare_hash('password'))
print(new_user.compare_hash('false_password'))
new_user.save()
new_user1 = User.get_by_login(login='login1', db_source=db_source.get_db_source())
print(new_user1.__dict__())
print(User.get_all(db_source=db_source.get_db_source()))

from data_model.user import User
from services.db_source_factory import DBFactory

db_source = DBFactory()
new_user = User(db_source=db_source.get_db_source(), login='login', name='name', password_hash='password')
print(new_user.get_password_hash())
new_user.password_to_hash()
print(new_user.get_password_hash())
print(new_user.compare_hash('password'))
print(new_user.compare_hash('false_password'))

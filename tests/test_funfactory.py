from tests.funfactory import Funfactory
factory = Funfactory
factory.create_group()
for i in range(3):
    factory.create_lesson_row()
class Teacher:
    def __init__(self, fio, teacher_id, bio, contacts, office_id, lesson):
        self.__fio = fio
        self.__teacher_id = teacher_id
        self.__bio = bio
        self.__contacts = contacts
        self.__office_id = office_id
        self.__lesson = lesson

# fio - ФИО, что впринципе логично
# teacher_id - ид учителя
# bio - инфа о учителе
# contacts - Контакты учителя
# office_id - закреплённый кабинет
# lesson - сделайте m2m связь, т.к. не знаю, не умею

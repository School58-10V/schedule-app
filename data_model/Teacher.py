# fio - ФИО, что впринципе логично
# teacher_id - ид учителя
# bio - инфа о учителе
# contacts - Контакты учителя
# office_id - закреплённый кабинет
# lesson - сделайте m2m связь, т.к. не знаю, не умею

class Teacher:
    def __init__(self, fio: str, teacher_id: int, subject: str, office_id: str = None, bio: str = None,
                 contacts: str = None):
        self.__fio = fio
        self.__teacher_id = teacher_id
        self.__bio = bio
        self.__contacts = contacts
        self.__office_id = office_id
        self.__subject = subject

    def get_fio(self):
        return self.__fio

    def get_teacher_id(self):
        return self.__teacher_id

    def get_bio(self):
        return self.__bio

    def get_contacts(self):
        return self.__contacts

    def get_subject(self):
        return self.__subject

    def get_office_id(self):
        return self.__office_id

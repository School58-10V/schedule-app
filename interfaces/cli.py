class Interfaces:
    def __init__(self):
        self.tip = ""
        self.fio = ""

    def info(self):
        print("Ввидите данные")
        self.tip = input("Ваш вид дейтельности (учитель/ученик/администратор)")
        while self.tip != "учитель" and self.tip != "ученик" and self.tip != "администратор":
            self.tip = input("такого типа нет, выберите 'учитель' или 'ученик' или 'администратор'")
        self.fio = input("ФИО")

    def show_menu(self):
        print("Выберите подходяшие вам действие:")
        if self.tip == "учитель":
            action = input("1) рассписание (уроки и групы на этих уроках)\n2) замены\n3)добавить новый предмет")
        elif self.tip == "администратор":
            action = input("1) добавить учителя \n2) добавить ученика\n3) добавить замены\n")

        else:
            action = input("1) рассписание (уроки и групы на этих уроках)\n2) все учителя\n")


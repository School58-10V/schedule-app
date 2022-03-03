def replacements(self):
    v_replacements = input("Выбирите опцию: 1. Замена на сегоднишний день 2. Выбирите замену по предмету, дате, преподователю")
    while True:
        if v_replacements in ["1", "2"]:
            break
        else:
            print("Неверная опция.")
            v_replacements = input("Выбирите опцию: 1. Замена на сегоднишний день 2. Выбирите замену по предмету, дате, преподователю")
    if v_replacements == "1":
        print(f"Замены на сегодня{self.__today_replacements()}")
    elif v_replacements == "2":
        lesson = input("Выбирите предмет, для которого ищется замена (Если этот пораметр вас не интересует запишите '-'):")
        while True:
            if __chek_lesson(lesson):
                break
            else:
                print("Неверный предмет.")
                lesson = input(
                    "Выбирите предмет, для которого ищется замена (Если этот пораметр вас не интересует запишите '-'):")
        teacher = input(
            "Выбирите учителя, для которого ищется замена (Если этот пораметр вас не интересует запишите '-'):")
        while True:
            if __chek_teacher(teacher):
                break
            else:
                print("Неверный учитель.")
                teacher = input(
                    "Выбирите учителя, для которого ищется замена (Если этот пораметр вас не интересует запишите '-'):")
        day = input(
            "Выбирите день, для которого ищется замена (Если этот пораметр вас не интересует запишите '-'):")
        while True:
            if __chek_day(day):
                break
            else:
                print("Неверный день.")
                day = input(
                    "Выбирите день, для которого ищется замена (Если этот пораметр вас не интересует запишите '-'):")
        print(f"Замены на {day}: {self.__day_replacements(lesson, teacher, day)}")


def __today_replacements(self):
    return "замены на сегоднешний день"


def __day_replacements(self, lesson, teacher, day):
    return "замены на конкретный день"


def __chek_lesson(self, lesson):
    pass


def __chek_teacher(self, teacher):
    pass


def __chek_day(self, day):
    pass

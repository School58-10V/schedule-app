class StudentInterface:
    def __init__(self):
        pass

    def authorization(self):
        username, password = input('Ваш логин'), input('Ваш пароль')

    def schedule(self):
        option = int(input('''
Напишите 1 - чтобы посмотреть расписание на сегодня
Напишите 2 - чтобы посмотреть расписание на неделю
Напишите 3 - чтобы посмотреть расписание на какой-либо день '''))
        while option != 1 and option != 2 and option != 3:
            option = int(input('Введите коректное число'))

        if option == 1:
            return self.__get_schedule_for_today()
        elif option == 2:
            return self.__get_schedule_for_week()
        elif option == 3:
            day = int(input('''
Напишите день на котороый хотите посмотреть расписание
Понедельник - 1
Вторник - 2
 т.д.'''))
            self.__get_schedule_for_day(day)

    def replacements(self):
        pass

    def free_days(self):
        pass

    def my_next_lesson(self):
        pass

    def get_class_teacher(self):
        pass

    def teacher_info(self):
        pass

    def __get_schedule_for_today(self):
        day = 1
        return f'расписание на {day}'

    def __get_schedule_for_week(self):
        return f'расписание на неделю'

    def __get_schedule_for_day(self, day):
        return f'расписание на выбранный день'


StudentInterface.schedule()




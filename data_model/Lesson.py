class Lesson:
    def __init__(self):
        self.time =
        self.day =
        self.teacher_id =
        self.lesson_id =
        self.group_for_lesson_id =
        self.subject =
        self.hometask =  # not necessary?
        self.state = True
        self.notes =

    def change_state(self):
        self.state = not self.state
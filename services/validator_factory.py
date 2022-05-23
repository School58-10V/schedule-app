from validators.abstract_validator import AbstractValidator
from validators.group_validator import GroupValidator
from validators.lesson_row_validator import LessonRowValidator
from validators.lesson_validator import LessonValidator
from validators.location_validator import LocationValidator
from validators.no_learning_period_validator import NoLearningPeriodValidator
from validators.student_validator import StudentValidator
from validators.subject_validator import SubjectValidator
from validators.teacher_validator import TeacherValidator
from validators.timetable_validator import TimeTableValidator


class ValFactory:
    def __init__(self):
        self.validators: list[AbstractValidator] = []
        self.validators.append(GroupValidator())
        self.validators.append(LessonValidator())
        self.validators.append(LessonRowValidator())
        self.validators.append(LocationValidator())
        self.validators.append(NoLearningPeriodValidator())
        self.validators.append(StudentValidator())
        self.validators.append(SubjectValidator())
        self.validators.append(TeacherValidator())
        self.validators.append(TimeTableValidator())

    def get_appropriate_validator(self, name):
        name = name.replace("_controller", "Validator")
        name.capitalize()
        for validator in self.validators:
            if validator.get_name() == name:
                return
        raise ValueError("Неверный тип валидатора")



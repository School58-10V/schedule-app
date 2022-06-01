from validators.abstract_validator import AbstractValidator
from validators.group_validator import GroupValidator
from validators.lesson_row_validator import LessonRowValidator
from validators.lesson_validator import LessonValidator
from validators.location_validator import LocationValidator
from validators.no_learning_period_validator import NoLearningPeriodValidator
from validators.student_validator import StudentValidator
from validators.subject_validator import SubjectValidator
from validators.teacher_validator import TeacherValidator
from validators.timetable_validator import TimetableValidator


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
        self.validators.append(TimetableValidator())

    @classmethod
    def snake_case_2_camel_case(cls, snake_case_text: str):
        """ converts camel_case_name to CamelCaseName """
        return ''.join([i.capitalize() for i in snake_case_text.split('_')])

    def get_appropriate_validator(self, name):
        file_name = name.split('.')[-1]
        camel_case_name = self.snake_case_2_camel_case(file_name)
        camel_case_name = camel_case_name.replace("Controller", "Validator")
        # name.capitalize()

        for validator in self.validators:
            if validator.get_name() == camel_case_name:
                return validator
        raise ValueError("Неверный тип валидатора")

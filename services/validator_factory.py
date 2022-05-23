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
        self.validators: list[str] = []
        self.validators.append(GroupValidator.get_name())
        self.validators.append(LessonValidator.get_name())
        self.validators.append(LessonRowValidator.get_name())
        self.validators.append(LocationValidator.get_name())
        self.validators.append(NoLearningPeriodValidator.get_name())
        self.validators.append(StudentValidator.get_name())
        self.validators.append(SubjectValidator.get_name())
        self.validators.append(TeacherValidator.get_name())
        self.validators.append(TimeTableValidator.get_name())

    def get_appropriate_validator(self, name):
        for validator_name in self.validators:
            if validator_name == name:
                return validator_name
        raise ValueError("Неверный тип валидатора")



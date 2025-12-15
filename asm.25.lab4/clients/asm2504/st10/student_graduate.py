from .student_master import StudentMaster

class StudentGraduate(StudentMaster):
    TYPE_NAME = "Аспирант"
    fields = StudentMaster.fields.copy()
    fields.update({
        "diploma_topic": "Тема кандидатской диссертации",
        "research_direction": "Направление исследований"
    })

from .student_bachelor import StudentBachelor

class StudentMaster(StudentBachelor):
    TYPE_NAME = "Магистр"
    fields = StudentBachelor.fields.copy()
    fields.update({
        "diploma_topic": "Тема магистерской диссертации",
        "publications": "Научные публикации",
        "internship": "Стажировка"
    })

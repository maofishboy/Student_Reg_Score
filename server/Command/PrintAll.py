from DBController.StudentInfoTable import StudentInfoTable
from DBController.SubjectInfoTable import SubjectInfoTable

class PrintAll:
    def __init__(self):
        self.student_info_table = StudentInfoTable()
        self.subject_info_table = SubjectInfoTable()

    def execute(self, parameters):
        all_students = self.student_info_table.select_all_students()
        students_with_subjects = {}

        for student in all_students:
            stu_id = student['stu_id']
            name = student['name']
            subjects = self.subject_info_table.select_subjects_by_student_id(stu_id)
            students_with_subjects[name] = {
                'name': name,
                'scores': {subject['subject']: subject['score'] for subject in subjects}
            }

        if not students_with_subjects:
            return {'status': 'OK', 'parameters': {}}
        else:
            return {'status': 'OK', 'parameters': students_with_subjects}

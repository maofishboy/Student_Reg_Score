from DBController.StudentInfoTable import StudentInfoTable
from DBController.SubjectInfoTable import SubjectInfoTable

class AddStu:
    def __init__(self):
        # 初始化数据库操作类
        self.student_info_table = StudentInfoTable()
        self.subject_info_table = SubjectInfoTable()

    def execute(self, parameters):
        name = parameters.get('name')
        scores = parameters.get('scores', {})

        # 首先检查学生是否已存在
        existing_students = self.student_info_table.select_a_student(name)
        if not existing_students:
            # 添加学生到数据库
            self.student_info_table.insert_a_student(name)

            # 获取刚添加的学生的ID
            student_id = self.student_info_table.select_a_student(name)[0]

            # 为学生添加每门科目的成绩
            for subject, score in scores.items():
                self.subject_info_table.insert_a_subject(student_id, subject, score)

            return {'status': 'OK'}
        return {'status': 'Fail', 'reason': 'The student already exists.'}

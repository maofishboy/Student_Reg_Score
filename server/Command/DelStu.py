from DBController.StudentInfoTable import StudentInfoTable
from DBController.SubjectInfoTable import SubjectInfoTable

class DelStu:
    def __init__(self):
        # 初始化数据库操作类
        self.student_info_table = StudentInfoTable()
        self.subject_info_table = SubjectInfoTable()

    def execute(self, parameters):
        name = parameters.get('name')
        # 首先根据名字查找学生ID
        student_ids = self.student_info_table.select_a_student(name)
        if not student_ids:
            return {'status': 'Fail', 'reason': 'The name is not found.'}

        # 删除学生的所有科目
        for stu_id in student_ids:
            # 查找该学生的所有科目
            subject_records = self.subject_info_table.select_subjects_by_student_id(stu_id)
            for subject_record in subject_records:
                subject = subject_record['subject']
                self.subject_info_table.delete_a_subject(stu_id, subject)
        
        # 删除学生信息
        for stu_id in student_ids:
            self.student_info_table.delete_a_student(stu_id)

        print(f"  Del {name} success")
        return {'status': 'OK'}

    
from DBController.StudentInfoTable import StudentInfoTable
from DBController.SubjectInfoTable import SubjectInfoTable

class ModifyStu:
    def __init__(self):
        # 初始化数据库操作类
        self.student_info_table = StudentInfoTable()
        self.subject_info_table = SubjectInfoTable()

    def execute(self, parameters):
        name = parameters.get('name')
        scores = parameters.get('scores', {})

        # 首先检查学生是否存在
        student_ids = self.student_info_table.select_a_student(name)
        if not student_ids:
            return {'status': 'Fail', 'reason': 'The name is not found.'}

        # 学生存在，获取学生 ID
        student_id = student_ids[0]

        # 更新或添加新的科目成绩
        for subject_name, score in scores.items():
            subject_records = self.subject_info_table.select_a_subject(subject_name)
            if any(record[1] == student_id for record in subject_records):
                # 更新现有科目的成绩
                subject_id = [record[0] for record in subject_records if record[1] == student_id][0]
                self.subject_info_table.update_a_subject_score(student_id, subject_id, score)
            else:
                # 插入新科目的成绩
                self.subject_info_table.insert_a_subject(student_id, subject_name, score)
        
        print(f"  Modify {name} success")
        return {'status': 'OK'}
        
        
       
  
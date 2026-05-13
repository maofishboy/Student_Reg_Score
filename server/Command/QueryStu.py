from DBController.StudentInfoTable import StudentInfoTable
from DBController.SubjectInfoTable import SubjectInfoTable

class QueryStu:
    def __init__(self):
        self.student_info_table = StudentInfoTable()
        self.subject_info_table = SubjectInfoTable()

    def execute(self, parameters):
        name = parameters.get('name')
        student_ids = self.student_info_table.select_a_student(name)
        
        if not student_ids:
            # 如果没有找到学生，返回未找到的状态
            result = {'status': 'Fail', 'reason': 'The name is not found.'}
            return result
        
        # 学生存在，接下来查询该学生的所有科目信息
        scores = {}
        for stu_id in student_ids:
            subjects = self.subject_info_table.select_subjects_by_student_id(stu_id)
            for subject in subjects:
                scores[subject['subject']] = subject['score']
        
        print(f"  Query {name} success")
        result = {'status': 'OK', 'scores': scores}
        return result

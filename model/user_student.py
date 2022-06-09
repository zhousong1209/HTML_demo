from model.user import User
from lib.helper import course_data_path, user_data_path, course_json_files_path, figure_save_path

class Student(User):
    def __init__(self, uid=-1, username="", password="", register_time="yyyy-MM-dd_HH:mm:ss", role="", email = ""):
        # initialize the parameters
        self.uid=uid
        self.username=username
        self.password=password
        self.register_time=register_time
        self.role=role
        self.email = email

    def __str__(self):
        #return '675531;;;test;;;**t****e****s****t**;;;2022-1-24_12:47:18.244;;;student;;;test@gmail.com;;;;;;;;;'
        return ';;;'.join([str(self.uid), self.username, self.encrypt_password(self.password), self.date_conversion(self.register_time), self.role, self.email])
    @classmethod
    def get_students_by_page(cls, page):
        # get students by page
        record_user = []
        with open(user_data_path, 'r') as f:
            m = f.read()
            m_list = m.split('\n')
            for course in m_list:
                if len(course.split(';;;'))==6:
                    uid,username,password,register_time,role,email = course.split(';;;')
                    tmp = Student(uid,username,password,register_time,role,email)
                    record_user.append(tmp)
            total_page = (len(record_user))//20+1
            total_num_users = len(record_user)
            if (page-1)*20+1<=total_num_users:
                return_course_max = min(total_num_users, page*20)
                record_user = record_user[(page-1)*20:return_course_max]
        return (record_user, total_page, total_num_users)
    @classmethod
    def get_student_by_id(cls, id):# original no id here
        # get student by id
        with open(user_data_path,'r') as f:
            for m in f.readlines():
                if len(m.split(';;;'))==6:
                    uid,username,password,register_time,role,email = m.split(';;;')
                    if id==int(uid):
                        tmp = Student(uid,username,password,register_time,role,email)
                        return tmp
        
    @classmethod
    def delete_student_by_id(cls, id):# original no id here
        # delete student by id
        delete_success=0
        transit = []
        # delete from user.txt
        with open(user_data_path,'r') as f:
            for m in f.readlines():
                if len(m.split(';;;'))==6:
                    uid,username,password,register_time,role,email = m.split(';;;')
                    if int(uid)==id:
                        delete_success=1
                        continue
                transit.append(m)
        with open(user_data_path, 'w') as f:
            for m in transit:
                f.write(m+'\n')
        
        if delete_success==0:
            return False
        else:
            return True
if __name__ == '__main__':
    a = Student()
    print(a.get_students_by_page(1))
    print(a.get_student_by_id(523938))
    print(a.delete_student_by_id(523938))
    print(a.get_student_by_id(523938))
    
    

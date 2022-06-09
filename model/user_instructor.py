from model.user import User
import numpy as np
from lib.helper import course_data_path, user_data_path, course_json_files_path, figure_save_path
import os
import matplotlib.pyplot as plt
import json

class Instructor(User):
    def __init__(self, uid=-1, username="", password="", register_time="yyyy-MM-dd_HH:mm:ss", role="",email = "",display_name = "",job_title="",course_id_list=[]):
        # initialize the parameters
        self.uid=uid
        self.username=username
        self.password=password
        self.register_time=register_time
        self.role=role
        self.email = email
        self.display_name = display_name
        self.job_title=job_title
        self.course_id_list=course_id_list

    def __str__(self):
        #return '945546;;;test;;;&&15&&&&25&&&&35&&&&45&&&&55&&&&65&&&&75&&&&85&&;;;2022-5-3_11:39:11.731;;;instructor;;;12312312@gmail.com;;;;;;;;;'
        return ';;;'.join([str(self.uid), self.username, self.encrypt_password(self.password), self.date_conversion(self.register_time), self.role, self.email])
    @classmethod
    def get_instructors(cls):
        # get user data from course
        # write user data from user.txt
        
        
        # write instructors info into user.txt
        path = os.getcwd()+course_json_files_path
        record_user = {}
        for dir in os.listdir(path):# for each category
            tmp_course_word = dir[11:]# category name
            for dirs in os.listdir(path+'/'+dir+'/'):
                for dirss in os.listdir(path+'/'+dir+'/'+dirs):# for each json file
                    with open(path+'/'+dir+'/'+dirs+'/'+dirss, 'r') as f:
                        read_json = json.loads(f.read())
                        subcategory_id = read_json['unitinfo']['source_objects'][0]['id']
                        subcategory_title = read_json['unitinfo']['source_objects'][0]['title']
                        subcategory_description = read_json['unitinfo']['source_objects'][0]['description']
                        subcategory_url = read_json['unitinfo']['source_objects'][0]['url']
                        for k in range(len(read_json['unitinfo']['items'])):# for each class
                            course_id = read_json['unitinfo']['items'][k]['id']
                            for i in range(len(read_json['unitinfo']['items'][k]['visible_instructors'])):
                                user_id = read_json['unitinfo']['items'][k]['visible_instructors'][i]['id']
                                username = read_json['unitinfo']['items'][k]['visible_instructors'][i]['display_name'].replace(' ', '_').lower()
                                display_name = read_json['unitinfo']['items'][k]['visible_instructors'][i]['display_name']
                                job_title = read_json['unitinfo']['items'][k]['visible_instructors'][i]['job_title']
                                register_time = cls.register_time
                                password = str(user_id)
                                email = username+'@gmail.com'
                                try: # if user already in record_user dict
                                    record_user[user_id]
                                    record_user[user_id][-1]=record_user[str(user_id)][-1]+'-'+course_id
                                except:# else record the info into hte record_user dict
                                    if job_title==None:
                                        job_title = 'None'
                                    record_user[user_id] = [str(user_id), username, cls.encrypt_password(password), register_time, 'instructor', email, display_name, job_title, str(course_id)]
        # process the users to combine their course_id_list
        with open(user_data_path, 'r') as f:
            m = f.read()
            m_list = m.split('\n')
            transit = []# record the original user in user.txt, including instructor and student
            for course in m_list:
                if len(course.split(';;;'))==9:
                    uid,username,password,register_time,role,email,display_name,job_title,course_id_list = course.split(';;;')
                    if course_id_list=='':
                        course_id_list = []
                    else:
                        course_id_list = course_id_list.split('-')
                    try:# if the user already in user.txt
                        record_user[uid]
                        course_id_list=np.unique(course_id_list.extend(record_user[id][-1])).tolist()
                        transit.append(';;;'.join([uid,username,password,register_time,role,email,display_name,job_title,course_id_list]))
                        del record_user[uid]
                    except:
                        pass
                transit.append(course)
        with open(user_data_path, 'w') as f:
            for m in transit:
                f.write(m+'\n')
            for val in record_user.values():
                f.write(';;;'.join(val)+'\n')
        
    @classmethod
    def get_instructors_by_page(cls, page):
        # get instructors by page
        record_user = []
        with open(user_data_path, 'r') as f:
            m = f.read()
            m_list = m.split('\n')
            for course in m_list:
                if len(course.split(';;;'))==9:
                    uid,username,password,register_time,role,email,display_name,job_title,course_id_list = course.split(';;;')
                    tmp = Instructor(uid,username,password,register_time,role,email)
                    record_user.append(tmp)
            total_page = (len(record_user))//20+1
            total_num_users = len(record_user)
            if (page-1)*20+1<=total_num_users:
                return_course_max = min(total_num_users, page*20)
                record_user = record_user[(page-1)*20:return_course_max]
        return (record_user, total_page, total_num_users)
    @classmethod
    def generate_instructor_figure1(cls):
        # draw a figure to show the first 10 instructors with the most number of courses
        record_user = {}
        with open(user_data_path, 'r') as f:
            m = f.read()
            m_list = m.split('\n')
            for course in m_list:
                if len(course.split(';;;'))==9:
                    uid,username,password,register_time,role,email,display_name,job_title,course_id_list = course.split(';;;')
                    record_user[username] = len(course_id_list.split('--'))
        new_sys2 = sorted(record_user.items(),  key=lambda d: d[1], reverse=True)
        first_10 = [i[0] for i in new_sys2[:10]]
        processed_first_10 = []
        for name in first_10:
            name_list = name.split('_')
            processed_first_10.append(' '.join(name_list[:min(3,len(name_list))]))
        
        
        num_of_categories = len(new_sys2)
        
        plt.figure()
        plt.barh(processed_first_10, [i[1] for i in new_sys2[:10]])
        plt.show()
        return 'draw a figure to show the first 10 instructors with the most number of courses'
if __name__ == '__main__':
    a = Instructor()
    #print(a.get_instructors())
    #print(a.get_instructors_by_page(1))
    #print(a.generate_instructor_figure1())

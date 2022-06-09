import os
import json
import numpy as np
import matplotlib.pyplot as plt
from lib.helper import course_data_path, user_data_path, course_json_files_path, figure_save_path

class Course:

    def __init__(self, category_title = "", subcategory_id =-1, subcategory_title="", subcategory_description="", subcategory_url="", course_id=-1, course_title="", course_url="", num_of_subscribers =0, avg_rating=0.0, num_of_reviews=0):
        # initialize the parameters
        self.category_title = category_title
        self.subcategory_id =subcategory_id
        self.subcategory_title=subcategory_title
        self.subcategory_description=subcategory_description
        self.subcategory_url=subcategory_url
        self.course_id=course_id
        self.course_title=course_title
        self.course_url=course_url
        self.num_of_subscribers =num_of_subscribers
        self.avg_rating=avg_rating
        self.num_of_reviews=num_of_reviews

    def __str__(self):
        #return "{category_title,subcategory_id,subcategory_title,subcategory_url,course_id,course_title,course_url,num_of_subscribers,avg_rating,num_of_reviews}"
        #return 'Development;;;8;;;Web Development;;;Learn web development skills to build fully functioning websites.;;;/courses/development/web-development/;;;1565838;;;The Complete 2021 Web Developemnt Bootcamp;;;/course/the-complete-web-development-bootcamp/;;;474825;;;4.675107;;;150052'
        return ';;;'.join([self.category_title, str(self.subcategory_id), self.subcategory_title, self.subcategory_description, self.subcategory_url, str(self.course_id), self.course_title, self.course_url, str(self.num_of_subscribers), str(self.avg_rating), str(self.num_of_reviewsnum_of_reviews)])
    @classmethod
    def get_courses(cls):
        # get courses info from source_course files
        # write courses info into course.txt
        path = os.getcwd()+course_json_files_path
        record_course = []
        with open(course_data_path, 'w') as f1:
            for dir in os.listdir(path):# for each category
                tmp_course_word = dir[11:]# category name
                if tmp_course_word ==cls.category_title:
                    for dirs in os.listdir(path+'/'+dir):
                        for dirss in os.listdir(path+'/'+dir+'/'+dirs):
                            with open(path+'/'+dir+'/'+dirs+'/'+dirss, 'r') as f:
                                read_json = json.loads(f.read())
                                subcategory_id = read_json['unitinfo']['source_objects'][0]['id']
                                subcategory_title = read_json['unitinfo']['source_objects'][0]['title']
                                subcategory_description = read_json['unitinfo']['source_objects'][0]['description']
                                subcategory_url = read_json['unitinfo']['source_objects'][0]['url']
                                for k in range(len(read_json['unitinfo']['items'])):
                                    course_id = read_json['unitinfo']['items'][k]['id']
                                    course_title = read_json['unitinfo']['items'][k]['title']
                                    course_url = read_json['unitinfo']['items'][k]['url']
                                    num_of_subscribers = read_json['unitinfo']['items'][k]['num_subscribers']
                                    avg_rating = read_json['unitinfo']['items'][k]['avg_rating']
                                    num_of_reviews = read_json['unitinfo']['items'][k]['num_reviews']
                                    
                                    
                                    record_str = [str(cls.category_title),str(subcategory_id),str(subcategory_title),str(subcategory_description),str(subcategory_url),str(course_id),str(course_title),str(course_url),str(num_of_subscribers),str(avg_rating),str(num_of_reviews)]
                                    f1.write(';;;'.join(record_str)+'\n')
        
                
        
    @classmethod
    def clear_course_data(cls):
        # clean the data in course.txt
        with open(course_data_path,'w') as f:
            f.close()
    @classmethod
    def generate_page_num_list(cls, page, total_pages):
        # return the visualized pages
        if page<=5:
            return [i+1 for i in range(9)]
        elif page<total_pages-4:
            return [page-4+i for i in range(9)]
        else:
            return [total_pages-8+i for i in range(9)]
    @classmethod
    def get_courses_by_page(cls, page):
        # get courses by page
        with open(course_data_path, 'r') as f:
            m = f.read()
            m_list = m.split('\n')
            total_page = (len(m_list))//20+1
            total_num_courses = len(m_list)
            if (page-1)*20+1<=total_num_courses:
                return_course_max = min(total_num_courses, page*20)
                record_course = []
                for course in m_list[(page-1)*20:return_course_max]:
                    print(course)
                    category_title,subcategory_id,subcategory_title,subcategory_description,subcategory_url,course_id,course_title,course_url,num_of_subscribers,avg_rating,num_of_reviews = course.split(';;;')
                    tmp = Course(category_title,subcategory_id,subcategory_title,subcategory_description,subcategory_url,course_id,course_title,course_url,num_of_subscribers,avg_rating,num_of_reviews)
                    record_course.append(tmp)
        return (record_course, total_page, total_num_courses)
                
            
    @classmethod
    def delete_course_by_id(cls, temp_course_id):
        # delete course by course_id
        delete_success=0
        transit = []
        # delete from course.txt
        with open(course_data_path,'r') as f:
            for m in f.readlines():
                category_title,subcategory_id,subcategory_title,subcategory_description,subcategory_url,course_id,course_title,course_url,num_of_subscribers,avg_rating,num_of_reviews = m.split(';;;')
                if int(course_id)==temp_course_id:
                    delete_success=1
                    continue
                transit.append(m)
        with open(course_data_path, 'w') as f:
            for m in transit:
                f.write(m)
        # delete from user.txt
        transit_teacher = []
        with open(user_data_path,'r') as f:
            for m in f.readlines():
                if len(m.split(';;;'))==9:
                    instructor_id,username,password,register_time,role,email, instructor_display_name,instructor_job_title,course_id_list = m.split(';;;')
                    course_id_list_list = course_id_list.split('--')
                    if str(temp_course_id).isin(course_id_list_list):
                        course_id_list_list.remove(str(temp_course_id))
                        course_id_list='--'.join(course_id_list_list)
                    transit_teacher.append(';;;'.join([instructor_id,username,password,register_time,role,email, instructor_display_name,instructor_job_title,course_id_list]))
        with open(user_data_path, 'w') as f:
            for m in transit_teacher:
                f.write(m)
        if delete_success==0:
            return False
        else:
            return True
        
    @classmethod
    def get_course_by_course_id(cls, temp_course_id):
        # get course by course_id
        with open(course_data_path,'r') as f:
            for m in f.readlines():
                category_title,subcategory_id,subcategory_title,subcategory_description,subcategory_url,course_id,course_title,course_url,num_of_subscribers,avg_rating,num_of_reviews = m.split(';;;')
                if int(course_id)==temp_course_id:
                    a = Course()
                    a.category_title =category_title
                    a.subcategory_id = int(subcategory_id)
                    a.subcategory_title = subcategory_title
                    a.subcategory_description = subcategory_description
                    a.subcategory_url = subcategory_url
                    a.course_id = int(course_id)
                    a.course_title = course_title
                    a.course_url = course_url
                    a.num_of_subscribers = int(num_of_subscribers)
                    a.avg_rating = np.float(avg_rating)
                    a.num_of_reviews = np.int(num_of_reviews)
                    if a.num_of_reviews>100000 and a.avg_rating>4.5 and a.num_of_reviews>10000:
                        comments = 'Top Course'
                    elif a.num_of_reviews>50000 and a.avg_rating>4.0 and a.num_of_reviews>5000:
                        comments = 'Popular Course'
                    elif a.num_of_reviews>10000 and a.avg_rating>3.5 and a.num_of_reviews>1000:
                        comments = 'Good Course'
                    else:
                        comments = 'General Course'
                    return (a, comments)
        
        return False
    @classmethod
    def get_course_by_instructor_id(cls, instructor_id):
        # get course by instructor id
        course_id_record = []
        with open(user_data_path,'r') as f:
            for m in f.readlines():
                user_instructor_id,username,password,register_time,role,email, instructor_display_name,instructor_job_title,course_id_list = m.split(';;;')
                if instructor_id==int(user_instructor_id) and role=='instructor':
                    course_id_record =course_id_list.split('--')
                    course_id_record = [int(i) for i in course_id_record]
        return_num_course = min(len(course_id_record),20)
        course_id_record = course_id_record[:return_num_course]
        record_course = []
        with open(course_data_path,'r') as f:
            for m in f.readlines():
                category_title,subcategory_id,subcategory_title,subcategory_description,subcategory_url,course_id,course_title,course_url,num_of_subscribers,avg_rating,num_of_reviews = m.split(';;;')
                if course_id in course_id_record:
                    tmp = Course(category_title,subcategory_id,subcategory_title,subcategory_description,subcategory_url,course_id,course_title,course_url,num_of_subscribers,avg_rating,num_of_reviews)
                    record_course.append(tmp)
        return record_course, return_num_course
    @classmethod
    def generate_course_figure1(cls):
        # 10 sub-category which has most number of subscribers
        path = os.getcwd()+course_json_files_path
        record_course = {}
        for dir in os.listdir(path):
            category_title = dir[11:]
            for dirs in os.listdir(path+'/'+dir+'/'):
                subcategory = dirs[2:]
                record_course[subcategory]=0
                for files in os.listdir(path+'/'+dir+'/'+dirs+'/'):
                    with open(path+'/'+dir+'/'+dirs+'/'+files, 'r') as f:
                        read_json = json.loads(f.read())
                        subcategory_id = read_json['unitinfo']['source_objects'][0]['id']
                        subcategory_title = read_json['unitinfo']['source_objects'][0]['title']
                        subcategory_description = read_json['unitinfo']['source_objects'][0]['description']
                        subcategory_url = read_json['unitinfo']['source_objects'][0]['url']
                        for k in range(len(read_json['unitinfo']['items'])):
                            course_id = read_json['unitinfo']['items'][k]['id']
                            course_title = read_json['unitinfo']['items'][k]['title']
                            course_url = read_json['unitinfo']['items'][k]['url']
                            num_of_subscribers = read_json['unitinfo']['items'][k]['num_subscribers']
                            avg_rating = read_json['unitinfo']['items'][k]['avg_rating']
                            num_of_reviews = read_json['unitinfo']['items'][k]['num_reviews']
                            
                            record_course[subcategory]+=int(num_of_subscribers)
        new_sys2 = sorted(record_course.items(),  key=lambda d: d[1], reverse=True)
        first_10_subcategory = [i[0] for i in new_sys2[:10]]
        plt.figure()
        plt.bar(first_10_subcategory, [i[1] for i in new_sys2[:10]])
        plt.xticks(rotation=45)
        plt.show()
        return '10 sub-category which has most number of subscribers'
    @classmethod
    def generate_course_figure2(cls):
        # first 10 courses which has number of comments more than 50000
        path = os.getcwd()+course_json_files_path
        record_course = {}
        for dir in os.listdir(path):
            category_title = dir[11:]
            for dirs in os.listdir(path+'/'+dir+'/'):
                subcategory = dirs[2:]
                for files in os.listdir(path+'/'+dir+'/'+dirs+'/'):
                    with open(path+'/'+dir+'/'+dirs+'/'+'/'+files, 'r') as f:
                        read_json = json.loads(f.read())
                        subcategory_id = read_json['unitinfo']['source_objects'][0]['id']
                        subcategory_title = read_json['unitinfo']['source_objects'][0]['title']
                        subcategory_description = read_json['unitinfo']['source_objects'][0]['description']
                        subcategory_url = read_json['unitinfo']['source_objects'][0]['url']
                        for k in range(len(read_json['unitinfo']['items'])):
                            course_id = read_json['unitinfo']['items'][k]['id']
                            course_title = read_json['unitinfo']['items'][k]['title']
                            course_url = read_json['unitinfo']['items'][k]['url']
                            num_of_subscribers = read_json['unitinfo']['items'][k]['num_subscribers']
                            avg_rating = read_json['unitinfo']['items'][k]['avg_rating']
                            num_of_reviews = read_json['unitinfo']['items'][k]['num_reviews']
                            
                            record_course[course_title]=int(num_of_reviews)
        new_sys2 = sorted(record_course.items(),  key=lambda d: d[1], reverse=True)
        first_10_courses = [i[0] for i in new_sys2[:10]]
        plt.figure()
        plt.bar(first_10_courses, [i[1] for i in new_sys2[:10]])
        plt.xticks(rotation=45)
        plt.show()
        return 'first 10 courses which has number of comments more than 50000'
    @classmethod
    def generate_course_figure3(cls):
        # scatter plot of courses which has avg score between 10000 and 100000
        path = os.getcwd()+course_json_files_path
        record_course = {}
        for dir in os.listdir(path):
            category_title = dir[11:]
            for dirs in os.listdir(path+'/'+dir+'/'):
                subcategory = dirs[2:]
                for files in os.listdir(path+'/'+dir+'/'+dirs+'/'):
                    with open(path+'/'+dir+'/'+dirs+'/'+files, 'r') as f:
                        read_json = json.loads(f.read())
                        subcategory_id = read_json['unitinfo']['source_objects'][0]['id']
                        subcategory_title = read_json['unitinfo']['source_objects'][0]['title']
                        subcategory_description = read_json['unitinfo']['source_objects'][0]['description']
                        subcategory_url = read_json['unitinfo']['source_objects'][0]['url']
                        for k in range(len(read_json['unitinfo']['items'])):
                            course_id = read_json['unitinfo']['items'][k]['id']
                            course_title = read_json['unitinfo']['items'][k]['title']
                            course_url = read_json['unitinfo']['items'][k]['url']
                            num_of_subscribers = read_json['unitinfo']['items'][k]['num_subscribers']
                            avg_rating = read_json['unitinfo']['items'][k]['avg_rating']
                            num_of_reviews = read_json['unitinfo']['items'][k]['num_reviews']
                            
                            if int(num_of_reviews)>=10000 and int(num_of_reviews)<=100000:
                                record_course[course_title]=int(avg_rating)
        new_sys2 = sorted(record_course.items(),  key=lambda d: d[1], reverse=True)
        first_10_courses = [i[0] for i in new_sys2]
        plt.figure()
        plt.scatter(first_10_courses, [i[1] for i in new_sys2])
        plt.xticks(rotation=45)
        plt.show()
        return 'scatter plot of courses which has avg score between 10000 and 100000'
    @classmethod
    def generate_course_figure4(cls):
        # draw pie plot to show the number of courses of all categories (not subcategories)
        path = os.getcwd()+course_json_files_path
        record_course = {}
        for dir in os.listdir(path):
            category_title = dir[11:]
            record_course[category_title] = 0
            for dirs in os.listdir(path+'/'+dir+'/'):
                subcategory = dirs[2:]
                for files in os.listdir(path+'/'+dir+'/'+dirs+'/'):
                    with open(path+'/'+dir+'/'+dirs+'/'+files, 'r') as f:
                        read_json = json.loads(f.read())
                        subcategory_id = read_json['unitinfo']['source_objects'][0]['id']
                        subcategory_title = read_json['unitinfo']['source_objects'][0]['title']
                        subcategory_description = read_json['unitinfo']['source_objects'][0]['description']
                        subcategory_url = read_json['unitinfo']['source_objects'][0]['url']
                        for k in range(len(read_json['unitinfo']['items'])):
                            course_id = read_json['unitinfo']['items'][k]['id']
                            course_title = read_json['unitinfo']['items'][k]['title']
                            course_url = read_json['unitinfo']['items'][k]['url']
                            num_of_subscribers = read_json['unitinfo']['items'][k]['num_subscribers']
                            avg_rating = read_json['unitinfo']['items'][k]['avg_rating']
                            num_of_reviews = read_json['unitinfo']['items'][k]['num_reviews']
                            
                            record_course[category_title]+=1
        new_sys2 = sorted(record_course.items(),  key=lambda d: d[1], reverse=False)
        first_10_courses = [i[0] for i in new_sys2]
        
        num_of_categories = len(new_sys2)
        color = ["blue","red","coral","green","yellow","orange"]
        colors = color[:num_of_categories]
        
        plt.figure()
        explode_value = [0 for i in range(len(new_sys2))]
        explode_value[-2] = 0.1
        plt.pie([i[1] for i in new_sys2], explode=explode_value, colors=colors, labels=first_10_courses, shadow=True)
        plt.show()
        return 'draw pie plot to show the number of courses of all categories (not subcategories)'
    @classmethod
    def generate_course_figure5(cls):
        # draw barh plot to show the distribution of courses which has comments
        path = os.getcwd()+course_json_files_path
        record_course = {}
        record_course['has_c']=0
        record_course['no_c']=0
        for dir in os.listdir(path):
            category_title = dir[11:]
            for dirs in os.listdir(path+'/'+dir+'/'):
                subcategory = dirs[2:]
                for files in os.listdir(path+'/'+dir+'/'+dirs+'/'):
                    with open(path+'/'+dir+'/'+dirs+'/'+files, 'r') as f:
                        read_json = json.loads(f.read())
                        subcategory_id = read_json['unitinfo']['source_objects'][0]['id']
                        subcategory_title = read_json['unitinfo']['source_objects'][0]['title']
                        subcategory_description = read_json['unitinfo']['source_objects'][0]['description']
                        subcategory_url = read_json['unitinfo']['source_objects'][0]['url']
                        for k in range(len(read_json['unitinfo']['items'])):
                            course_id = read_json['unitinfo']['items'][k]['id']
                            course_title = read_json['unitinfo']['items'][k]['title']
                            course_url = read_json['unitinfo']['items'][k]['url']
                            num_of_subscribers = read_json['unitinfo']['items'][k]['num_subscribers']
                            avg_rating = read_json['unitinfo']['items'][k]['avg_rating']
                            num_of_reviews = read_json['unitinfo']['items'][k]['num_reviews']
                            
                            if int(num_of_reviews)>0:
                                record_course['has_c']+=1
                            else:
                                record_course['no_c']+=1
        new_sys2 = sorted(record_course.items(),  key=lambda d: d[1], reverse=True)
        first_10_courses = [i[0] for i in new_sys2]
        plt.figure()
        plt.barh(first_10_courses, [i[1] for i in new_sys2])
        plt.show()
        return 'draw barh plot to show the distribution of courses which has comments'
    @classmethod
    def generate_course_figure6(cls):
        # draw a chart to show the first 10 sub-categories which has the least number of courses
        path = os.getcwd()+course_json_files_path
        record_course = {}
        for dir in os.listdir(path):
            category_title = dir[11:]
            for dirs in os.listdir(path+'/'+dir+'/'):
                subcategory = dirs[2:]
                record_course[subcategory]=0
                for files in os.listdir(path+'/'+dir+'/'+dirs+'/'):
                    with open(path+'/'+dir+'/'+dirs+'/'+files, 'r') as f:
                        read_json = json.loads(f.read())
                        subcategory_id = read_json['unitinfo']['source_objects'][0]['id']
                        subcategory_title = read_json['unitinfo']['source_objects'][0]['title']
                        subcategory_description = read_json['unitinfo']['source_objects'][0]['description']
                        subcategory_url = read_json['unitinfo']['source_objects'][0]['url']
                        for k in range(len(read_json['unitinfo']['items'])):
                            course_id = read_json['unitinfo']['items'][k]['id']
                            course_title = read_json['unitinfo']['items'][k]['title']
                            course_url = read_json['unitinfo']['items'][k]['url']
                            num_of_subscribers = read_json['unitinfo']['items'][k]['num_subscribers']
                            avg_rating = read_json['unitinfo']['items'][k]['avg_rating']
                            num_of_reviews = read_json['unitinfo']['items'][k]['num_reviews']
                            
                            record_course[subcategory]+=1
        new_sys2 = sorted(record_course.items(),  key=lambda d: d[1], reverse=False)
        first_10_courses = [i[0] for i in new_sys2[:10]]
        processed_first_10_courses = []
        for name in first_10_courses:
            name_list = name.split('-')
            try:
                name_list.remove('')
            except:
                pass
            processed_first_10_courses.append(' '.join(name_list[:min(3,len(name_list))]))
        
        
        num_of_categories = len(new_sys2)
        
        plt.figure()
        plt.barh(processed_first_10_courses, [i[1] for i in new_sys2[:10]])
        plt.show()
        return 'draw a chart to show the first 10 sub-categories which has the least number of courses'
if __name__ == '__main__':
    a = Course(category_title='Business')
    print(a.get_courses())
    print(a.get_courses_by_page(1))
    print(a.delete_course_by_id(495303923))
    print(a.get_course_by_course_id(263886449))
    print(a.get_course_by_instructor_id(23445566))
    print(a.generate_course_figure6())
    

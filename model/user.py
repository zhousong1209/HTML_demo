import os
from lib.helper import get_day_from_timestamp
import re
from lib.helper import course_data_path, user_data_path, course_json_files_path, figure_save_path
import numpy as np

class User:
    current_login_user = None #[admin\instructor\student]
    def __init__(self, uid=-1, username="", password="", register_time="yyyy-MM-dd_HH:mm:ss", role=""):
        # initialize the parameters
        self.uid=uid
        self.username=username
        self.password=password
        self.register_time=register_time
        self.role=role # only be [Admin”、“Instructor”、“Student”]

    def __str__(self):
        #return "uid;;;username;;;password;;;register_time;;;role"
        return ';;;'.join([str(self.uid), self.username, self.encrypt_password(self.password), self.date_conversion(self.register_time), self.role])
    @classmethod
    def validate_username(cls, username):
        # determine whether the username contains only characters and '_'
        if username=='':
            return False
        split_u = list(username)
        for a in split_u:
            if ord(a) < ord('A') or (ord(a)>ord('Z') and ord(a)<ord('_')) or (ord(a)>ord('_') and ord(a)<ord('a')) or ord(a)>ord('z'):
                return False
        return True
    @classmethod
    def validate_password(cls, password):
        # determine whether the length of password equals or larger than 8
        if len(list(password))>=8:
            return True
        return False
    @classmethod
    def validate_email(cls, email):
        # use re to judge whether email address is valid
        
        ret = re.search(".com$", email)
        ret2 = re.search("@", email)
        if ret and ret2 and len(email)>8:
            return True
        else:
            return False
    @classmethod
    def clear_user_data(cls):
        # clean the data in user.txt
        with open(user_data_path,'w') as f:
            f.close()
    @classmethod
    def authenticate_user(cls, username, password):
        # open txt files and check whether username and password exists in the file
        with open(user_data_path,'r') as f:
            for m in f.readlines():
                id, user, pasw = m.split(';;;')[:3]
                if user==username and cls.encrypt_password(password)==pasw:
                    return m.strip('\n')
        
        return None
    @classmethod
    def check_username_exist(cls, username):
        # open txt files and check whether username exists in the file
        with open(user_data_path,'r') as f:
            for m in f.readlines():
                id, user, pasw = m.split(';;;')[:3]
                if user==username:
                    return True
        
        return False
    @classmethod
    def generate_unique_user_id(cls):
        # generate and return an id which is not in user.txt
        with open(user_data_path,'r') as f:
            id_list = []
            for m in f.readlines():
                id, user, pasw = m.split(';;;')[:3]
                id_list.append(id)
        
        id = np.random.randint(100000,999999)
        count_index=0
        while str(id) in id_list and count_index<10000:
            id = np.random.randint(100000,999999)
            count_index+=1
        if count_index<10000:
            return id
        else:
            raise Error
    @classmethod
    def encrypt_password(cls, password):
        # With given password, encrypt the password with '***'
        split_passw = list(password)
        enc_value  = '****'.join(['a']+split_passw+['a'])
        return enc_value[3:-3]
    @classmethod
    def register_user(cls, username, password, email, register_time, role):
        if cls.check_username_exist(username):# if user name exists in user.txt, return False
            return False
        new_id = cls.generate_unique_user_id()# if not, register one for the user and return True
        print(register_time)
        time = register_time
        encrypt_pasw =cls.encrypt_password(password)
        record = [str(new_id), username, encrypt_pasw, time, role, email]
        record_txt = ';;;'.join(record)
        with open(user_data_path,'a') as f:# write the user information into user.txt
            f.write(record_txt+'\n')
        return True
    @classmethod
    def date_conversion(cls, register_time):
        # convert epoch to datetime
        # 时间应该是格林尼治时间+11墨尔本时区。
        hs = register_time%1000
        register_time = register_time//1000
        year = register_time//31556926
        register_time = register_time-31556926*year
        year = 1970+year
        month = register_time//2629743
        register_time = register_time-2629743*month
        date = get_day_from_timestamp(register_time)
        #date = register_time//86400
        register_time = register_time-86400*date
        if register_time<0:
            register_time=register_time+86400
        hour = register_time//3600
        register_time = register_time-3600*hour
        min = register_time//60
        register_time = register_time-60*min
        sec = register_time
        return str(year)+'-'+str(month)+'-'+str(date)+'_'+str(hour)+':'+str(min)+':'+str(sec)+'.'+str(hs)


if __name__ == '__main__':
    a = User()
    print(a.date_conversion(1637549590753))
    print('------check email------')
    print(a.validate_email('wwwfdsa@gmail.com'))
    print(a.validate_email('w@1.com'))
    print('------check username-------')
    print(a.validate_username('a!*'))
    print(a.validate_username('a_fdsA'))
    print('------check password--------')
    print(a.validate_password('abcdefg'))
    print(a.validate_password('abcdefghd'))
    print('------')
    print(a.authenticate_user('aaaaa', 'aaaaa'))
    print(a.register_user('aaaaaa', 'aaaaaaaaaaa111', 'cccc@gmail.com', 1637549590753, 'student'))
    

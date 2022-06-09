from model.user import User
from lib.helper import course_data_path, user_data_path, course_json_files_path, figure_save_path
import numpy as np

class Admin(User):
    def __init__(self, uid=-1, username="", password="", register_time="yyyy-MM-dd_HH:mm:ss", role=""):
        # initialize the parameters
        self.uid=uid
        self.username=username
        self.password=password
        self.register_time=register_time
        self.role=role

    def register_admin(self):
        new_admin = User()# initialize an instance User()
        #new_admin.current_login_user = self.role
        #new_admin.username=self.username
        #new_admin.password=self.password
        #new_admin.register_time=self.register_time
        #new_admin.role=self.role
        
        username = 'Admin02'
        email = username+'@gmail.com'############ Need to confirm ##########
        new_admin.register_user(username, '123456789', email,1637549590753, 'admin')# use the register_user function in User()

    def __str__(self):
        # return an example
        #return '285108;;;aaaaa;;;**a****a****a****a****a**;;;2021-11-29_32:32:28.590;;;admin'
        return ';;;'.join([str(self.uid), self.username, self.encrypt_password(self.password), self.date_conversion(self.register_time), self.role])
if __name__ == '__main__':
    a = Admin()
    a.register_admin()


from flask import render_template, Blueprint

from model.user import User
from model.user_admin import Admin


index_page = Blueprint("index_page", __name__)

@index_page.route("/")# GET request
def index():
    # check the class variable User.current_login_user
    current_user_role=''
    if User.current_login_user!=None:
        current_user_role = User.current_login_user.role
    # manually register an admin account when open index page
    ad_acc = Admin(123456, 'admin', '12345678', register_time = '2022-05-26_12:24:33.507', role='admin')
    ad_acc.register_user('admin', '12345678', 'xxx@mail.com','2022-05-26_12:24:33.507', 'admin')

    print(current_user_role)
    return render_template('01index.html',current_user_role=current_user_role)
    

if __name__ == '__main__':
    index()

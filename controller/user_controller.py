
from flask import Blueprint, render_template, request, redirect, url_for
from lib.helper import render_result, render_err_result, course_data_path, user_data_path
from model.course import Course
from model.user import User
from model.user_admin import Admin
from model.user_instructor import Instructor
from model.user_student import Student

user_page = Blueprint("user_page", __name__)

model_user = User()
model_course = Course()
model_student = Student()


def generate_user(login_user_str):
    #login_user = None # a User object
    
    if len(login_user_str.split(';;;'))<5:
        return
    word_list = login_user_str.split(";;;")
    User.current_login_user = None
    if "admin" in word_list:
        User.current_login_user = Admin(int(word_list[0]), word_list[1], word_list[2], word_list[3], word_list[4])
    elif "student" in word_list:
        print(int(word_list[0]), word_list[1], word_list[2], word_list[3], word_list[4], word_list[5])
        User.current_login_user = Student(int(word_list[0]), word_list[1], word_list[2], word_list[3], word_list[4], word_list[5])
    elif "instructor" in word_list:
        User.current_login_user = Instructor(int(word_list[0]), word_list[1], word_list[2], word_list[3], word_list[4], word_list[5],word_list[6],word_list[7], word_list[8].strip("\n").split("--"))
    
    #return login_user



# use @user_page.route("") for each page url
@user_page.route("/login", methods=["GET"])
def login():
    return render_template("00login.html")

@user_page.route("/login", methods=["POST"])
def login_post():
    req = request.values
    username = req["username"] if "username" in req else ""
    password = req["password"] if "password" in req else ""
    a = model_user.validate_username(username)
    b = model_user.validate_password(password)
    if a and b:
        c = model_user.authenticate_user(username, password)
        print(c)
        if c:
            generate_user(c)
            #return render_template("11student_info.html")
            
            return render_result(msg="login success")#########
        else:
            return render_err_result(msg="login failure")
    else:
        return render_err_result(msg="login failure")
    #return redirect(url_for("user_page.student_info"))
    #return render_template("11student_info.html")
    
    
# 4. templates/00login.html页面在这里创建两个输入框，供用户输入用户名和密码。用户名输入的类型为文本，密码输入的类型为密码。在学生代码注释区域内编写您的代码。


@user_page.route("/logout", methods=["GET"])
def logout():
    model_user.current_login_user = None
    return render_template("01index.html")


@user_page.route("/register", methods=["GET"])
def register():
    model_user.current_login_user = None
    return render_template("00register.html")

@user_page.route("/register", methods=["POST"])
def register_post():
    req = request.values
    username = req["username"] if "username" in req else ""
    password = req["password"] if "password" in req else ""
    email = req['email'] if "email" in req else ""
    register_time = req['register_time'] if "register_time" in req else ""
    role = req['role'] if "role" in req else ""
    a = model_user.validate_username(username)
    b = model_user.validate_password(password)
    c = model_user.validate_email(email)
    if a and b and c:
        # register this user
        model_user.register_user(username, password, email, register_time, role)
        return render_result(msg="register successfully!")
    else:
        return render_err_result(msg="inproper message for users")
    #return render_template("00login.html")

@user_page.route("/student-list", methods=["GET"])
def student_list():
    if User.current_login_user:
        page = request.args["page"] if "page" in request.args.keys() else 1
    context = {}
    
    one_page_user_list,total_pages,total_num = Student.get_student_by_page(page)
    page_num_list = Course.generate_page_num_list(page, total_pages)
    
    current_page = req['current_page'] if "current_page" in req else 1
    

    context['one_page_user_list'] = one_page_user_list
    context['total_pages'] = total_pages
    context['page_num_list'] = page_num_list
    context['current_page'] = int(page)
    context['total_num'] = total_num
    context['current_user_role'] = Student.current_login_user.role
    if not User.current_login_user:
        return redirect(url_for("index_page.index"))
    else:
        return render_template("10student_list.html",**context)

@user_page.route("/student-info", methods=["GET"])
def student_info():
    req = request.values
    id = req['id'] if "id" in req else ""
    context = {}
    return_id = model_student.get_student_by_id(id)
    if not return_id:
        context["user"] = model_student
        context["current_user_role"] = model_student.role
    else:
        context["user"] = model_user
        context["current_user_role"] = model_user.current_login_user.role
    return render_template("11student_info.html",**context)#########

@user_page.route("/student-delete", methods=["GET"])
def student_delete():
    req = request.values
    id = req['id'] if "id" in req else ""
    model_student.delete_student_by_id(id)
    #return render_template("10student_list.html")###########
    return     url_for("user_page.student-list", page=1)

# 5. templates/11student_info.html页面 创建一个页面，让一个标题打印出“Student Info”和一个学生的所有信息。在给定的div标记中编写代码



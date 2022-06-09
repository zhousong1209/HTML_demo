from flask import Blueprint, render_template, request, redirect, url_for
from lib.helper import render_result, render_err_result, course_data_path, user_data_path
from model.user import User
from model.course import Course

import pandas as pd
from flask import render_template, Blueprint

from model.user_instructor import Instructor

instructor_page = Blueprint("instructor_page", __name__)

model_instructor = Instructor()
model_course = Course()


@instructor_page.route("/instructor-list", methods=["GET"])
def instructor_list():
    if model_instructor=='Instructor':# check login user
        req = request.values
        page = req['page'] if "page" in req else 1
        context = {}
        # get values for one_page_instructor_list, total_pages, total_num
        one_page_instructor_list = req['one_page_instructor_list'] if "one_page_instructor_list" in req else 1
        # get values for page_num_list
        page_num_list = req['page_num_list'] if "page_num_list" in req else 1
        # check one_page_instructor_list, make sure this variable not be None, if None, assign it to []
        if one_page_instructor_list == None:
            one_page_instructor_list = []

        context['one_page_instructor_list'] = one_page_instructor_list
        context['total_pages'] = total_pages
        context['page_num_list'] = page_num_list
        context['current_page'] = int(page)
        context['total_num'] = total_num
        # add "current_user_role" to context
        context['current_user_role'] = model_instructor.current_login_user.role
    else:
        return redirect(url_for("index_page.index"))
    
    return redirect(url_for("index_page.index"))
    return render_template("07instructor_list.html", **context)

@instructor_page.route("/teach-courses", methods=["GET"])
def teach_courses():
    context = {}

    if model_instructor=='Student':# check login user
        # get instructor id
        req = request.values
        instructor_id = req['id'] if "id" in req else model_instructor.uid
        # get values for course_list, total_num
        course_list = req['course_list'] if "course_list" in req else 1
        total_num = req['total_num'] if "total_num" in req else 1
        context['course_list'] = course_list
        context['total_num'] = total_num
        # add "current_user_role" to context
        context['current_user_role'] = model_instructor.current_login_user.role
    else:
        return redirect(url_for("index_page.index"))
    return render_template("09instructor_courses.html", **context)



@instructor_page.route("/instructor-analysis")
def instructor_analysis():
    # if Instructor.instructor_data.shape[0] == 0:
    #     return render_err_result(msg="no instructor in datafile")

    explain1 = model_instructor.generate_instructor_figure1()

    context = {}
    context['explain1'] = explain1

    return render_template("08instructor_analysis.html", **context)


@instructor_page.route("/process-instructor", methods=["POST"])
def process_instructor():
    try:
        model_instructor.get_instructors()
    except Exception as e:
        print(e)
        return render_err_result(msg="error in process instructors")

    return render_result(msg="process instructors finished successfully")

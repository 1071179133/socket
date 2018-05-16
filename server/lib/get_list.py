#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# author：chenjianwen
# email：1071179133@qq.com
import os
import sys
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib.logger import logger
from lib.init_db_dir import databases
from lib import read_and_write_file as rw


def get_school_list():
    data = rw.read(databases)
    logger.info("可选择的学校有：")
    for school_name in data["school"]:
        print(school_name)

def get_course_list(belong_to_school):
    data = rw.read(databases)
    logger.info("可选择的课程有：")
    for course_name in data["course"]:
        if data["course"][course_name]["belong_to_school"] == belong_to_school:
            print(course_name)

def get_classes_list(belong_to_course):
    data = rw.read(databases)
    logger.info("可选择的班级有：")
    for classes_name in data["classes"]:
        if data["classes"][classes_name]["belong_to_course"] == belong_to_course:
            print(classes_name)

def get_teacher_list(belong_to_school):
    data = rw.read(databases)
    logger.info("可选择的讲师有：")
    for teacher_name in data["teacher"]:
        if data["teacher"][teacher_name]["belong_to_school"] == belong_to_school:
            teacher_major = data["teacher"][teacher_name]["teacher_major"]
            print("名字",teacher_name,"专业：",teacher_major)

# get_school_list()
# get_course_list("撸码学院北京校区")
# get_classes_list("python自动化开发")
# get_teacher_list("撸码学院北京校区")
'''
Created on June 20, 2016

@author: Yue
'''

import os
import json
import re

import mysql.connector

from sets import Set
import datetime

def problem_structure(path):
    
    # Connect to the database
    connection = mysql.connector.connect(user='root', password='123456', host='127.0.0.1', database='EX101x_3T2015')
    cursor = connection.cursor()
    tablecheck =('DROP TABLE IF EXISTS problem_courseware_studentmodule')
    cursor.execute(tablecheck)
    connection.commit()

    problem_structure_table = (
    "  CREATE TABLE `problem_courseware_studentmodule` ("
    "  `module_id` int NOT NULL,"
    "  `problem_id` varchar(255) NOT NULL,"
    "  `course_user_id` varchar(255) NOT NULL,"
    "  `grade` float NOT NULL,"
    "  `max_grade` float NOT NULL,"
    "  `created` datetime,"
    "  `modified` datetime,"
    "  PRIMARY KEY (`module_id`),"
    "  FOREIGN KEY (`course_user_id`) REFERENCES `course_user`(`course_user_id`),"
    "  FOREIGN KEY (`problem_id`) REFERENCES `problems`(`problem_id`),"
    "  FOREIGN KEY (`problem_id`) REFERENCES `resources`(`resource_id`),"
    "  KEY `index` (`module_id`, `problem_id`, `course_user_id`)"
    ") ENGINE=MyISAM")
    cursor.execute(problem_structure_table)
    connection.commit()


    # problem_structure(problem_id, relevant_week, chapter_id, chapter_start, sequential_id, sequential_start, sequential_due, vertical_id, course_id)
    
    global_course_id = ""
    global_course_id_org = ""

    # Processing course_structure data
    metadata_files = os.listdir(path)          
    for file in metadata_files:   
        if "courseware_studentmodule" in file:
            print file                       
            fp = open(path + file,"r")
            problemCounter = 0
            with open(path + file, 'r') as inputfile:
                for line in inputfile:
                    if problemCounter == 0:
                        # Skip the header
                        problemCounter = problemCounter + 1
                        continue

                    items = line.split("\t")
                    if items[1] != "problem":
                        continue

                    problemCounter = problemCounter + 1
                    if problemCounter % 10000 == 0:
                        print problemCounter

                    module_id = items[0]
                    problem_id = items[2]

                    course_id_array = problem_id.split(":")[1].split("+")
                    global_course_id_org = course_id_array[0] + "+" + course_id_array[1] + "+" + course_id_array[2]
                    global_course_id = "course-v1:" + course_id_array[0] + "+" + course_id_array[1] + "+" + course_id_array[2]

                    course_user_id = global_course_id + "_" + items[3]

                    grade = items[-6]
                    created = items[-5]
                    modified = items[-4]
                    max_grade = items[-3]

                    sql = "insert into problem_courseware_studentmodule(module_id, problem_id, course_user_id, grade, max_grade, created, modified) values"
                    sql += "('%s','%s','%s','%s','%s','%s','%s');" % (module_id, problem_id, course_user_id, grade, max_grade, created, modified)
                    cursor.execute(sql)  
            
            problemCounter = problemCounter - 1
            print "Number of Recorded Problems: " + str(problemCounter)
    
    connection.close()
    
    print "Problem Courseware Studentmodule Constructed."

problem_structure("/Volumes/YuePassport/course_log/EX101x-3T2015/")


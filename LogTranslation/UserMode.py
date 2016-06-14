'''
Created on Jul 24, 2015

@author: Angus
'''

import os
import json
import time,datetime
import mysql.connector
from sets import Set
  
def cmp_datetime(a_datetime, b_datetime):    
    a_datetime = a_datetime.replace("T", " ")
    a_datetime = a_datetime.replace("Z", "")
    b_datetime = b_datetime.replace("T", " ")
    b_datetime = b_datetime.replace("Z", "")
    
    format="%Y-%m-%d %H:%M:%S";
    a_time = datetime.datetime.strptime(a_datetime,format)
    b_time = datetime.datetime.strptime(b_datetime,format)
    
    if a_time < b_time:
        return False
    elif a_time >= b_time:
        return True 
    
def user_mode(path):
    
    files = os.listdir(path)
    
    # Connect to the database
    connection = mysql.connector.connect(user='root', password='123456', host='127.0.0.1', database='FP101x_3T2015')
    cursor = connection.cursor()
    
    # 1. course table
    course_id = ""
    course_name = ""
    course_start_time = ""
    course_end_time = ""
    
    course_id_org = ""

    # 2. user_pii table
    user_mail_map = {}
    
    # 3. course_user table
    course_user_map = {}
    user_enrollment_time_map = {}
    
    # Enrolled learners set
    enrolledLearner_set = Set()
    
    # Processing course_structure data                
    for file in files:             
        if "course_structure" in file:           
            fp = open(path + file, "r")     
            lines = fp.readlines()
            jsonLine = ""   
            for line in lines:                
                line = line.replace("\n", "")
                jsonLine += line
            
            # To extract course_id     
            course_id_array = file.split("-")
            course_id = "course-v1:" + course_id_array[0] + "+" + course_id_array[1] + "+" + course_id_array[2]
            course_id_org = course_id_array[0] + "+" + course_id_array[1] + "+" + course_id_array[2]

            jsonObject = json.loads(jsonLine)
            for record in jsonObject:
                if jsonObject[record]["category"] == "course":                    
                    course_name = jsonObject[record]["metadata"]["display_name"]
                    course_start_time = jsonObject[record]["metadata"]["start"]
                    course_end_time = jsonObject[record]["metadata"]["end"]
            

            # time data in the table is YYYY-MM-DDThh:mm:ssZ                    
            sql = "insert into courses(course_id, course_name, course_start_time, course_end_time) values"
            sql += "('%s','%s','%s','%s');" % (course_id, course_name, course_start_time, course_end_time)
            cursor.execute(sql)
            
    # Processing student_courseenrollment data

    for file in files:       
        if "student_courseenrollment" in file:
            fp = open(path + file, "r")
            fp.readline()
            lines = fp.readlines()
                        
            for line in lines:
                record = line.split("\t")
                global_user_id = record[1]
                course_id = record[2]
                time = record[3]
                course_user_id = course_id + "_" + global_user_id
                    
                if cmp_datetime(course_end_time, time):
                    enrolledLearner_set.add(global_user_id)
                    
                    sql = "insert into global_user(global_user_id, course_id, course_user_id) values"
                    sql += "('%s','%s','%s');" % (global_user_id, course_id, course_user_id)
                    cursor.execute(sql)
                    
                    course_user_map[global_user_id] = course_user_id
                    user_enrollment_time_map[global_user_id] = time
        
            print "The number of enrolled learners is: " + str(len(enrolledLearner_set)) + "\n"
  
    # Processing auth_user data  
    for file in files:               
        if "auth_user-" in file:
            fp = open(path + file, "r")
            fp.readline()
            lines = fp.readlines()
                        
            for line in lines:
                record = line.split("\t")
                if record[0] in enrolledLearner_set:
                    email = record[4]
                    if "'" in email:
                        email = email.replace("'", "\\'")
                    user_mail_map[record[0]] = email
                    
    # Processing certificates_generatedcertificate data
    num_uncertifiedLearners = 0
    num_certifiedLearners = 0    
    for file in files:       
        if "certificates_generatedcertificate" in file:
            fp = open(path + file, "r")
            fp.readline()
            lines = fp.readlines()
                                    
            for line in lines:
                record = line.split("\t")
                global_user_id = record[1]
                final_grade = record[3]
                enrollment_mode = record[14].replace("\n", "")
                certificate_status = record[7]                         
                
                if course_user_map.has_key(global_user_id):
                    
                    num_certifiedLearners += 1
                    
                    sql = "insert into course_user(course_user_id, final_grade, enrollment_mode, certificate_status, register_time) values"
                    sql += "('%s','%s','%s','%s','%s');" % (course_user_map[global_user_id], final_grade, enrollment_mode, certificate_status, user_enrollment_time_map[global_user_id])
                    cursor.execute(sql)                
                else:
                    num_uncertifiedLearners += 1

            # print "The number of uncertified learners is: " + str(num_uncertifiedLearners)
            # print "The number of certified learners is: " + str(num_certifiedLearners) + "\n"    
    
    # Processing auth_userprofile data
    num_user_pii = 0                    
    for file in files:       
        if "auth_userprofile" in file:
            fp = open(path + file, "r")
            fp.readline()
            lines = fp.readlines()
            
            for line in lines:
                record = line.split("\t")
                global_user_id = record[1]
                gender = record[7]
                year_of_birth = record[9]
                level_of_education = record[10]
                country = record[13]
                                
                if global_user_id in enrolledLearner_set:
                    num_user_pii += 1
                    
                    course_user_id = course_user_map[global_user_id]
                    
                    sql = "insert into user_pii(course_user_id, gender, year_of_birth, level_of_education, country, email) values"
                    sql += "('%s','%s','%s','%s','%s','%s');" % (course_user_id, gender, year_of_birth, level_of_education, country, user_mail_map[global_user_id])
                                 
                    cursor.execute(sql)         
            
            # print "The number of records in the user_pii file is: " + str(len(lines))
            # print "The number of selected user_pii records is: " + str(num_user_pii) + "\n"
            
    connection.close()
 
    print "User mode finished."
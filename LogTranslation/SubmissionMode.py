'''
Created on Jul 24, 2015

@author: Angus
'''

import os
import json
import re

import mysql.connector

from sets import Set
import datetime

def getNextDay(current_day_string):
    format="%Y-%m-%d";
    current_day = datetime.datetime.strptime(current_day_string,format)
    oneday = datetime.timedelta(days=1)
    next_day = current_day + oneday   
    return str(next_day)[0:10]

def submission_mode(path):
    
    # Connect to the database
    connection = mysql.connector.connect(user='root', password='123456', host='127.0.0.1', database='FP101x_3T2015')
    cursor = connection.cursor()
    
    global_course_id = ""
    global_course_id_org = ""

    # Processing course_structure data
    metadata_files = os.listdir(path)          
    for file in metadata_files:   
        if "course_structure" in file:                       
            fp = open(path + file,"r")            
            lines = fp.readlines()
            jsonLine = ""   
            for line in lines:
                line = line.replace("\n","")
                jsonLine += line
                
            # To extract course_id    
            course_id_array = file.split("-")
            global_course_id_org = course_id_array[0] + "+" + course_id_array[1] + "+" + course_id_array[2]
            global_course_id = "course-v1:" + course_id_array[0] + "+" + course_id_array[1] + "+" + course_id_array[2]
                
            # Problem collection
            problem_collection = []

            children_parent_map = {}            
            block_type_map = {}
                        
            jsonObject = json.loads(jsonLine)
            for record in jsonObject:
                if jsonObject[record]["category"] == "course":
                    # To obtain the course_start time
                    course_start_date = jsonObject[record]["metadata"]["start"]
                    course_start_date = course_start_date[0:course_start_date.index("T")]
                    # To obtain the course_end time
                    course_end_date = jsonObject[record]["metadata"]["end"]
                    course_end_date = course_end_date[0:course_end_date.index("T")]
                else:
                    resourse_id = record
                                        
                    # Record all the problems id
                    if jsonObject[resourse_id]["category"] == "problem":
                        problem_collection.append(resourse_id)   
                    
                    # Children to parent relation                    
                    for child in jsonObject[resourse_id]["children"]:
                        children_parent_map[child] = resourse_id                                                 
                    
                    # Types of blocks to which problems belong
                    if jsonObject[resourse_id]["category"] == "sequential":
                        if "display_name" in jsonObject[resourse_id]["metadata"]:
                            block_type = jsonObject[resourse_id]["metadata"]["display_name"]
                            block_type_map[resourse_id] = block_type                                      
                        
            # To locate problem_type for each problem
            for problem in problem_collection:                
                
                problem_parent = children_parent_map[problem]                
                while not block_type_map.has_key(problem_parent):
                    problem_parent = children_parent_map[problem_parent]
                    
                problem_type = block_type_map[problem_parent]                
                
                sql = "insert into problems(problem_id, problem_type) values"
                sql += "('%s','%s');" % (problem, problem_type)                    
                cursor.execute(sql) 
                          
    # Processing events data
    
    submission_event_collection = []
    submission_event_collection.append("problem_check")
    submission_event_collection.append("problem_check_fail")
    submission_event_collection.append("problem_reset") # event_source: browser
    submission_event_collection.append("problem_rescore")
    submission_event_collection.append("problem_rescore_fail")
    submission_event_collection.append("problem_save") # event_source: browser
    submission_event_collection.append("show_answer")
    submission_event_collection.append("save_problem_fail")
    submission_event_collection.append("save_problem_success")
    submission_event_collection.append("problem_graded")

    submission_id_set = Set()
    assessments = {}
    
    current_date = course_start_date
    course_end_date = getNextDay(course_end_date)
    
    log_files = os.listdir(path)

    while True:
        
        if current_date == course_end_date:
            break;
        
        for file in log_files:
            if current_date in file:
                print file
                fp = open(path + file,"r")                
                lines = fp.readlines()
                        
                for line in lines:                              
                    jsonObject = json.loads(line)
                
                    if jsonObject["event_type"] in submission_event_collection:
                        
                        course_id = jsonObject["context"]["course_id"]
                        
                        # Only translate the records pertinent to the specific course
                        if global_course_id != course_id:
                            continue
                          
                        # Some log records have empty user_id value  
                        if jsonObject["context"]["user_id"] != "":
                            
                            course_user_id = course_id + "_" + str(jsonObject["context"]["user_id"]) 
                            
                            problem_id = ""
                        
                            grade = ""
                            max_grade = ""
                            
                            event_time = jsonObject["time"]
                            event_time = event_time[0:19]
                            event_time = event_time.replace("T", " ")
                            format="%Y-%m-%d %H:%M:%S"
                            event_time = datetime.datetime.strptime(event_time,format)               
                        
                            if isinstance(jsonObject["event"], dict):                     
                                problem_id = jsonObject["event"]["problem_id"]
                                
                                # The fields "grade" and "max_grade" are specific to submission event "problem_check"
                                if jsonObject["event"].has_key("grade") and jsonObject["event"].has_key("max_grade"):
                                    grade = jsonObject["event"]["grade"]
                                    max_grade = jsonObject["event"]["max_grade"]
                                                                
                            if isinstance(jsonObject["event"], unicode):
                                                                                    
                                regex = re.compile("input_[a-zA-Z0-9-_]+")
                                problem_id_array = regex.findall(jsonObject["event"])
                                if not len(problem_id_array) == 0:                                
                                    problem_id = problem_id_array[0]                                
                                
                                    subRegex = re.compile("-[a-zA-Z0-9]*_[a-zA-Z0-9]*-")
                                    if not len(subRegex.findall(problem_id)) == 0:
                                        original_course_id = subRegex.findall(problem_id)[0]
                                        changed_course_id = original_course_id.replace("_",".")
                                        problem_id = problem_id.replace(original_course_id, changed_course_id)
                                    
                                    problem_id = problem_id.replace("input_", "")
                                    problem_id = problem_id[0:problem_id.index("_")]
                                    
                                    xml_array = problem_id.split("-")
                                    problem_id = "block-v1:" + global_course_id_org + "+type@problem+block@" + xml_array[0]
                                    
                            if isinstance(jsonObject["event"], list):                     
                                problem_id = jsonObject["event"][0]
                                if problem_id != "":
                                    problem_id = problem_id.split("_")
                                    problem_id = "block-v1:" + global_course_id_org + "+type@problem+block@" + problem_id[1]
            
                            if problem_id != "":
                                
                                submission_id = course_user_id + "_" + problem_id
                            
                                # For submissions
                                if not submission_id in submission_id_set:
                                    submission_id_set.add(submission_id)
                                    
                                    sql = "insert into submissions(submission_id, course_user_id, problem_id, submission_timestamp) values"
                                    sql += "('%s','%s','%s','%s');" % (submission_id, course_user_id, problem_id, event_time)
                                    cursor.execute(sql)
                            
                                # For assessments
                                if jsonObject["event_source"] == "server":
                                    assessments[submission_id] = {"course_user_id":course_user_id, "max_grade":max_grade, "grade":grade}                  
                
        current_date = getNextDay(current_date)
        
    for assessment in assessments:
        
        sql = "insert into assessments(assessment_id, course_user_id, max_grade, grade) values"
        sql += "('%s','%s','%s','%s');" % (assessment, assessments[assessment]["course_user_id"], str(assessments[assessment]["max_grade"]), str(assessments[assessment]["grade"]))
        cursor.execute(sql)
        
    connection.close()
    
    print "Submission mode finished."


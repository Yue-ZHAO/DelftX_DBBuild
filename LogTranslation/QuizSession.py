'''
Created on Jan 18, 2016

@author: Angus
'''

import os
import json
import csv

import time,datetime
import operator

import mysql.connector

def getDayDiff(beginDate,endDate):  
    format="%Y-%m-%d"  
    bd = datetime.datetime.strptime(beginDate,format)  
    ed = datetime.datetime.strptime(endDate,format)      
    oneday = datetime.timedelta(days=1)  
    count = 0
    while bd != ed:  
        ed = ed - oneday  
        count += 1
    return count

def getNextDay(current_day_string):
    format="%Y-%m-%d";
    current_day = datetime.datetime.strptime(current_day_string,format)
    oneday = datetime.timedelta(days=1)
    next_day = current_day + oneday   
    return str(next_day)[0:10]

def cmp_datetime(a_datetime, b_datetime):
    if a_datetime < b_datetime:
        return -1
    elif a_datetime > b_datetime:
        return 1
    else:
        return 0 

def quiz_session(path):
    
    # Connect to the database
    connection = mysql.connector.connect(user='root', password='123456', host='127.0.0.1', database='FP101x_3T2015')
    cursor = connection.cursor()
    
    # Course information
    global_course_id = ""
    course_start_date = ""
    course_end_date = ""
    
    children_parent_map = {}
    
    # Processing course_structure data
    metadata_files = os.listdir(path)           
    for file in metadata_files:             
        if "course_structure" in file: 
            
            # To extract course_id     
            course_id_array = file.split("-")
            global_course_id = "course-v1:" + course_id_array[0] + "+" + course_id_array[1] + "+" + course_id_array[2]
                       
            fp = open(path + file,"r")            
            lines = fp.readlines()
            jsonLine = ""   
            for line in lines:
                line = line.replace("\n","")
                jsonLine += line
            
            jsonObject = json.loads(jsonLine)
            for record in jsonObject:
                if jsonObject[record]["category"] == "course":
                    # To obtain the course_start_date
                    course_start_date = jsonObject[record]["metadata"]["start"]
                    course_start_date = course_start_date[0:course_start_date.index("T")]
                    # To obtain the course_end_date
                    course_end_date = jsonObject[record]["metadata"]["end"]
                    course_end_date = course_end_date[0:course_end_date.index("T")]
                else:
                    resourse_id = record
                    
                    # Children to parent relation                    
                    for child in jsonObject[resourse_id]["children"]:
                        children_parent_map[child] = resourse_id
                    
            
    
    # Processing events data 
    current_date = course_start_date   
    course_end_next_date = getNextDay(course_end_date)
    
    submission_event_types = []
    submission_event_types.append("problem_check")
    submission_event_types.append("problem_check_fail")
    submission_event_types.append("problem_graded")
    submission_event_types.append("problem_rescore")
    submission_event_types.append("problem_rescore_fail")
    submission_event_types.append("problem_reset")           # event_source: browser
    submission_event_types.append("problem_save")            # event_source: browser
    submission_event_types.append("problem_show")
    submission_event_types.append("reset_problem")
    submission_event_types.append("reset_problem_fail") 
    submission_event_types.append("save_problem_fail")
    submission_event_types.append("save_problem_success")
    submission_event_types.append("show_answer")
    
    user_all_event_logs = {}    
    quiz_sessions = {}
    
    log_files = os.listdir(path)
    
    while True:
        
        if current_date == course_end_next_date:
            break;
        
        for file in log_files:           
            if current_date in file:
                
                print file
                                
                user_all_event_logs.clear()
                
                fp = open(path + file,"r")
                lines = fp.readlines()
                        
                for line in lines:
                    
                    jsonObject = json.loads(line)
                    
                    # For forum session separation
                    global_user_id = jsonObject["context"]["user_id"]
                    event_type = str(jsonObject["event_type"])
                                            
                    if global_user_id != "":
                        
                        course_id = jsonObject["context"]["course_id"]
                        course_user_id = course_id + "_" + str(global_user_id)
                        
                        event_time = jsonObject["time"]
                        event_time = event_time[0:19]
                        event_time = event_time.replace("T", " ")
                        format="%Y-%m-%d %H:%M:%S"
                        event_time = datetime.datetime.strptime(event_time,format)
                                               
                        if user_all_event_logs.has_key(course_user_id):
                            user_all_event_logs[course_user_id].append({"event_time":event_time, "event_type":event_type})
                        else:
                            user_all_event_logs[course_user_id] = [{"event_time":event_time, "event_type":event_type}]
                            
                # For quiz session separation
                for user in user_all_event_logs.keys():
                    
                    course_user_id = user                    
                    event_logs = user_all_event_logs[user]
                    
                    # Sorting
                    event_logs.sort(cmp=cmp_datetime, key=operator.itemgetter('event_time'))
                      
                    session_id = ""
                    start_time = ""
                    end_time = ""                    
                    
                    for i in range(len(event_logs)):
                        if session_id =="":
                            
                            if "problem+block" in event_logs[i]["event_type"]:
                                
                                event_type_array = event_logs[i]["event_type"].split("/")
                                problem_id = event_type_array[4]
                                
                                if problem_id in children_parent_map.keys():
                                    parent_block_id = children_parent_map[problem_id]
                                
                                    session_id = "quiz_session_" + parent_block_id + "_" +course_user_id
                                    start_time = event_logs[i]["event_time"]
                                    end_time = event_logs[i]["event_time"]                                
                                                                                        
                        else:
                            if "problem+block" in event_logs[i]["event_type"] or event_logs[i]["event_type"] in submission_event_types:

                                if event_logs[i]["event_time"] > end_time + datetime.timedelta(hours=0.5):
                                    if quiz_sessions.has_key(session_id):
                                        quiz_sessions[session_id]["time_array"].append({"start_time":start_time, "end_time":end_time})
                                    else:
                                        quiz_sessions[session_id] = {"course_user_id":course_user_id, "time_array":[{"start_time":start_time, "end_time":end_time}]}
                                        
                                    
                                    if "problem+block" in event_logs[i]["event_type"]:
                                    
                                        event_type_array = event_logs[i]["event_type"].split("/")
                                        problem_id = event_type_array[4]
                                        
                                        if problem_id in children_parent_map.keys():
                                            parent_block_id = children_parent_map[problem_id]
                                
                                            session_id = "quiz_session_" + parent_block_id + "_" +course_user_id
                                            start_time = event_logs[i]["event_time"]
                                            end_time = event_logs[i]["event_time"]
                                        else:
                                            session_id = ""
                                            start_time = ""
                                            end_time = ""     
                                else:                                    
                                    end_time = event_logs[i]["event_time"]                            
                            else:
                                
                                end_time = event_logs[i]["event_time"]
                                
                                if quiz_sessions.has_key(session_id):
                                    quiz_sessions[session_id]["time_array"].append({"start_time":start_time, "end_time":end_time})
                                else:
                                    quiz_sessions[session_id] = {"course_user_id":course_user_id, "time_array":[{"start_time":start_time, "end_time":end_time}]}
                                    
                                session_id = ""
                                start_time = ""
                                end_time = ""
                                
                        if i == len(event_logs) - 1:
                            
                            if session_id == "" and "problem+block" in event_logs[i]["event_type"]:
                                
                                event_type_array = event_logs[i]["event_type"].split("/")
                                problem_id = event_type_array[4]
                                
                                if problem_id in children_parent_map.keys():
                                    parent_block_id = children_parent_map[problem_id]
                                
                                    session_id = "quiz_session_" + parent_block_id + "_" +course_user_id
                                    start_time = event_logs[i]["event_time"]
                                    end_time = event_logs[i]["event_time"]
                                    
                                    if quiz_sessions.has_key(session_id):
                                        quiz_sessions[session_id]["time_array"].append({"start_time":start_time, "end_time":end_time})
                                    else:
                                        quiz_sessions[session_id] = {"course_user_id":course_user_id, "time_array":[{"start_time":start_time, "end_time":end_time}]}
                            
                            if session_id != "":
                                
                                if "problem+block" in event_logs[i]["event_type"] or event_logs[i]["event_type"] in submission_event_types:
                                    
                                    if event_logs[i]["event_time"] > end_time + datetime.timedelta(hours=0.5):
                                        if quiz_sessions.has_key(session_id):
                                            quiz_sessions[session_id]["time_array"].append({"start_time":start_time, "end_time":end_time})
                                        else:
                                            quiz_sessions[session_id] = {"course_user_id":course_user_id, "time_array":[{"start_time":start_time, "end_time":end_time}]}
                                                                                    
                                        if "problem+block" in event_logs[i]["event_type"]:
                                            
                                            event_type_array = event_logs[i]["event_type"].split("/")
                                            problem_id = event_type_array[4]
                                            
                                            if problem_id in children_parent_map.keys():
                                                parent_block_id = children_parent_map[problem_id]
                                
                                                session_id = "quiz_session_" + parent_block_id + "_" +course_user_id
                                                start_time = event_logs[i]["event_time"]
                                                end_time = event_logs[i]["event_time"]
                                            
                                                if quiz_sessions.has_key(session_id):
                                                    quiz_sessions[session_id]["time_array"].append({"start_time":start_time, "end_time":end_time})
                                                else:
                                                    quiz_sessions[session_id] = {"course_user_id":course_user_id, "time_array":[{"start_time":start_time, "end_time":end_time}]}
                                            
                                            
                                                                               
                                    else:
                                        
                                        end_time = event_logs[i]["event_time"]
                                            
                                        if quiz_sessions.has_key(session_id):
                                            quiz_sessions[session_id]["time_array"].append({"start_time":start_time, "end_time":end_time})                                            
                                        else:
                                            quiz_sessions[session_id] = {"course_user_id":course_user_id, "time_array":[{"start_time":start_time, "end_time":end_time}]}
                                        
                                else:
                                    
                                    end_time = event_logs[i]["event_time"]
                                    
                                    if quiz_sessions.has_key(session_id):
                                        quiz_sessions[session_id]["time_array"].append({"start_time":start_time, "end_time":end_time})
                                    else:
                                        quiz_sessions[session_id] = {"course_user_id":course_user_id, "time_array":[{"start_time":start_time, "end_time":end_time}]}
                            
        current_date = getNextDay(current_date)
    
    # To compress the session event_logs
    for session in quiz_sessions:
        if len(quiz_sessions[session]["time_array"]) > 1:            
            start_time = ""
            end_time = ""
            updated_time_array = []
            
            for i in range(len(quiz_sessions[session]["time_array"])):                
                if i == 0:
                    start_time = quiz_sessions[session]["time_array"][i]["start_time"]
                    end_time = quiz_sessions[session]["time_array"][i]["end_time"]
                else:
                    if quiz_sessions[session]["time_array"][i]["start_time"] > end_time + datetime.timedelta(hours=0.5):
                        updated_time_array.append({"start_time":start_time, "end_time":end_time})                        
                        start_time = quiz_sessions[session]["time_array"][i]["start_time"]
                        end_time = quiz_sessions[session]["time_array"][i]["end_time"]
                    else:
                        end_time = quiz_sessions[session]["time_array"][i]["end_time"]
                        
                if i == len(quiz_sessions[session]["time_array"]) - 1:
                    updated_time_array.append({"start_time":start_time, "end_time":end_time})
            
            quiz_sessions[session]["time_array"] = updated_time_array
            
    # Output quiz_sessions table
    for session in quiz_sessions:        
        session_id = session
        course_user_id = quiz_sessions[session]["course_user_id"]
        
        for i in range(len(quiz_sessions[session]["time_array"])):
            start_time = quiz_sessions[session]["time_array"][i]["start_time"]
            end_time = quiz_sessions[session]["time_array"][i]["end_time"]
            if start_time < end_time:
                duration = (end_time - start_time).days * 24 * 60 * 60 + (end_time - start_time).seconds
                final_session_id = session_id + "_" + str(start_time) + "_" + str(end_time)
                
                if duration > 5:
                    sql = "insert into quiz_sessions (quiz_session_id, course_user_id, start_time, end_time, duration) values"
                    sql += "('%s','%s','%s','%s','%s');" % (final_session_id, course_user_id, start_time, end_time, duration)
                    cursor.execute(sql)
    
    connection.close()
    print "Quiz sessions finished."


    

'''
Created on June 16, 2016

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
    tablecheck =('DROP TABLE IF EXISTS problem_structure')
    cursor.execute(tablecheck)
    connection.commit()

    problem_structure_table = (
    "  CREATE TABLE `problem_structure` ("
    "  `problem_id` varchar(255) NOT NULL,"
    "  `relevant_week` int NOT NULL,"
    "  `weight` float NOT NULL,"
    "  `chapter_id` varchar(255) NOT NULL,"
    "  `chapter_start` datetime,"
    "  `sequential_id` varchar(255),"
    "  `sequential_start` datetime,"
    "  `sequential_due` datetime,"
    "  `vertical_id` varchar(255),"
    "  `course_id` varchar(255) NOT NULL,"
    "  PRIMARY KEY (`problem_id`),"
    "  FOREIGN KEY (`course_id`) REFERENCES `courses`(`course_id`),"
    "  FOREIGN KEY (`problem_id`) REFERENCES `problems`(`problem_id`),"
    "  FOREIGN KEY (`problem_id`) REFERENCES `resources`(`resource_id`),"
    "  FOREIGN KEY (`chapter_id`) REFERENCES `resources`(`resource_id`),"
    "  KEY `index` (`problem_id`, `chapter_id`, `course_id`)"
    ") ENGINE=MyISAM")
    cursor.execute(problem_structure_table)
    connection.commit()


    # problem_structure(problem_id, relevant_week, chapter_id, chapter_start, sequential_id, sequential_start, sequential_due, vertical_id, course_id)
    
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
            problem_collection = {}
            sequential_collection = {}
            chapter_collection = {}
            session_date = []

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

                    for child in jsonObject[record]["children"]:
                        children_parent_map[child] = global_course_id

                else:
                    resourse_id = record

                    if jsonObject[resourse_id]["category"] == "chapter":
                        # chapter_id + chapter start time
                        if jsonObject[resourse_id]["metadata"].has_key("start"):
                            starttime = jsonObject[resourse_id]["metadata"]["start"]
                            chapter_collection[resourse_id] = starttime
                            # Each chapter has its own start time, some of them may have the same start time.
                            # I collect all the start time in Set, and then sort them, from the earliest to the latest
                            # Each start time represent a start of a week ( or a learning session)!
                            startdate = starttime[0:10]
                            if startdate not in session_date:
                                session_date.append(startdate)

                        else:
                            chapter_collection[resourse_id] = "0"
                    
                    # Types of blocks to which problems belong
                    if jsonObject[resourse_id]["category"] == "sequential":
                        # if "graded" in jsonObject[resourse_id]["metadata"]:                            
                        #     if jsonObject[resourse_id]["metadata"]["graded"] is True:
                        # not all the sequential has graded problem are tagged as "graded": true
                        tempdict = {}
                        if jsonObject[resourse_id]["metadata"].has_key("due"):
                            tempdict["due"] = jsonObject[resourse_id]["metadata"]["due"]
                        else:
                            tempdict["due"] = "0"

                        if jsonObject[resourse_id]["metadata"].has_key("start"):
                            tempdict["start"] = jsonObject[resourse_id]["metadata"]["start"]
                        else:
                            tempdict["start"] = "0"
                        # add resourse_id
                        # jsonObject[resourse_id]["metadata"]["due"]
                        # jsonObject[resourse_id]["metadata"]["start"]
                        sequential_collection[resourse_id] = tempdict

                    # Record all the problems id
                    if jsonObject[resourse_id]["category"] == "problem":
                        if jsonObject[resourse_id]["metadata"].has_key("weight"):
                            problem_collection[resourse_id] = jsonObject[resourse_id]["metadata"]["weight"]
                        else:
                            # By default the weight is 1?
                            problem_collection[resourse_id] = 1.0

                    # Children to parent relation                    
                    for child in jsonObject[resourse_id]["children"]:
                        children_parent_map[child] = resourse_id  
            
            # Rank the session date
            session_date.sort()

            # To locate problem_type for each problem
            for problem in problem_collection:                
                problem_vertical_id = ""
                problem_sequential_id = ""
                problem_sequential_start = "0"
                problem_sequential_due = "0"
                problem_chapter_id = ""
                problem_chapter_start = "0"
                session_order = 0
                problem_weight = problem_collection[problem]


                # print "problem id: " + problem
                problem_parent = children_parent_map[problem]
                if "vertical" in problem_parent:
                    problem_vertical_id = problem_parent
                    # print "vertical id: " + problem_vertical_id
                    problem_parent = children_parent_map[problem_parent]

                if "sequential" in problem_parent:
                    problem_sequential_id = problem_parent
                    # print "sequential id: " + problem_sequential_id
                    if sequential_collection[problem_sequential_id].has_key("start"):
                        problem_sequential_start = sequential_collection[problem_sequential_id]["start"]
                    if sequential_collection[problem_sequential_id].has_key("due"):
                        problem_sequential_due = sequential_collection[problem_sequential_id]["due"]
                    problem_parent = children_parent_map[problem_parent]

                if "chapter" in problem_parent:
                    problem_chapter_id = problem_parent
                    # print "chapter id: " + problem_chapter_id
                    if problem_chapter_id in chapter_collection:
                        problem_chapter_start = chapter_collection[problem_chapter_id]

                if problem_chapter_start != "0":
                    problem_chapter_start_date = problem_chapter_start[0:10]
                    session_order = session_date.index(problem_chapter_start_date) + 1


                if problem_sequential_start == "0":
                    problem_sequential_start = problem_chapter_start

                print (problem + ", "
                     + str(session_order) + ", "
                     + str(problem_weight) + ", "
                     + problem_chapter_id + ", "
                     + problem_chapter_start + ", "
                     + problem_sequential_id + ", "
                     + problem_sequential_start + ", "
                     + problem_sequential_due + ", "
                     + problem_vertical_id + ", "
                     + global_course_id)
                print ""


                # while not block_type_map.has_key(problem_parent):
                #     problem_parent = children_parent_map[problem_parent]
                    
                # problem_type = block_type_map[problem_parent]                
                
                # sql = "insert into problems(problem_id, problem_type) values"
                # sql += "('%s','%s');" % (problem, problem_type)                    
                # cursor.execute(sql)
                sql = "insert into problem_structure(problem_id, relevant_week, weight, chapter_id, chapter_start, sequential_id, sequential_start, sequential_due, vertical_id, course_id) values"
                sql += "('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');" % (problem, session_order, problem_weight, problem_chapter_id, problem_chapter_start, problem_sequential_id, problem_sequential_start, problem_sequential_due, problem_vertical_id, global_course_id)
                cursor.execute(sql)  
            
            # print session_date
    # connection.close()
    
    print "Problem Structure Constructed."

problem_structure("/Volumes/YuePassport/course_log/EX101x-3T2015/")


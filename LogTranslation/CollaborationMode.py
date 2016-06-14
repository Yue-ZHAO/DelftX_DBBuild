'''
Created on Jul 24, 2015

@author: Angus
'''

import os
import json

import time,datetime
from time import *

import mysql.connector

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def collaboration_mode(path):
    
    files = os.listdir(path)
    
    # Course information
    course_end_time = ""
    
    # Processing course_structure data                
    for file in files:             
        if "course_structure" in file:           
            fp = open(path + file, "r")            
            lines = fp.readlines()
            jsonLine = ""   
            for line in lines:
                line = line.replace("\n", "")
                jsonLine += line

            jsonObject = json.loads(jsonLine)
            for record in jsonObject:
                if jsonObject[record]["category"] == "course":
                    course_end_time = jsonObject[record]["metadata"]["end"]
                    
                    format="%Y-%m-%d %H:%M:%S"
                       
                    course_end_time = course_end_time[0:19]
                    course_end_time = course_end_time.replace("T", " ")                    
                    course_end_time = datetime.datetime.strptime(course_end_time,format)
    
    # Connect to the database
    connection = mysql.connector.connect(user='root', password='123456', host='127.0.0.1', database='FP101x_3T2015')
    cursor = connection.cursor()
    
    # Processing forum data      
    for file in files:
        if ".mongo" in file:
            fp = open(path + file,"r")   
            for line in fp:
                jsonObject = json.loads(line)
                   
                collaboration_id = jsonObject["_id"]["$oid"]                
                course_user_id = jsonObject["course_id"] + "_" + jsonObject["author_id"]                

                collaboration_type = jsonObject["_type"]
                if collaboration_type == "CommentThread":
                    collaboration_type += "_" + jsonObject["thread_type"]                
                if "parent_id" in jsonObject:
                    if jsonObject["parent_id"] != "":
                        collaboration_type = "Comment_Reply"
                
                collaboration_title = ""
                if "title" in jsonObject:
                    collaboration_title=jsonObject["title"]
                
                collaboration_content = jsonObject["body"]
                
                collaboration_timestamp = jsonObject["created_at"]["$date"]
                
                #collaboration_timestamp = strftime("%Y-%m-%d %H:%M:%S",gmtime(collaboration_timestamp/1000))
                #collaboration_timestamp = datetime.datetime.strptime(collaboration_timestamp,"%Y-%m-%d %H:%M:%S")
                
                collaboration_timestamp = collaboration_timestamp[0:19]
                collaboration_timestamp = collaboration_timestamp.replace("T", " ")
                format="%Y-%m-%d %H:%M:%S"
                collaboration_timestamp = datetime.datetime.strptime(collaboration_timestamp,format)
                
                collaboration_parent_id = ""
                if "parent_id" in jsonObject:
                    collaboration_parent_id = jsonObject["parent_id"]["$oid"]
                
                collaboration_thread_id = ""    
                if "comment_thread_id" in jsonObject:
                    collaboration_thread_id = jsonObject["comment_thread_id"]["$oid"]                
                
                collaboration_title = collaboration_title.replace("\n", " ")
                collaboration_title = collaboration_title.replace("\\", "\\\\")
                collaboration_title = collaboration_title.replace("\'", "\\'")
                
                collaboration_content = collaboration_content.replace("\n", " ")
                collaboration_content = collaboration_content.replace("\\", "\\\\")
                collaboration_content = collaboration_content.replace("\'", "\\'")
                
                if collaboration_timestamp < course_end_time:
                           
                    sql = "insert into collaborations(collaboration_id, course_user_id, collaboration_type, collaboration_title, collaboration_content, collaboration_timestamp, collaboration_parent_id, collaboration_thread_id) values"
                    sql += "('%s','%s','%s','%s','%s','%s','%s', '%s');" % (collaboration_id, course_user_id, collaboration_type, collaboration_title, collaboration_content, collaboration_timestamp, collaboration_parent_id, collaboration_thread_id)  
                    
                    cursor.execute(sql)
                
            fp.close()
            
    connection.close()
       
    print "Collaboration mode finished."
'''
Created on Nov 5, 2015

@author: Angus
'''

import os
import LogTranslation.UserMode
import LogTranslation.CollaborationMode
import LogTranslation.SubmissionMode
import LogTranslation.ObservationMode
import LogTranslation.ForumSession
import LogTranslation.QuizSession

#import LogTranslation.SurveyMode

course_path = "/Volumes/YuePassport/course_log/FP101x-3T2015/"

# User mode
if os.path.isdir(course_path):
    LogTranslation.UserMode.user_mode(course_path)
    
# Observation mode
if os.path.isdir(course_path):
    LogTranslation.ObservationMode.observation_mode(course_path)     

# Collaboration mode
if os.path.isdir(course_path):
    LogTranslation.CollaborationMode.collaboration_mode(course_path)

# Submission mode
if os.path.isdir(course_path):
    LogTranslation.SubmissionMode.submission_mode(course_path)    


    
# Quiz Session
if os.path.isdir(course_path):
    LogTranslation.QuizSession.quiz_session(course_path)

# Forum Session
if os.path.isdir(course_path):
    LogTranslation.ForumSession.forum_session(course_path)
    
'''
# Survey mode
# if os.path.isdir(course_path):
#     LogTranslation.SurveyMode.survey_mode(course_path)  
'''

print "All finished."
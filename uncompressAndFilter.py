'''
Created on Nov 5, 2015

@author: Angus
'''

import os
import gzip
import traceback
import json

################# GENERAL DESCRIPTION  ####################
#
#  This script will extract the daily logs of specific courses.
#  In the output folder, each course has its own folder 
#  which contains all the uncompressed and filtered daily logs 
#  of the course.
#
###########################################################

# Search for the courses that have not been translated
try:

    ################# CONFIG - START ####################

    # zip_files & unzip_files folder path
    # Input folder is the zip folder which contains all the gzip daily logs
    # Output folder is the the unzip folder which contains 

    unzip_folder_path = "/Volumes/YuePassport/course_log/DailyEventLog3/"
    zip_folder_path = "/Volumes/YuePassport/course_log/DailyEventLog3/"
    # start and endates: only consider logfiles with the start and endrange. In order to be safe,
    # just slect one month before the startdate of the first couse, and plus one month after
    # the enddate of the last course
    startdate = "2015-07-01"    # use "yyyy-mm-dd" format
    enddate = "2016-03-01"      # use "yyyy-mm-dd" format
    # provide the IDs of the courses you are interested in
    courseids = [["EX101x","3T2015"], ["FP101x","3T2015"]] 
    # each course id is an array of the course code and the course quarter, e.g. ["EX101x","3T2015"]
    # the reason we seperate them to match the course id is that edx may change its data format some time

    ################# CONFIG - END ####################


    # Uncompress the log files

    ## iterate over all log files
    log_files = os.listdir(zip_folder_path)
    for log_file in log_files:
        if ".gz" in log_file:
            # check if current log file is in correct date / time range
            if log_file[18:28] >= startdate and log_file[18:28] <= enddate:
                print(log_file[18:28])

                ## build output folders for each course
                outputfiles = []
                for i in range(0, len(courseids)):
                    directory = unzip_folder_path + courseids[i][0]+"-"+courseids[i][1]+"/"
                    path = directory + log_file[0:-3]
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    outputfile = open(path, 'wt')
                    outputfiles.append(outputfile)

                with gzip.open(zip_folder_path + log_file, 'rt') as f:
                    for line in f:
                        jsonObject = json.loads(line)
                        for i in range(0, len(courseids)):
                            course = courseids[i]
                            if course[0] in jsonObject["context"]["course_id"] and course[1] in jsonObject["context"]["course_id"]:
                                outputfiles[i].write(line)

                for outputfile in outputfiles:
                    outputfile.close()

except Exception as e:
    print("Error occurs when translating\t")
    print(e)
    traceback.print_exc()

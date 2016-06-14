'''
Created on Dec 21, 2015

@author: Angus
'''

import os
import json
    
def LogFileCleaning(path):
    
    files = os.listdir(path)
    for file in files:
        # Processing events log data
        if "events" in file:
            print file
        
            # Output clear-out file
            clear_out_path1 = os.path.dirname(os.path.dirname(path)) + "/Clear-out/EX101x-3T2015/" + file
            if os.path.isfile(clear_out_path1):
                os.remove(clear_out_path1)
        
            clear_out_file1 = open(clear_out_path1, 'wb')

            clear_out_path2 = os.path.dirname(os.path.dirname(path)) + "/Clear-out/FP101x-3T2015/" + file
            if os.path.isfile(clear_out_path2):
                os.remove(clear_out_path2)
        
            clear_out_file2 = open(clear_out_path2, 'wb')
        
            fp = open(path + "/" + file,"r")   
            for line in fp:
                jsonObject = json.loads(line)            
                
                if "EX101x" in jsonObject["context"]["course_id"] and "3T2015" in jsonObject["context"]["course_id"]:
                    clear_out_file1.write(line)
                
                if "FP101x" in jsonObject["context"]["course_id"] and "3T2015" in jsonObject["context"]["course_id"]:
                    clear_out_file2.write(line)
                
            clear_out_file1.close()
            clear_out_file2.close()         


####################################################    
path = "/Volumes/YuePassport/course_log/DailyEventLog/"
LogFileCleaning(path)
print "Finished."       


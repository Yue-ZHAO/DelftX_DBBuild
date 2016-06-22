'''
Created on Nov 5, 2015

@author: Angus
'''

import os
import gzip


# Search for the courses that have not been translated
try:

    # zip_files & unzip_files folder path
    unzip_folder_path = "./uncompressed/"
    zip_folder_path = "./alllogs/"
    startdate = "2015-09-01"
    enddate = "2016-03-01"

    # Uncompress the log files

    log_files = os.listdir(zip_folder_path)
    for log_file in log_files:
        if ".gz" in log_file:
            if log_file[18:28]>= startdate and log_file[18:28]<=enddate:
                print(log_file[18:28])
                gz_file = gzip.GzipFile(zip_folder_path + log_file)
                log_file = log_file.replace(".gz", "")
                open(unzip_folder_path + log_file, "wb+").write(gz_file.read())
                gz_file.close()

except Exception as e:
    print("Error occurs when translating\t")
    print(e)

print ("All log files uncompressed.")

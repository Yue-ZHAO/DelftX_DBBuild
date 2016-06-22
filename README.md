# Building Database for Courses Data of MOOCs (EDX)

## 1. Database Building

### 1.1 Environmantal Setting

1. This manual is tested on Mac OSX. 

2. This manual is tested on course data of EX101x-3T2015 and FP101x-3T2015.

3. Python 2.7 should be well installed in the machine.

### 1.2 Installing MySQL

1. Downloading [MySQL Community Server](http://dev.mysql.com/downloads/mysql/)

2. Installing and recording the initial root password

3. Checking if MySQL installed in ```/usr/local/mysql/bin```

4. Setting PATH
    * Editting bash profile ```vim ~/.bash_profile```
    * Setting the path ```PATH=$PATH:/usr/local/mysql/bin```
    * Adding this in bash file:
    
    ```
    alias mysql=/usr/local/mysql/bin/mysql
    alias mysqladmin=/usr/local/mysql/bin/mysqladmin
    ```
    * Saving the setting ```esc``` + ```:wq```
    * Sourcing bash profile ```source ~/.bash_profile```

5. Running MySQL Server
    * Mac OS X users can start it on System Preferences
    
6. Setting the password of root
    * Using ```mysql -uroot -p``` with password to login MySQL
    * Inputting ```SET PASSWORD FOR 'root'@'localhost' = PASSWORD('newpass');```
    
7. Installing [MySQL Workbench](http://dev.mysql.com/downloads/workbench/) for connecting MySQL Server

8. Installing Connector/Python 
    * Please check the documents [MySQL Connector/Python Developer Guide](https://dev.mysql.com/doc/connector-python/en/connector-python-installation-binary.html)
    * MacOSX users can install it by ```sudo pip install mysql-connector-repackaged```
    * Checking if the package installed by using ```import mysql.connector``` 

### 1.3 Building the database

<!--1. Create database ```<database name>```
    * Login MySQL ```mysql -uroot -p```
    * ```CREATE DATABASE <database name>``` For example ```CREATE DATABASE FP101x_3T2015```-->
    
1. Editting self-contained file ```moocdb.sql``` by changing the database name as ```<database name>```

2. Open the file ```moocdb.sql``` by MySQL Workbench and Run the SQL script.

### 1.4 Reading course data into the the database
    
<!--2. Setting the folder
    * Root folder is named as the course name.
    * mkdir ```zip_files``` and ```unzip_files``` under the root folder
    * mkdir ```metadata``` under the folder ```unzip_files```, and put all the  files of metadata of the course into the folder ```metadata```
    * Put all the daily log files with ```.gz``` into ```zip_files```-->
    
1. Preprocessing daily log files: (All of following steps will be coded into ```LogFileCleaning.py``` later)
    * Checking the file whose name contains ```course_structure``` in the course metadata to get the course start time and the course end time;
    * Uncompressing all the daily log files whose timestamps are from course start time to the course end time (*you can uncompress more daily logs around course time range. For example, two weeks before the course start and after the course end*).
    * Editing ```Path``` of uncompressed course daily files in file ```LogFileCleaning.py```
    * Editing ```course name``` in file ```LogFileCleaning.py``` for filtering the daily log files of specific course.
    * ```python LogFileCleaning.py``` generating preprocessed daily log files

2. All the daily logs and metadata of the course should be put into the same folder.
    * Making a folder for a course. For example, you can name it as ```FP101x_3T2015```
    * Uncompressing all the metadata of the courses (the file ```<course name>.zip```)
    * Putting all the metadata of the course into the folder
    * Putting all preprocessed daily log files into the folder

3. Editing course folder path in ```main.py```

4. Editing database info in each ```.py``` files

5. Running the code by ```python main.py```

### 1.5 Problems

1. If ```null``` cannot be added into integer columns in some tables, changing the mode of MySQL to non-strict.
    * mkdir ```mysql``` in folder ```/etc```
    * ```sudo vi etc/mysql/my.cnf```
    * Adding content into ```my.cnf```
    
    ```
    [mysqld]
    sql_mode=NO_ENGINE_SUBSTITUTION
    ```
    * Restarting MySQL Server


## 2. Relations with The Moocdb Project

### 2.1 The Moocdb Project

[The MOOCdb Project](moocdb.csail.mit.edu) is an open source framework, which sets a shared data model standard for organzing data generated from MOOCs.

The initial schema of moocdb consists of four modules, which are Observing, Submitting, Collaborating and Feedback.

### 2.2 Our current schema

Our current schema is mainly based on the moocdb project. It consists of four modules, which are named as Observations, Submissions, Collaborations and UserModes. 

![Alt](./MOOCdb_Data_Model.png "Title")

As shown in Figure 1, each module in our schema has several tables of information. The differences between our current schema and the initial moocdb schema are discussed in the following sections.

### 2.3 Observing

In original Moocdb schema, Observing mode has five tables, which are observed_event, resources, resources_urls, resources_types and urls. 

In our current schema, we merge them into two tables, named observations and resources. This two tables represent the observed events of students and relevant resouces to events.

### 2.4 Submitting

In original Moocdb schema, Submitting mode has four tables, which are problem_type, problems, submissions, and assessments. 

In our current schema, we merge the problem table into problems table. After that, a table named quiz_sessions is added. quiz_sessions is leveraged to represent how users answer sessions of quiz.

### 2.5 Collaborating

In original Moocdb schema, Collaborating mode has two tables, which are collaborations and collaboration_types. 

In our current schema, the two original table collaborations and collaboration_types are combined into one table collaborations. forum_sessions is added as a new table, which represents users activities on forum.

### 2.6 UserModes

In our schema, we have another parts named user modes. which contains four tables named courses, global_user, course_user and user_pii.

Table courses contains the metainfo of courses. Table global_user represent the relations between users and courses. Table course_user represent users' status and grade in courses. Table user_pii represent course users' demographic data. 

## 3. Passing Students Checking

### 3.1 How many student passed the course in each week?

1. Manually checking the weight of each problem in metadata file "course_structure" and fix them based on course setting on Edx.

2. Building a new table named ```problem_structure``` by running the file ```ProblemStructure.py```

3. Running the SQL query to join three tables ```submissions```, ```assessments``` and ```problem_structure``` and select information of student submissions and grades we need.

    ```
    SELECT 
	    assessments.course_user_id as course_user_id, 
	    assessments.grade as grade, 
   	    assessments.max_grade as max_grade,
	    ps.weight as weight,
	    submissions.problem_id as problem_id,
	    ps.relevant_week as relevant_week,
	    submissions.submission_timestamp as submission_timestamp
    FROM 
	    FP101x_3T2015.assessments AS assessments
	    JOIN FP101x_3T2015.submissions AS submissions
	    ON assessments.assessment_id = submissions.submission_id
	    JOIN FP101x_3T2015.problem_structure AS ps
	    ON submissions.problem_id = ps.problem_id        
    WHERE # select all the pass user
	    assessments.course_user_id IN (
		    SELECT 
			    FP101x_3T2015.course_user.course_user_id 
		    FROM 
			    FP101x_3T2015.course_user
		    WHERE 
			    FP101x_3T2015.course_user.certificate_status <> "notpassing")
	    AND ps.weight > 0
	    AND assessments.grade > 0
        AND assessments.max_grade > 0
    ``` 

4. Exporting the new tables generated in Step 3 into csv files
    * if you run the SQL script on MySQL Workbench in Step 3, you also need to setting the limitation of the rows in results
    * If you run Step 3 in your codes or R/python environments, you may skip this step.

5. Run R script ```ProgressAggregation.r``` for the aggregration of student grade by their id and relevant weeks. (*can be writen in python later*)

6. Run R script ```ProgressPlot.r``` for plotting the number of passing students in each week based on the aggregration in Step 5. (*can be writen in python later*)





# 1. Database Building

## 1.1 Installing MySQL

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

8. Installing Connector/Python by ```sudo pip install mysql-connector-repackaged```
    * Checking if the package installed by using ```import mysql.connector``` 

## 1.2 Building the database

1. Create database ```<database name>```
    * Login MySQL ```mysql -uroot -p```
    * ```CREATE DATABASE <database name>``` For example ```CREATE DATABASE FP101x_3T2015```
    
2. Importing the dump structure of ```<database name>``` by using MySQL Workbench
    * Editting self-contained file ```moocdb.sql``` by changing the database name as ```<database name>```
    * Openning MySQL Workbench
    * Selecting Data Import in MANAGEMENT
    * Importing self-contained file ```moocdb.sql``` in Schema ```<database name>``` with Dump Structure Only

## 1.3 Reading course data into the the database

1. Changing the mode of MySQL to non-strict, otherwise ```null``` cannot be added into integer columns in some tables
    * mkdir ```mysql``` in folder ```/etc```
    * ```sudo vi etc/mysql/my.cnf```
    * Adding content into ```my.cnf```
    
    ```
    [mysqld]
    sql_mode=NO_ENGINE_SUBSTITUTION
    ```
    * Restarting MySQL Server
    
<!--2. Setting the folder
    * Root folder is named as the course name.
    * mkdir ```zip_files``` and ```unzip_files``` under the root folder
    * mkdir ```metadata``` under the folder ```unzip_files```, and put all the  files of metadata of the course into the folder ```metadata```
    * Put all the daily log files with ```.gz``` into ```zip_files```-->
    
2. Setting the folder
    * ```root``` folder is named as the course name.
    * Preprocessing daily log files:
        * Uncompressing all the daily log files (which in the course time)
        * Editting ```LogFileCleaning.py``` for filtering the daily log files
        * ```python LogFileCleaning.py``` generating preprocessed daily log files
        * Putting all preprocessed daily log files into ```root``` folder
    * Uncompressing all the metadata of the courses and putting them into ```root``` folder

3. Editting course folder path in ```main.py```
4. Editting database info in each ```.py``` files
5. Running the code by ```python main.py```

## 1.4 Others

These codes are test on EX101x-3T2015 and FP101x-3T2015.

# 2. Relations with The Moocdb Project

## 2.1 The Moocdb Project

[The MOOCdb Project](moocdb.csail.mit.edu) is an open source framework, which sets a shared data model standard for organzing data generated from MOOCs.

The initial schema of moocdb consists of four modules, which are Observing, Submitting, Collaborating and Feedback.

## 2.2 Our current schema

Our current schema mainly consists of four modules, which are named as Observations, Submissions, Collaborations and UserModes. 

![Alt](./MOOCdb_Data_Model.png "Title")

As shown in Figure 1, each module in our schema has several tables of information. The differences between our current schema and the initial moocdb schema are discussed in the following sections.

## 2.3 Observing

In original Moocdb schema, Observing mode has five tables, which are observed_event, resources, resources_urls, resources_types and urls. 

In our current schema, we merge them into two tables, named observations and resources. This two tables represent the observed events of students and relevant resouces to events.

## 2.4 Submitting

In original Moocdb schema, Submitting mode has four tables, which are problem_type, problems, submissions, and assessments. 

In our current schema, we merge the problem table into problems table. After that, a table named quiz_sessions is added. quiz_sessions is leveraged to represent how users answer sessions of quiz.

## 2.5 Collaborating

In original Moocdb schema, Collaborating mode has two tables, which are collaborations and collaboration_types. 

In our current schema, the two original table collaborations and collaboration_types are combined into one table collaborations. forum_sessions is added as a new table, which represents users activities on forum.

## 2.6 UserModes

In our schema, we have another parts named user modes. which contains four tables named courses, global_user, course_user and user_pii.

Table courses contains the metainfo of courses. Table global_user represent the relations between users and courses. Table course_user represent users' status and grade in courses. Table user_pii represent course users' demographic data. 




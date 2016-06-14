# 1. Installing MySQL

1. Downloading [MySQL Community Server](http://dev.mysql.com/downloads/mysql/)

2. Installing and recording the initial root password

3. Checking if MySQL installed in ```/usr/local/mysql/bin```

4. Setting PATH
    * Editting bash profile ```vim ~/.bash_profile```
    * Setting the path ```PATH=$PATH:/usr/local/mysql/bin```
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

# 2. Building the database

1. Create database ```<database name>```
    * Login MySQL ```mysql -uroot -p```
    * ```CREATE DATABASE <database name>``` For example ```CREATE DATABASE FP101x_3T2015```
    
2. Importing the dump structure of ```<database name>``` by using MySQL Workbench
    * Editting self-contained file ```moocdb.sql``` by changing the database name as ```<database name>```
    * Openning MySQL Workbench
    * Selecting Data Import in MANAGEMENT
    * Importing self-contained file ```moocdb.sql``` in Schema ```<database name>``` with Dump Structure Only

# 3. Reading course data into the the database

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

# Others

These codes are test on EX101x-3T2015 and FP101x-3T2015.

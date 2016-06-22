<<<<<<< HEAD
DROP SCHEMA IF EXISTS FP101x_3T2015;
CREATE SCHEMA FP101x_3T2015 CHARACTER SET `latin1`;

USE FP101x_3T2015;

DROP TABLE IF EXISTS `courses`;
CREATE TABLE `courses` (
course_id varchar(255) NOT NULL,
course_name varchar(255),
course_start_time datetime,
course_end_time datetime,
PRIMARY KEY (course_id),
INDEX `index` (`course_id`)
) ENGINE=MyISAM;

DROP TABLE IF EXISTS `user_pii`;
CREATE TABLE `user_pii` (
course_user_id varchar(255) NOT NULL,
gender varchar(255),
year_of_birth int,
level_of_education varchar(255),
country varchar(255),
email varchar(255),
PRIMARY KEY (course_user_id),
FOREIGN KEY (course_user_id) REFERENCES global_user(course_user_id),
INDEX `index` (`course_user_id`(50), `gender`, `year_of_birth`, `level_of_education`, `country`)
) ENGINE=MyISAM;

DROP TABLE IF EXISTS `global_user`;
CREATE TABLE `global_user` (
global_user_id int NOT NULL,
course_id varchar(255) NOT NULL,
course_user_id varchar(255) NOT NULL,
PRIMARY KEY (course_user_id),
FOREIGN KEY (course_id) REFERENCES courses(course_id),
FOREIGN KEY (global_user_id) REFERENCES user_pii(global_user_id),
INDEX `index` (`global_user_id`, `course_id`, `course_user_id`)
) ENGINE=MyISAM;

DROP TABLE IF EXISTS `course_user`;
CREATE TABLE `course_user` (
course_user_id varchar(255) NOT NULL,
final_grade FLOAT,
enrollment_mode varchar(255),
certificate_status varchar(255),
register_time datetime,
PRIMARY KEY (course_user_id),
FOREIGN KEY (course_user_id) REFERENCES global_user(course_user_id),
INDEX `index` (`course_user_id`, `enrollment_mode`, `certificate_status`)
) ENGINE=MyISAM;

DROP TABLE IF EXISTS `problems`;
CREATE TABLE `problems` (
problem_id varchar(255) NOT NULL,
problem_type varchar(255),
PRIMARY KEY (problem_id),
FOREIGN KEY (problem_id) REFERENCES resources(resource_id),
INDEX `index` (`problem_id`, `problem_type`)
) ENGINE=MyISAM;

DROP TABLE IF EXISTS `submissions`;
CREATE TABLE `submissions` (
submission_id varchar(255) NOT NULL,
course_user_id varchar(255) NOT NULL,
problem_id varchar(255) NOT NULL,
submission_timestamp datetime,
PRIMARY KEY (submission_id),
FOREIGN KEY (course_user_id) REFERENCES global_user(course_user_id),
FOREIGN KEY (problem_id) REFERENCES resources(resource_id),
INDEX `index` (`submission_id`, `course_user_id`, `problem_id`)
) ENGINE=MyISAM;

DROP TABLE IF EXISTS `assessments`;
CREATE TABLE `assessments` (
assessment_id varchar(255) NOT NULL,
course_user_id varchar(255),
max_grade float,
grade float,
PRIMARY KEY (assessment_id),
FOREIGN KEY (course_user_id) REFERENCES global_user(course_user_id),
FOREIGN KEY (assessment_id) REFERENCES submissions(submission_id),
INDEX `index` (`assessment_id`, `course_user_id`, `max_grade`, `grade`)
) ENGINE=MyISAM;



DROP TABLE IF EXISTS `observations`;
CREATE TABLE `observations` (
observation_id varchar(255) NOT NULL,
course_user_id varchar(255) NOT NULL,
resource_id varchar(255) NOT NULL,
observation_type varchar(255),
duration double,

times_forwardSeek int,
duration_forwardSeek double,
times_backwardSeek int,
duration_backwardSeek double,
times_speedUp int,
times_speedDown int,
times_pause int,
duration_pause double,
start_time datetime,
end_time datetime,

PRIMARY KEY (observation_id),
FOREIGN KEY (course_user_id) REFERENCES global_user(course_user_id),
FOREIGN KEY (resource_id) REFERENCES resources(resource_id),
INDEX `index` (`observation_id`(50), `course_user_id`(50), `resource_id`(50))

) ENGINE=MyISAM;

DROP TABLE IF EXISTS `resources`;
CREATE TABLE `resources` (
resource_id varchar(255) NOT NULL,
resource_type varchar(255),
relevant_week int,
course_id varchar(255),
PRIMARY KEY (resource_id),
FOREIGN KEY (course_id) REFERENCES courses(course_id),
INDEX `index` (`resource_id`, `resource_type`, `relevant_week`, `course_id`)
) ENGINE=MyISAM;



DROP TABLE IF EXISTS `collaborations`;
CREATE TABLE `collaborations` (
collaboration_id varchar(255) NOT NULL,
course_user_id varchar(255),
collaboration_type varchar(255),
collaboration_title text,
collaboration_content text,
collaboration_timestamp datetime,
collaboration_parent_id varchar(255),
collaboration_thread_id varchar(255),
PRIMARY KEY (collaboration_id),
FOREIGN KEY (course_user_id) REFERENCES global_user(course_user_id),
INDEX `index` (`collaboration_id`, `course_user_id`, `collaboration_type`)
) ENGINE=MyISAM;



DROP TABLE IF EXISTS `sessions`;
CREATE TABLE `sessions` (
session_id varchar(255) NOT NULL,
course_user_id varchar(255) NOT NULL,
start_time datetime,
end_time datetime,
duration int,
PRIMARY KEY (session_id),
FOREIGN KEY (course_user_id) REFERENCES global_user(course_user_id),
INDEX `index` (`session_id`, `course_user_id`)
) ENGINE=MyISAM;


DROP TABLE IF EXISTS `forum_sessions`;
CREATE TABLE `forum_sessions` (
forum_session_id varchar(255) NOT NULL,
course_user_id varchar(255) NOT NULL,
times_search int,
start_time datetime,
end_time datetime,
duration int,
PRIMARY KEY (forum_session_id),
FOREIGN KEY (course_user_id) REFERENCES global_user(course_user_id),
INDEX `index` (`forum_session_id`, `course_user_id`)
) ENGINE=MyISAM;


DROP TABLE IF EXISTS `quiz_sessions`;
CREATE TABLE `quiz_sessions` (
quiz_session_id varchar(255) NOT NULL,
course_user_id varchar(255) NOT NULL,
start_time datetime,
end_time datetime,
duration int,
PRIMARY KEY (quiz_session_id),
FOREIGN KEY (course_user_id) REFERENCES global_user(course_user_id),
INDEX `index` (`quiz_session_id`, `course_user_id`)
) ENGINE=MyISAM;


DROP TABLE IF EXISTS `survey_description`;
CREATE TABLE `survey_description` (
question_id varchar(255) NOT NULL,
course_id varchar(255),
question_type varchar(255),
description text,
PRIMARY KEY (question_id),
FOREIGN KEY (course_id) REFERENCES courses(course_id),
INDEX `index` (`question_id`, `course_id`, `question_type`)
) ENGINE=MyISAM;

DROP TABLE IF EXISTS `survey_response`;
CREATE TABLE survey_response (
response_id varchar(255) NOT NULL,
course_user_id varchar(255),
question_id varchar(255),
answer text,
PRIMARY KEY (response_id),
FOREIGN KEY (course_user_id) REFERENCES global_user(course_user_id),
INDEX `index` (`response_id`, `course_user_id`, `question_id`)
) ENGINE=MyISAM;
=======
DROP DATABASE IF EXISTS TEST;
CREATE DATABASE TEST;

USE TEST;

DROP TABLE IF EXISTS `courses`;
CREATE TABLE `courses` (
course_id varchar(255) NOT NULL,
course_name varchar(255),
course_start_time datetime,
course_end_time datetime,
PRIMARY KEY (course_id),
KEY `index` (`course_id`)
) ENGINE=MyISAM;

DROP TABLE IF EXISTS `user_pii`;
CREATE TABLE `user_pii` (
course_user_id varchar(255) NOT NULL,
gender varchar(255),
year_of_birth int,
level_of_education varchar(255),
country varchar(255),
email varchar(255),
PRIMARY KEY (course_user_id),
FOREIGN KEY (course_user_id) REFERENCES global_user(course_user_id),
KEY `index` (`course_user_id`(50), `gender`, `year_of_birth`, `level_of_education`, `country`)
) ENGINE=MyISAM;

DROP TABLE IF EXISTS `global_user`;
CREATE TABLE `global_user` (
global_user_id int NOT NULL,
course_id varchar(255) NOT NULL,
course_user_id varchar(255) NOT NULL,
PRIMARY KEY (course_user_id),
FOREIGN KEY (course_id) REFERENCES courses(course_id),
FOREIGN KEY (global_user_id) REFERENCES user_pii(global_user_id),
KEY `index` (`global_user_id`, `course_id`, `course_user_id`)
) ENGINE=MyISAM;

DROP TABLE IF EXISTS `course_user`;
CREATE TABLE `course_user` (
course_user_id varchar(255) NOT NULL,
final_grade FLOAT,
enrollment_mode varchar(255),
certificate_status varchar(255),
register_time datetime,
PRIMARY KEY (course_user_id),
FOREIGN KEY (course_user_id) REFERENCES global_user(course_user_id),
KEY `index` (`course_user_id`, `enrollment_mode`, `certificate_status`)
) ENGINE=MyISAM;

DROP TABLE IF EXISTS `problems`;
CREATE TABLE `problems` (
problem_id varchar(255) NOT NULL,
problem_type varchar(255),
PRIMARY KEY (problem_id),
FOREIGN KEY (problem_id) REFERENCES resources(resource_id),
KEY `index` (`problem_id`, `problem_type`)
) ENGINE=MyISAM;

DROP TABLE IF EXISTS `submissions`;
CREATE TABLE `submissions` (
submission_id varchar(255) NOT NULL,
course_user_id varchar(255) NOT NULL,
problem_id varchar(255) NOT NULL,
submission_timestamp datetime,
PRIMARY KEY (submission_id),
FOREIGN KEY (course_user_id) REFERENCES global_user(course_user_id),
FOREIGN KEY (problem_id) REFERENCES resources(resource_id),
KEY `index` (`submission_id`, `course_user_id`, `problem_id`)
) ENGINE=MyISAM;

DROP TABLE IF EXISTS `assessments`;
CREATE TABLE `assessments` (
assessment_id varchar(255) NOT NULL,
course_user_id varchar(255),
max_grade float,
grade float,
PRIMARY KEY (assessment_id),
FOREIGN KEY (course_user_id) REFERENCES global_user(course_user_id),
FOREIGN KEY (assessment_id) REFERENCES submissions(submission_id),
KEY `index` (`assessment_id`, `course_user_id`, `max_grade`, `grade`)
) ENGINE=MyISAM;



DROP TABLE IF EXISTS `observations`;
CREATE TABLE `observations` (
observation_id varchar(255) NOT NULL,
course_user_id varchar(255) NOT NULL,
resource_id varchar(255) NOT NULL,
observation_type varchar(255),
duration double,

times_forwardSeek int,
duration_forwardSeek double,
times_backwardSeek int,
duration_backwardSeek double,
times_speedUp int,
times_speedDown int,
times_pause int,
duration_pause double,

start_time datetime,
end_time datetime,

PRIMARY KEY (observation_id),
FOREIGN KEY (course_user_id) REFERENCES global_user(course_user_id),
FOREIGN KEY (resource_id) REFERENCES resources(resource_id),

KEY `index` (`observation_id`(50), `course_user_id`(50), `resource_id`(50))

) ENGINE=MyISAM;

DROP TABLE IF EXISTS `resources`;
CREATE TABLE `resources` (
resource_id varchar(255) NOT NULL,
resource_type varchar(255),
relevant_week int,
course_id varchar(255),
PRIMARY KEY (resource_id),
FOREIGN KEY (course_id) REFERENCES courses(course_id),
KEY `index` (`resource_id`, `resource_type`, `relevant_week`, `course_id`)
) ENGINE=MyISAM;



DROP TABLE IF EXISTS `collaborations`;
CREATE TABLE `collaborations` (
collaboration_id varchar(255) NOT NULL,
course_user_id varchar(255),
collaboration_type varchar(255),
collaboration_title text,
collaboration_content text,
collaboration_timestamp datetime,
collaboration_parent_id varchar(255),
collaboration_thread_id varchar(255),
PRIMARY KEY (collaboration_id),
FOREIGN KEY (course_user_id) REFERENCES global_user(course_user_id),
KEY `index` (`collaboration_id`, `course_user_id`, `collaboration_type`)
) ENGINE=MyISAM;



DROP TABLE IF EXISTS `sessions`;
CREATE TABLE `sessions` (
session_id varchar(255) NOT NULL,
course_user_id varchar(255) NOT NULL,
start_time datetime,
end_time datetime,
duration int,
PRIMARY KEY (session_id),
FOREIGN KEY (course_user_id) REFERENCES global_user(course_user_id),
KEY `index` (`session_id`, `course_user_id`)
) ENGINE=MyISAM;


DROP TABLE IF EXISTS `forum_sessions`;
CREATE TABLE `forum_sessions` (
forum_session_id varchar(255) NOT NULL,
course_user_id varchar(255) NOT NULL,
times_search int,
start_time datetime,
end_time datetime,
duration int,
PRIMARY KEY (forum_session_id),
FOREIGN KEY (course_user_id) REFERENCES global_user(course_user_id),
KEY `index` (`forum_session_id`, `course_user_id`)
) ENGINE=MyISAM;


DROP TABLE IF EXISTS `quiz_sessions`;
CREATE TABLE `quiz_sessions` (
quiz_session_id varchar(255) NOT NULL,
course_user_id varchar(255) NOT NULL,
start_time datetime,
end_time datetime,
duration int,
PRIMARY KEY (quiz_session_id),
FOREIGN KEY (course_user_id) REFERENCES global_user(course_user_id),
KEY `index` (`quiz_session_id`, `course_user_id`)
) ENGINE=MyISAM;


DROP TABLE IF EXISTS `survey_description`;
CREATE TABLE `survey_description` (
question_id varchar(255) NOT NULL,
course_id varchar(255),
question_type varchar(255),
description text,
PRIMARY KEY (question_id),
FOREIGN KEY (course_id) REFERENCES courses(course_id),
KEY `index` (`question_id`, `course_id`, `question_type`)
) ENGINE=MyISAM;

DROP TABLE IF EXISTS `survey_response`;
CREATE TABLE survey_response (
response_id varchar(255) NOT NULL,
course_user_id varchar(255),
question_id varchar(255),
answer text,
PRIMARY KEY (response_id),
FOREIGN KEY (course_user_id) REFERENCES global_user(course_user_id),
KEY `index` (`response_id`, `course_user_id`, `question_id`)
) ENGINE=MyISAM;

>>>>>>> e82ce82cf252980d1c89e03fc9f4dfb11b7eaa37

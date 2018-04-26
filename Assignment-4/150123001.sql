create database 09feb2018;
use 09feb2018;

create table Course(
	course_id VARCHAR(10) NOT NULL,
	division ENUM('I','II','III','IV','NA') default 'NA',
	CONSTRAINT course_key PRIMARY KEY(course_id,division)
	);

create table Room(
	room_number VARCHAR(10) NOT NULL,
	location ENUM('Core-I', 'Core-II', 'Core-III', 'Core-IV', 'LH', 'Local') NOT NULL,
	CONSTRAINT room_key PRIMARY KEY(room_number)
	);

create table Slot(
	letter ENUM('A','B','C','D','E','F','G','H','I','J','K','L','A1','B1','C1','D1','E1') NOT NULL,
	day ENUM('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday') NOT NULL,
	start_time TIME NOT NULL,
	end_time TIME NOT NULL,
	CONSTRAINT slot_key PRIMARY KEY(letter,day)
	);

create table Department(
	department_id ENUM('BSBE','CE','CH','CL','CRT','CS','EEE','HSS','MA','ME','PH') NOT NULL,
	name VARCHAR(100) NOT NULL,
	CONSTRAINT department_key PRIMARY KEY(department_id)
	);

-- All the primary keys in various tables have to be together composite primary key for ScheduledIn as 
-- without even one of them an entry can't be figured out correctly
-- although department_id can be removed from primary_key as it's not necessary to distinguish entries
-- but for handling future database problems, I have kept it as primary key.
create table ScheduledIn(
	department_id ENUM('BSBE','CE','CH','CL','CRT','CS','EEE','HSS','MA','ME','PH') NOT NULL,
	course_id VARCHAR(10) NOT NULL,
	division ENUM('I','II','III','IV','NA') DEFAULT 'NA',
	letter ENUM('A','B','C','D','E','F','G','H','I','J','K','L','A1','B1','C1','D1','E1') NOT NULL,
	room_number VARCHAR(10) NOT NULL,
	day ENUM('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday') NOT NULL,
	CONSTRAINT scheduledin_key PRIMARY KEY(department_id,course_id,division,letter,room_number,day),
	FOREIGN KEY (department_id) REFERENCES Department(department_id),
	FOREIGN KEY (course_id,division) REFERENCES Course(course_id,division),
	FOREIGN KEY (letter,day) REFERENCES Slot(letter,day),
	FOREIGN KEY (room_number) REFERENCES Room(room_number)
	);


/*
LOAD DATA LOCAL INFILE  '/media/abhinav/00BC77C1BC77B030/IIT-Guwahati/Mathematics/ds-lab/9Feb-db_lab/150123001_room.csv' 
INTO TABLE Room FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n';
LOAD DATA LOCAL INFILE  '/media/abhinav/00BC77C1BC77B030/IIT-Guwahati/Mathematics/ds-lab/9Feb-db_lab/150123001_course.csv' 
INTO TABLE Course FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n';
LOAD DATA LOCAL INFILE  '/media/abhinav/00BC77C1BC77B030/IIT-Guwahati/Mathematics/ds-lab/9Feb-db_lab/150123001_department.csv' 
INTO TABLE Department FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n';
LOAD DATA LOCAL INFILE  '/media/abhinav/00BC77C1BC77B030/IIT-Guwahati/Mathematics/ds-lab/9Feb-db_lab/150123001_slot.csv' 
INTO TABLE Slot FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\r\n';
LOAD DATA LOCAL INFILE  '/media/abhinav/00BC77C1BC77B030/IIT-Guwahati/Mathematics/ds-lab/9Feb-db_lab/150123001_scheduledin.csv' 
INTO TABLE ScheduledIn FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'
(department_id,course_id,division,letter,room_number,day);
*/
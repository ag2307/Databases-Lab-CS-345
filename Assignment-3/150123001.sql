create database 25jan2018;
use 25jan2018;
-- id and exam_date together need to be primary key
-- id in cc table should be unique for single course
-- email can be null also
create table ett(id VARCHAR(10) NOT NULL,exam_date DATE NOT NULL,start_time TIME NOT NULL,end_time TIME NOT NULL,PRIMARY KEY(id,exam_date));
create table cc(id VARCHAR(10) NOT NULL UNIQUE,credits INT NOT NULL,PRIMARY KEY(id));
create table cwsl(id VARCHAR(10) NOT NULL,sr INT,roll VARCHAR(15) NOT NULL,name VARCHAR(40) NOT NULL,email VARCHAR(50),PRIMARY KEY(id,roll));

create temporary table ett_temp(id VARCHAR(10) NOT NULL,exam_date DATE NOT NULL,start_time TIME NOT NULL,end_time TIME NOT NULL,PRIMARY KEY(id,exam_date));
create temporary table cc_temp(id VARCHAR(10) NOT NULL UNIQUE,credits INT NOT NULL,PRIMARY KEY(id));
create temporary table cwsl_temp(id VARCHAR(10) NOT NULL,sr INT,roll VARCHAR(15) NOT NULL,name VARCHAR(40) NOT NULL,email VARCHAR(50),PRIMARY KEY(id,roll));

create table ett_clone LIKE ett;	
create table cc_clone LIKE cc;
create table cwsl_clone LIKE cwsl;


SET NAMES utf8mb4;
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

DROP SCHEMA IF EXISTS wrattel;

CREATE SCHEMA wrattel
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE wrattel;


CREATE TABLE person (
id INT PRIMARY KEY AUTO_INCREMENT,
fname VARCHAR(50) NOT NULL,
lname VARCHAR(50) NOT NULL,
year_of_study SMALLINT UNSIGNED CHECK(year_of_study IN(1,2,3,4,5)),
contact_number VARCHAR(12),
join_date DATE,
email VARCHAR(50),
address VARCHAR(75)
);

CREATE TABLE level (
id INT PRIMARY KEY,
name VARCHAR(10) NOT NULL CHECK (name IN('تلاوة', 'غيبي', 'انتقالي', 'اجازة')),
description VARCHAR(150) NOT NULL,
plan VARCHAR(150) NOT NULL
);

CREATE TABLE student(
id INT PRIMARY KEY,
status VARCHAR(10) NOT NULL CHECK(status IN ('نشط', 'منقطع', 'متخرج')),
CONSTRAINT student_person_fk FOREIGN KEY(id) REFERENCES person(id)
);

CREATE TABLE student_level(
id INT PRIMARY KEY AUTO_INCREMENT,
level_id INT NOT NULL,
student_id INT NOT NULL,
reached_at DATE NOT NULL,
CONSTRAINT student_level_student_fk FOREIGN KEY(student_id) REFERENCES student(id),
CONSTRAINT student_level_level_fk FOREIGN KEY(level_id) REFERENCES level(id)
);

CREATE TABLE supervisor(
id INT PRIMARY KEY,
role VARCHAR(20) CHECK(role IN('مسمع','مساعد', 'مشرف')) NOT NULL,
became_supervisor_at DATE NOT NULL,
retired_at DATE,
assistant_id INT,
CONSTRAINT supervisor_person_fk FOREIGN KEY(id) REFERENCES person(id)
);

ALTER TABLE supervisor
ADD CONSTRAINT supervisor_assistant_fk FOREIGN KEY(assistant_id) REFERENCES supervisor(id),
ADD CONSTRAINT suprevisor_assistant_not_equal CHECK(assistant_id <> id);


CREATE TABLE student_supervisor(
id INT PRIMARY KEY AUTO_INCREMENT,
student_id INT NOT NULL,
supervisor_id INT NOT NULL,
assigned_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
retired_at DATE,
CONSTRAINT student_supervisor_student_fk FOREIGN KEY(student_id) REFERENCES student(id),
CONSTRAINT supervisor_student_supervisor_fk FOREIGN KEY(supervisor_id) REFERENCES supervisor(id),
CONSTRAINT student_supervisor_student_not_equal_supervisor CHECK (student_id <> supervisor_id)
);

CREATE TABLE achievement(
id INT PRIMARY KEY AUTO_INCREMENT,
num_of_parts SMALLINT UNSIGNED CHECK(num_of_parts BETWEEN 1 AND 30),
type_of_achievement VARCHAR(10) NOT NULL CHECK(type_of_achievement IN ('تلاوة', 'غيبي','اجازة')),
date_aquired DATE NOT NULL,
person_id INT NOT NULL,
CONSTRAINT achievement_person_fk FOREIGN KEY(person_id) REFERENCES person(id)
);

CREATE TABLE report(
id INT PRIMARY KEY AUTO_INCREMENT,
student_supervisor_id INT NOT NULL,
student_level_id INT NOT NULL,
start_page SMALLINT UNSIGNED NOT NULL,
qty SMALLINT UNSIGNED NOT NULL,
report_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
CONSTRAINT report_student_supervisor_id FOREIGN KEY(student_supervisor_id) REFERENCES student_supervisor(id),
CONSTRAINT report_student_level_id FOREIGN KEY(student_level_id) REFERENCES student_level(id)
);

CREATE TABLE error (
id INT PRIMARY KEY AUTO_INCREMENT,
error_type VARCHAR(15) CHECK (error_type IN ( 'تشكيلي' , 'حفظي' , 'تجويدي' )),
score SMALLINT
);

CREATE TABLE report_error (
id INT PRIMARY KEY AUTO_INCREMENT,
report_id INT NOT NULL,
error_id INT NOT NULL,
details VARCHAR(50) NOT NULL,
error_word VARCHAR(30) NOT NULL,
CONSTRAINT report_error_report_fk FOREIGN KEY(report_id) REFERENCES report(id),
CONSTRAINT report_error_error_fk FOREIGN KEY(error_id) REFERENCES error(id)
);

CREATE TABLE exam (
id INT PRIMARY KEY AUTO_INCREMENT,
student_id INT NOT NULL,
supervisor_id INT NOT NULL,
student_level_id INT NOT NULL,
exam_type VARCHAR(15) CHECK (exam_type IN ('انتقالي' , 'مرحلي')),
part SMALLINT UNSIGNED CHECK(part BETWEEN 1 AND 30),
qty SMALLINT UNSIGNED CHECK(qty BETWEEN 1 AND 30),
exam_date DATE,
CONSTRAINT exam_student_fk FOREIGN KEY(student_id) REFERENCES student(id),
CONSTRAINT exam_supervisor_fk FOREIGN KEY(supervisor_id) REFERENCES supervisor(id),
CONSTRAINT exam_student_not_equal_supervisor CHECK (student_id <> supervisor_id),
CONSTRAINT exam_student_level_fk FOREIGN KEY(student_level_id) REFERENCES student_level(id)
);

CREATE TABLE exam_error (
id INT PRIMARY KEY AUTO_INCREMENT,
error_id INT NOT NULL,
exam_id INT NOT NULL,
details VARCHAR(50) NOT NULL,
error_word VARCHAR(30) NOT NULL,
CONSTRAINT exam_error_error_fk FOREIGN KEY(error_id) REFERENCES error(id),
CONSTRAINT exam_error_exam_fk FOREIGN KEY(exam_id) REFERENCES exam(id)
);



CREATE TABLE activity_type(
id INT PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(25) NOT NULL
);

CREATE TABLE activity(
id INT PRIMARY KEY AUTO_INCREMENT,
title varchar(100),
activity_type_id INT NOT NULL,
coordinator_id INT NOT NULL,
presenter_id INT NOT NULL,
activity_date TIMESTAMP NOT NULL,
CONSTRAINT activity_coordinator_fk FOREIGN KEY(coordinator_id) REFERENCES supervisor(id),
CONSTRAINT activity_activity_type_fk FOREIGN KEY(activity_type_id) REFERENCES activity_type(id),
CONSTRAINT activity_presenter_fk FOREIGN KEY (presenter_id) REFERENCES supervisor(id)
);

create table activity_student (
id INT PRIMARY KEY AUTO_INCREMENT,
activity_id INT NOT NULL,
student_id INT NOT NULL,
CONSTRAINT activity_student_student_fk FOREIGN KEY(student_id) REFERENCES student(id),
CONSTRAINT activity_student_activity_fk FOREIGN KEY(activity_id) REFERENCES activity(id)
);

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;


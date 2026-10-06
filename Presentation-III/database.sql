CREATE DATABASE IF NOT EXISTS examination_db;

USE examination_db;

CREATE TABLE STUDENT (
    Student_ID INT PRIMARY KEY,
    Name VARCHAR(100),
    Branch VARCHAR(100),
    Semester INT
);

CREATE TABLE COURSE (
    Course_ID INT PRIMARY KEY,
    Course_Name VARCHAR(100),
    Credits INT
);

CREATE TABLE EXAMINATION (
    Exam_ID INT PRIMARY KEY,
    Course_ID INT,
    Exam_Date DATE,
    FOREIGN KEY (Course_ID) REFERENCES COURSE(Course_ID)
);

CREATE TABLE FACULTY (
    Faculty_ID INT PRIMARY KEY,
    Faculty_Name VARCHAR(100)
);

CREATE TABLE EXAM_HALL (
    Hall_ID INT PRIMARY KEY,
    Hall_Name VARCHAR(100),
    Capacity INT
);

CREATE TABLE MARKS (
    Marks_ID INT PRIMARY KEY,
    Student_ID INT,
    Exam_ID INT,
    Marks_Obtained INT,
    FOREIGN KEY (Student_ID) REFERENCES STUDENT(Student_ID),
    FOREIGN KEY (Exam_ID) REFERENCES EXAMINATION(Exam_ID)
);

CREATE TABLE RESULT (
    Result_ID INT PRIMARY KEY,
    Student_ID INT,
    Course_ID INT,
    Grade VARCHAR(10),
    Status VARCHAR(20),
    FOREIGN KEY (Student_ID) REFERENCES STUDENT(Student_ID),
    FOREIGN KEY (Course_ID) REFERENCES COURSE(Course_ID)
);

CREATE TABLE EXAM_INVIGILATOR (
    Exam_ID INT,
    Faculty_ID INT,
    PRIMARY KEY (Exam_ID, Faculty_ID),
    FOREIGN KEY (Exam_ID) REFERENCES EXAMINATION(Exam_ID),
    FOREIGN KEY (Faculty_ID) REFERENCES FACULTY(Faculty_ID)
);

CREATE TABLE HALL_ALLOCATION (
    Exam_ID INT,
    Hall_ID INT,
    PRIMARY KEY (Exam_ID, Hall_ID),
    FOREIGN KEY (Exam_ID) REFERENCES EXAMINATION(Exam_ID),
    FOREIGN KEY (Hall_ID) REFERENCES EXAM_HALL(Hall_ID)
);
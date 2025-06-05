CREATE DATABASE university;
use university;

-- Étudiants
CREATE TABLE students (
    student_id VARCHAR(20) PRIMARY KEY,
    full_name VARCHAR(100),
    birth_date DATE,
    email VARCHAR(100),
    nationality VARCHAR(50)
);

-- Filières (majors)
CREATE TABLE majors (
    major_code VARCHAR(10) PRIMARY KEY,
    major_name VARCHAR(100)
);

-- Inscriptions
CREATE TABLE enrollments (
    enrollment_id INT PRIMARY KEY AUTO_INCREMENT,
    student_id VARCHAR(20),
    major_code VARCHAR(10),
    registration_date DATE,
    status ENUM('active', 'cancelled', 'pending'),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (major_code) REFERENCES majors(major_code)
);

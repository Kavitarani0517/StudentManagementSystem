

CREATE DATABASE student_db;

USE student_db;

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20),
    course VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO students (name, email, phone, course)
VALUES
('Ananya Sharma', 'ananya@example.com', '9876543210', 'BCA'),
('Rahul Kumar', 'rahul@example.com', '9876501234', 'BSc Computer Science');

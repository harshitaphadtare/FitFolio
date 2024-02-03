CREATE DATABASE fitfolio;
USE fitfolio;

-- USER TABLE 
CREATE TABLE users(
	id INT PRIMARY KEY AUTO_INCREMENT,
	username VARCHAR(50) UNIQUE,
    fullname VARCHAR(100),
    dob TEXT,
    password VARCHAR(500),
    gender VARCHAR(20)
); 

-- CARDIO TABLE 
CREATE TABLE cardio(
	username VARCHAR(20),
    distance FLOAT,
    date TEXT,
    time FLOAT,
    calories FLOAT,
    weight FLOAT
);
ALTER TABLE cardio
ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY;

INSERT INTO cardio (username, date, distance, time, calories, weight)
VALUES
('harshita123', '2024-01-25', 3.5, 30, 150, 60),
('harshita123', '2024-01-26', 4.2, 40, 180, 65),
('harshita123', '2024-01-27', 2.8, 25, 120, 55),
('harshita123', '2024-01-28', 5.0, 45, 200, 70),
('harshita123', '2024-01-29', 3.0, 35, 160, 58),
('harshita123', '2024-01-30', 4.5, 40, 190, 68),
('harshita123', '2024-01-31', 3.2, 28, 140, 62),
('harshita123', '2024-02-01', 4.0, 38, 170, 63),
('harshita123', '2024-02-02', 2.5, 20, 110, 50),
('harshita123', '2024-02-03', 5.5, 50, 220, 75),
('harshita123', '2024-02-04', 3.8, 35, 180, 66),
('harshita123', '2024-02-05', 4.3, 42, 200, 70),
('harshita123', '2024-02-06', 2.0, 18, 100, 48),
('harshita123', '2024-02-07', 4.8, 44, 210, 72),
('harshita123', '2024-02-08', 3.6, 32, 160, 59),
('harshita123', '2024-02-09', 5.2, 48, 230, 78),
('harshita123', '2024-02-10', 3.4, 30, 150, 65),
('harshita123', '2024-02-11', 4.1, 37, 180, 70),
('harshita123', '2024-02-12', 2.7, 25, 130, 55),
('harshita123', '2024-02-13', 4.6, 42, 200, 68);

-- CYCLING TABLE
CREATE TABLE cycling(
	username VARCHAR(20),
    distance FLOAT,
    date TEXT,
    time FLOAT,
    calories FLOAT,
    weight FLOAT
);

ALTER TABLE cycling
ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY;

CREATE TABLE mindfulness(
	id INT AUTO_INCREMENT PRIMARY KEY,
	username VARCHAR(20),
    date TEXT,
    time FLOAT,
    activity TEXT 
);

CREATE TABLE sleep(
	id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(20),
    bed_in TEXT,
    bed_out TEXT,
    total_hrs TEXT,
    date TEXT
);

CREATE TABLE bmi(
	id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(20),
    height FLOAT,
    weight FLOAT,
    bmi FLOAT,
    status TEXT,
    date TEXT
);

SELECT * FROM bmi;

SELECT * FROM sleep;

SELECT * FROM mindfulness;

SELECT * FROM cycling;

SELECT * FROM users;

SELECT * FROM cardio;

DROP DATABASE fitfolio;

DROP TABLE sleep;
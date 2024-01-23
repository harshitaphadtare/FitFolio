CREATE DATABASE fitfolio;
USE fitfolio;

-- USER TABLE 
CREATE TABLE users(
	id INT PRIMARY KEY auto_increment,
    fullname VARCHAR(100),
    dob TEXT,
    username VARCHAR(20) UNIQUE,
    password VARCHAR(500),
    gender VARCHAR(20)
);

-- CARDIO TABLE 
CREATE TABLE cardio(
	user_id INT,
    date TEXT,
    distance FLOAT,
    time FLOAT,
    calories FLOAT,
    FOREIGN KEY (user_id) REFERENCES users(id)
)

SELECT * FROM users;

DROP DATABASE fitfolio;


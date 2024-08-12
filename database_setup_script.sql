CREATE DATABASE fitness_center;
USE fitness_center;

CREATE TABLE Members (
    id INT AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE WorkoutSessions (
    session_id INT AUTO_INCREMENT,
    member_id INT,
    session_date DATE,
    session_time VARCHAR(50),
    activity VARCHAR(255),
    PRIMARY KEY (session_id),
    FOREIGN KEY (member_id) REFERENCES Members(id)
);

SELECT * FROM WorkoutSessions;

SELECT * FROM Members;
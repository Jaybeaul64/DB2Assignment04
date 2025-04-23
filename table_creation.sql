CREATE DATABASE IF NOT EXISTS task_db;

CREATE TABLE IF NOT EXISTS task_db.Tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    description VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS task_db.Task_audit (
    audit_id INT AUTO_INCREMENT PRIMARY KEY,
    task_id INT, -- I did not set it up to be a foreign key because the task may not exist anymore.
    description VARCHAR(255) NOT NULL,
    old_description VARCHAR(255),
    user_action VARCHAR(255) NOT NULL,
    user VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
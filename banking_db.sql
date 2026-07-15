DROP DATABASE IF EXISTS banking_db;

CREATE DATABASE banking_db;

USE banking_db;

CREATE TABLE accounts (
    account_no INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    mobile VARCHAR(15) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    balance DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Seed data (password '1234' hashed with SHA-256)

INSERT INTO accounts
(name, age, mobile, password, balance)
VALUES
('Harshit Sharma',22,'9876543210','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4',10000.00);

INSERT INTO accounts
(name, age, mobile, password, balance)
VALUES
('Rahul',24,'9876501234','03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4',5000.00);



SELECT * FROM accounts;
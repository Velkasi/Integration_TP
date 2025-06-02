CREATE DATABASE integration_test;
USE integration_test;

CREATE TABLE customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    birthdate DATE,
    total_amount DECIMAL(5,2),
    enabled BOOLEAN
);

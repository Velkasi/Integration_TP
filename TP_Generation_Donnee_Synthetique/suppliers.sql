CREATE DATABASE supplier_integration_test;
USE supplier_integration_test;

CREATE TABLE suppliers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_name VARCHAR(100),
    contact_email VARCHAR(100),
    registration_date DATETIME,
    country VARCHAR(100),
    reputation_score INT,
    is_active BOOLEAN
);
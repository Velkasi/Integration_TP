CREATE DATABASE IF NOT EXISTS company_db;
USE company_db;

CREATE TABLE IF NOT EXISTS employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR (100),
    email VARCHAR (100),
    date_recrut DATETIME,
    salaire_annuel DECIMAL(10,2),
    salarie_active BOOLEAN
);

DROP TABLE IF EXISTS employees;
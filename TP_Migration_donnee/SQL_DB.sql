CREATE DATABASE company_db;
USE company_db

CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR (100),
    date_recrut DATETIME,
    salaire_annuel DECIMAL(10,3)
    );
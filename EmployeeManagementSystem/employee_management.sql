CREATE DATABASE employee_management;
USE employee_management;
CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(100),
    lastname VARCHAR(100),
    gender VARCHAR(10),
    age INT,
    address VARCHAR(255),
    contact VARCHAR(20),
    department VARCHAR(100),
    employment_date DATE,
    nationality VARCHAR(100),
    marital_status VARCHAR(20)
);

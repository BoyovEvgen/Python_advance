CREATE DATABASE employees;
USE employees;

CREATE TABLE departaments (departament_id INT AUTO_INCREMENT PRIMARY KEY, departament_name VARCHAR(100) NOT NULL, manager_id INT NOT NULL, location_id INT NOT NULL);

SHOW COLUMNS IN departaments;

CREATE TABLE jobs (job_id INT AUTO_INCREMENT PRIMARY KEY, job_title VARCHAR(100) NOT NULL, min_salary DECIMAL(10,2) UNSIGNED NOT NULL, max_salar DECIMAL(10,2) UNSIGNED NOT NULL);

SHOW COLUMNS IN jobs;

ALTER TABLE departaments RENAME departments
ALTER TABLE departments RENAME COLUMN departament_id TO department_id;
ALTER TABLE departments RENAME COLUMN departament_name TO department_name;
SHOW COLUMNS IN departments;


CREATE TABLE job_history(employee_id INT NOT NULL, start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, end_date TIMESTAMP, job_id INT NOT NULL, department_id INT NOT NULL, FOREIGN KEY (job_id) REFERENCES jobs(job_id), FOREIGN KEY (department_id) REFERENCES departments(department_id));

SHOW COLUMNS IN job_history;

CREATE TABLE regions (region_id INT AUTO_INCREMENT PRIMARY KEY, region_name VARCHAR(40) NOT NULL);

CREATE TABLE countries (country_id INT NOT NULL, counry_name VARCHAR(100) NOT NULL, region_id INT NOT NULL, FOREIGN KEY (region_id) REFERENCES regions(region_id));

ALTER TABLE countries MODIFY country_id INT NOT NULL PRIMARY KEY;


CREATE TABLE locations (location_id INT AUTO_INCREMENT PRIMARY KEY, street_address VARCHAR(50) NOT NULL, postal_code INT NOT NULL, city VARCHAR(50) NOT NULL, state_province VARCHAR(50), country_id INT NOT NULL, FOREIGN KEY(country_id) REFERENCES countries(country_id));

ALTER TABLE departments ADD FOREIGN KEY (location_id) REFERENCES locations(location_id);

CREATE TABLE employees (employee_id INT AUTO_INCREMENT PRIMARY KEY, first_name VARCHAR(50) NOT NULL, last_name VARCHAR(50) NOT NULL, email VARCHAR(50) NOT NULL, phone_number TINYINT
 NOT NULL, hire_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, job_id INT NOT NULL, salary DECIMAL(10,2) UNSIGNED NOT NULL, comission_pct TINYINT, manager_id INT, department_id INT NOT NULL, FOREIGN KEY (manager_id) REFERENCES employees (employee_id), FOREIGN KEY (department_id) REFERENCES departments(department_id)   );
 
 ALTER TABLE departments MODIFY manager_id INT;
 ALTER TABLE departments ADD FOREIGN KEY (manager_id) REFERENCES employees(employee_id);
 ALTER TABLE job_history ADD FOREIGN KEY (employee_id) REFERENCES employees(employee_id);
 ALTER TABLE employees ADD FOREIGN KEY (job_id) REFERENCES jobs(job_id);
 ALTER TABLE countries RENAME COLUMN counry_name TO country_name;
 ALTER TABLE jobs RENAME COLUMN max_salar TO max_salary;
 ALTER TABLE employees MODIFY phone_number VARCHAR(15) NOT NULL UNIQUE;
 ALTER TABLE employees MODIFY email VARCHAR(50) NOT NULL UNIQUE;





mysqldump -u root -<pass> <nameDB > <path/name_file>.sql





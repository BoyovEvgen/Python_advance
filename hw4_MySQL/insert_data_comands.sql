INSERT INTO regions (region_name) VALUES ('Europe'), ('Asia'), ('North'), ('America');

INSERT INTO countries (country_id, country_name, region_id) VALUES (380, 'Ukraine', 1), (30, 'Grece', 1), (81, 'Japan', 2), (1, 'USA', 4);

INSERT INTO locations (street_address, postal_code, city, state_province, country_id) VALUES
 ('bulevard Peremohi', 49106, 'Dnipro', 'Dnipropetrovska', 1);

INSERT INTO departments (department_id, department_name, location_id) VALUES (20, 'coffee brewers', 1), (30, 'management', 1), (50, 'developers', 1), (80, 'sales', 1);

INSERT INTO jobs (job_title, min_salary, max_salary) VALUES ('junior coffee maker', 5000, 15000), ('midle coffee maker', 15000, 25000), ('team lider', 5000, 6000), ('developer', 2000, 5000),
('salespeerson', 1000, 5000);

INSERT INTO employees (first_name, last_name, email, phone_number, hire_date, job_id, salary, comission_pct, department_id) VALUES ('Evhen', 'Boiov', 'qwe@qwe.qwe', 789456123, '22-11-1', 4, 4000, 35, 50);

INSERT INTO employees (first_name, last_name, email, phone_number, hire_date, job_id, salary, comission_pct, department_id) VALUES ('Tony', 'Robinson', 'asd@asd.asd', 789456165, '2008-11-1', 4, 8000, 0, 20);




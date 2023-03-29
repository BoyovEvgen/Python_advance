

SELECT * FROM employees;

SELECT * FROM employees WHERE first_name LIKE 'David';

SELECT * FROM employees WHERE departmment_id IN (20, 30);

SELECT * FROM employees WHERE departmment_id IN (50, 80) AND commission_pct NOT NULL;

SELECT first_name, last_name FROM employees  WHERE DAY(hire_date) = 1;

SELECT first_name, last_name FROM employees  WHERE YEAR(hire_date) = 2008;

SELECT DATE_FORMAT(CURDATE() + INTERVAL 1 DAY,'Tomorrow is %D of %M') FROM DUAL;

SElECT first_name, last_name, DATE_FORMAT(hire_date, '%D of %M, %Y') FROM employees;

SElECT first_name, last_name, CONCAT(comission_pct, '%') FROM employees WHERE comission_pct
= 20;

SElECT first_name, last_name FROM employees WHERE hire_date BETWEEN '2007/02/01' AND '2007/03/01';

SELECT NOW(), NOW() + INTERVAL 1 SECOND, NOW() + INTERVAL 1 MINUTE, NOW() + INTERVAL 1 HOUR, NOW() + INTERVAL 1 DAY, NOW() + INTERVAL 1 MONTH, NOW() + INTERVAL 1 YEAR FROM DUAL;


SElECT first_name, last_name, CONCAT('$', salary + salary/100*comission_pct) AS full_salary
FROM employees;

SElECT first_name, last_name, CONCAT('$', FORMAT(salary + salary/100*comission_pct, 'c')) AS full_salary FROM employees;

SElECT first_name, last_name, CASE comission_pct WHEN NULL THEN 'no' WHEN 0 THEN 'no' ELSE 'yes' END AS bonus  FROM employees;



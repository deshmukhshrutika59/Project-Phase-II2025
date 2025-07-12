def get_company_schema():
    return {
        "department": {
            "dept_id": {"type": "int", "primary_key": True},
            "dept_name": {"type": "varchar", "unique": True},
            "location": {"type": "varchar"},
            "sample_data": [
                {"dept_id": 1, "dept_name": "Human Resources", "location": "Delhi"},
                {"dept_id": 2, "dept_name": "Information Technology", "location": "Bengaluru"},
                {"dept_id": 3, "dept_name": "Sales", "location": "Mumbai"},
                {"dept_id": 4, "dept_name": "Marketing", "location": "Pune"},
                {"dept_id": 5, "dept_name": "Finance", "location": "Hyderabad"},
                {"dept_id": 6, "dept_name": "Legal", "location": "Kolkata"},
                {"dept_id": 7, "dept_name": "Research and Development", "location": "Chennai"},
                {"dept_id": 8, "dept_name": "Customer Support", "location": "Jaipur"},
                {"dept_id": 9, "dept_name": "Procurement", "location": "Bhopal"},
                {"dept_id": 10, "dept_name": "Logistics", "location": "Ludhiana"},
                {"dept_id": 11, "dept_name": "Administration", "location": "Ahmedabad"},
                {"dept_id": 12, "dept_name": "Security", "location": "Guwahati"},
                {"dept_id": 13, "dept_name": "Training", "location": "Lucknow"},
                {"dept_id": 14, "dept_name": "Operations", "location": "Raipur"},
                {"dept_id": 15, "dept_name": "Customer Service", "location": "Chandigarh"},
                {"dept_id": 16, "dept_name": "Engineering", "location": "Kochi"},
                {"dept_id": 17, "dept_name": "Product Management", "location": "Nagpur"},
                {"dept_id": 18, "dept_name": "Quality Assurance", "location": "Visakhapatnam"},
                {"dept_id": 19, "dept_name": "Data Science", "location": "Patna"},
                {"dept_id": 20, "dept_name": "Public Relations", "location": "Dehradun"},
                {"dept_id": 21, "dept_name": "Strategy", "location": "Indore"},
                {"dept_id": 22, "dept_name": "Innovation", "location": "Gandhinagar"},
                {"dept_id": 23, "dept_name": "Compliance", "location": "Meerut"},
                {"dept_id": 24, "dept_name": "Analytics", "location": "Shillong"},
                {"dept_id": 25, "dept_name": "Sustainability", "location": "Thiruvananthapuram"}
            ]
        },

        "employee": {
            "emp_id": {"type": "int", "primary_key": True},
            "emp_name": {"type": "varchar"},
            "gender": {"type": "char(1)"},
            "dob": {"type": "string"},
            "hire_date": {"type": "string"},
            "salary": {"type": "float"},
            "dept_id": {"type": "int", "foreign_key": "department.dept_id"},
            "manager_id": {"type": "int", "foreign_key": "employee.emp_id"},
            "sample_data": [
                {"emp_id": 101, "emp_name": "Ravi Kumar", "gender": "M", "dob": "1985-07-12", "hire_date": "2010-05-10", "salary": 95000.0, "dept_id": 1, "manager_id": None},
                {"emp_id": 102, "emp_name": "Priya Sharma", "gender": "F", "dob": "1990-04-15", "hire_date": "2013-09-23", "salary": 87000.0, "dept_id": 2, "manager_id": 101},
                {"emp_id": 103, "emp_name": "Amit Singh", "gender": "M", "dob": "1988-12-05", "hire_date": "2014-01-12", "salary": 81000.0, "dept_id": 3, "manager_id": 102},
                {"emp_id": 104, "emp_name": "Neha Verma", "gender": "F", "dob": "1991-03-18", "hire_date": "2016-04-30", "salary": 76000.0, "dept_id": 4, "manager_id": 102},
                {"emp_id": 105, "emp_name": "Karan Patel", "gender": "M", "dob": "1992-09-25", "hire_date": "2017-08-10", "salary": 72000.0, "dept_id": 5, "manager_id": 101},
                {"emp_id": 106, "emp_name": "Meena Joshi", "gender": "F", "dob": "1989-11-30", "hire_date": "2011-06-19", "salary": 69000.0, "dept_id": 6, "manager_id": 103},
                {"emp_id": 107, "emp_name": "Anil Mehta", "gender": "M", "dob": "1984-05-20", "hire_date": "2009-02-14", "salary": 98000.0, "dept_id": 7, "manager_id": 101},
                {"emp_id": 108, "emp_name": "Sunita Rao", "gender": "F", "dob": "1993-01-12", "hire_date": "2018-03-11", "salary": 61000.0, "dept_id": 8, "manager_id": 104},
                {"emp_id": 109, "emp_name": "Vikram Nair", "gender": "M", "dob": "1986-06-22", "hire_date": "2012-07-16", "salary": 84000.0, "dept_id": 9, "manager_id": 105},
                {"emp_id": 110, "emp_name": "Anjali Deshmukh", "gender": "F", "dob": "1994-02-17", "hire_date": "2019-11-08", "salary": 55000.0, "dept_id": 10, "manager_id": 104},
                {"emp_id": 111, "emp_name": "Rajesh Kumar", "gender": "M", "dob": "1991-10-05", "hire_date": "2016-06-12", "salary": 70000.0, "dept_id": 1, "manager_id": 101},
                {"emp_id": 112, "emp_name": "Shreya Reddy", "gender": "F", "dob": "1987-08-19", "hire_date": "2011-09-01", "salary": 86000.0, "dept_id": 2, "manager_id": 102},
                {"emp_id": 113, "emp_name": "Manoj Tiwari", "gender": "M", "dob": "1985-01-25", "hire_date": "2010-02-17", "salary": 90000.0, "dept_id": 3, "manager_id": 103},
                {"emp_id": 114, "emp_name": "Kavita Iyer", "gender": "F", "dob": "1990-11-10", "hire_date": "2014-07-07", "salary": 73000.0, "dept_id": 4, "manager_id": 104},
                {"emp_id": 115, "emp_name": "Sameer Jain", "gender": "M", "dob": "1992-03-28", "hire_date": "2015-09-30", "salary": 78000.0, "dept_id": 5, "manager_id": 105},
                {"emp_id": 116, "emp_name": "Pooja Malhotra", "gender": "F", "dob": "1993-07-08", "hire_date": "2016-12-22", "salary": 62000.0, "dept_id": 6, "manager_id": 106},
                {"emp_id": 117, "emp_name": "Deepak Shah", "gender": "M", "dob": "1986-09-15", "hire_date": "2008-10-10", "salary": 92000.0, "dept_id": 7, "manager_id": 107},
                {"emp_id": 118, "emp_name": "Ritika Saxena", "gender": "F", "dob": "1995-04-03", "hire_date": "2020-02-05", "salary": 50000.0, "dept_id": 8, "manager_id": 108},
                {"emp_id": 119, "emp_name": "Suresh Babu", "gender": "M", "dob": "1990-12-29", "hire_date": "2013-04-14", "salary": 76000.0, "dept_id": 9, "manager_id": 109},
                {"emp_id": 120, "emp_name": "Nidhi Aggarwal", "gender": "F", "dob": "1991-06-06", "hire_date": "2015-01-28", "salary": 67000.0, "dept_id": 10, "manager_id": 110},
                {"emp_id": 121, "emp_name": "Ajay Kulkarni", "gender": "M", "dob": "1989-08-13", "hire_date": "2012-05-01", "salary": 82000.0, "dept_id": 1, "manager_id": 111},
                {"emp_id": 122, "emp_name": "Divya Menon", "gender": "F", "dob": "1992-02-09", "hire_date": "2017-03-18", "salary": 71000.0, "dept_id": 2, "manager_id": 112},
                {"emp_id": 123, "emp_name": "Tarun Das", "gender": "M", "dob": "1987-03-05", "hire_date": "2009-12-05", "salary": 94000.0, "dept_id": 3, "manager_id": 113},
                {"emp_id": 124, "emp_name": "Ishita Roy", "gender": "F", "dob": "1993-10-21", "hire_date": "2018-06-09", "salary": 60000.0, "dept_id": 4, "manager_id": 114},
                {"emp_id": 125, "emp_name": "Mohit Arora", "gender": "M", "dob": "1994-01-11", "hire_date": "2019-04-01", "salary": 64000.0, "dept_id": 5, "manager_id": 115}
            ]
        },

        "project": {
            "project_id": {"type": "int", "primary_key": True},
            "project_name": {"type": "varchar"},
            "start_date": {"type": "string"},
            "end_date": {"type": "string"},
            "dept_id": {"type": "int", "foreign_key": "department.dept_id"},
            "sample_data": [
                {"project_id": 201, "project_name": "HR Management System", "start_date": "2023-01-01", "end_date": "2023-12-31", "dept_id": 1},
                {"project_id": 202, "project_name": "AI Integration", "start_date": "2023-06-01", "end_date": None, "dept_id": 2},
                {"project_id": 203, "project_name": "Sales Forecasting", "start_date": "2023-03-10", "end_date": "2023-09-10", "dept_id": 3},
                {"project_id": 204, "project_name": "Marketing Campaign 2024", "start_date": "2024-01-15", "end_date": "2024-06-15", "dept_id": 4},
                {"project_id": 205, "project_name": "GST Compliance Audit", "start_date": "2023-07-01", "end_date": "2023-11-30", "dept_id": 5},
                {"project_id": 206, "project_name": "Contract Management", "start_date": "2023-08-05", "end_date": None, "dept_id": 6},
                {"project_id": 207, "project_name": "Patent Filing Portal", "start_date": "2023-02-20", "end_date": "2023-12-20", "dept_id": 7},
                {"project_id": 208, "project_name": "CRM Support System", "start_date": "2024-03-01", "end_date": "2024-12-01", "dept_id": 8},
                {"project_id": 209, "project_name": "Vendor Onboarding", "start_date": "2023-10-10", "end_date": None, "dept_id": 9},
                {"project_id": 210, "project_name": "Warehouse Automation", "start_date": "2022-11-01", "end_date": "2023-11-01", "dept_id": 10},
                {"project_id": 211, "project_name": "Digital Office Setup", "start_date": "2023-01-10", "end_date": "2023-04-30", "dept_id": 11},
                {"project_id": 212, "project_name": "Security Surveillance Upgrade", "start_date": "2023-05-15", "end_date": "2023-09-15", "dept_id": 12},
                {"project_id": 213, "project_name": "Training Portal", "start_date": "2023-03-01", "end_date": "2023-06-30", "dept_id": 13},
                {"project_id": 214, "project_name": "ERP Optimization", "start_date": "2023-07-10", "end_date": None, "dept_id": 14},
                {"project_id": 215, "project_name": "Customer Chatbot", "start_date": "2023-08-01", "end_date": "2024-01-31", "dept_id": 15},
                {"project_id": 216, "project_name": "IoT Sensor Network", "start_date": "2023-09-05", "end_date": "2024-03-05", "dept_id": 16},
                {"project_id": 217, "project_name": "Product Redesign", "start_date": "2023-04-10", "end_date": None, "dept_id": 17},
                {"project_id": 218, "project_name": "QA Automation Tools", "start_date": "2023-06-20", "end_date": "2024-02-20", "dept_id": 18},
                {"project_id": 219, "project_name": "Data Analytics Dashboard", "start_date": "2023-10-01", "end_date": "2024-04-01", "dept_id": 19},
                {"project_id": 220, "project_name": "Media Outreach Plan", "start_date": "2023-12-01", "end_date": "2024-06-01", "dept_id": 20}
            ]
        },

        "works_on": {
            "emp_id": {"type": "int", "foreign_key": "employee.emp_id","primary_key": True},
            "project_id": {"type": "int", "foreign_key": "project.project_id","primary_key": True},
            "hours_per_week": {"type": "int"},
            "primary_key": ["emp_id", "project_id"],
            "sample_data": [
                {"emp_id": 101, "project_id": 201, "hours_per_week": 10},
                {"emp_id": 102, "project_id": 202, "hours_per_week": 30},
                {"emp_id": 103, "project_id": 203, "hours_per_week": 25},
                {"emp_id": 104, "project_id": 204, "hours_per_week": 35},
                {"emp_id": 105, "project_id": 205, "hours_per_week": 20},
                {"emp_id": 106, "project_id": 206, "hours_per_week": 15},
                {"emp_id": 107, "project_id": 207, "hours_per_week": 28},
                {"emp_id": 108, "project_id": 208, "hours_per_week": 30},
                {"emp_id": 109, "project_id": 209, "hours_per_week": 18},
                {"emp_id": 110, "project_id": 210, "hours_per_week": 22},
                {"emp_id": 111, "project_id": 211, "hours_per_week": 16},
                {"emp_id": 112, "project_id": 212, "hours_per_week": 12},
                {"emp_id": 113, "project_id": 213, "hours_per_week": 24},
                {"emp_id": 114, "project_id": 214, "hours_per_week": 26},
                {"emp_id": 115, "project_id": 215, "hours_per_week": 20},
                {"emp_id": 116, "project_id": 216, "hours_per_week": 14},
                {"emp_id": 117, "project_id": 217, "hours_per_week": 30},
                {"emp_id": 118, "project_id": 218, "hours_per_week": 16},
                {"emp_id": 119, "project_id": 219, "hours_per_week": 22},
                {"emp_id": 120, "project_id": 220, "hours_per_week": 25},
                {"emp_id": 121, "project_id": 201, "hours_per_week": 12},
                {"emp_id": 122, "project_id": 202, "hours_per_week": 28},
                {"emp_id": 123, "project_id": 203, "hours_per_week": 15},
                {"emp_id": 124, "project_id": 204, "hours_per_week": 10},
                {"emp_id": 125, "project_id": 205, "hours_per_week": 18}
            ]
        },

        "dependent": {
            "dependent_id": {"type": "int", "primary_key": True},
            "emp_id": {"type": "int", "foreign_key": "employee.emp_id"},
            "name": {"type": "varchar"},
            "relation": {"type": "varchar"},
            "birth_date": {"type": "string"},
            "sample_data": [
                {"dependent_id": 1, "emp_id": 101, "name": "Aarav Kumar", "relation": "Son", "birth_date": "2015-04-20"},
                {"dependent_id": 2, "emp_id": 102, "name": "Sneha Sharma", "relation": "Spouse", "birth_date": "1989-06-10"},
                {"dependent_id": 3, "emp_id": 103, "name": "Riya Singh", "relation": "Daughter", "birth_date": "2016-09-15"},
                {"dependent_id": 4, "emp_id": 104, "name": "Alok Verma", "relation": "Father", "birth_date": "1960-02-18"},
                {"dependent_id": 5, "emp_id": 105, "name": "Sita Patel", "relation": "Mother", "birth_date": "1965-07-07"},
                {"dependent_id": 6, "emp_id": 106, "name": "Rohan Joshi", "relation": "Son", "birth_date": "2017-05-05"},
                {"dependent_id": 7, "emp_id": 107, "name": "Deepa Mehta", "relation": "Spouse", "birth_date": "1986-12-30"},
                {"dependent_id": 8, "emp_id": 108, "name": "Priya Rao", "relation": "Daughter", "birth_date": "2014-08-23"},
                {"dependent_id": 9, "emp_id": 109, "name": "Mohan Nair", "relation": "Father", "birth_date": "1955-11-11"},
                {"dependent_id": 10, "emp_id": 110, "name": "Leela Deshmukh", "relation": "Mother", "birth_date": "1962-04-01"},
                {"dependent_id": 11, "emp_id": 111, "name": "Kabir Kumar", "relation": "Son", "birth_date": "2018-01-20"},
                {"dependent_id": 12, "emp_id": 112, "name": "Ritu Reddy", "relation": "Spouse", "birth_date": "1991-09-05"},
                {"dependent_id": 13, "emp_id": 113, "name": "Aanya Tiwari", "relation": "Daughter", "birth_date": "2019-06-14"},
                {"dependent_id": 14, "emp_id": 114, "name": "Nandini Iyer", "relation": "Spouse", "birth_date": "1992-02-11"},
                {"dependent_id": 15, "emp_id": 115, "name": "Rakesh Jain", "relation": "Father", "birth_date": "1958-10-22"},
                {"dependent_id": 16, "emp_id": 116, "name": "Meera Malhotra", "relation": "Mother", "birth_date": "1961-07-13"},
                {"dependent_id": 17, "emp_id": 117, "name": "Aarohi Shah", "relation": "Daughter", "birth_date": "2020-03-17"},
                {"dependent_id": 18, "emp_id": 118, "name": "Manav Saxena", "relation": "Son", "birth_date": "2016-12-25"},
                {"dependent_id": 19, "emp_id": 119, "name": "Sonal Babu", "relation": "Spouse", "birth_date": "1990-05-30"},
                {"dependent_id": 20, "emp_id": 120, "name": "Anita Aggarwal", "relation": "Mother", "birth_date": "1963-03-03"},
                {"dependent_id": 21, "emp_id": 121, "name": "Ayaan Kulkarni", "relation": "Son", "birth_date": "2017-11-11"},
                {"dependent_id": 22, "emp_id": 122, "name": "Divya Menon", "relation": "Spouse", "birth_date": "1994-01-15"},
                {"dependent_id": 23, "emp_id": 123, "name": "Krishna Das", "relation": "Father", "birth_date": "1957-06-18"},
                {"dependent_id": 24, "emp_id": 124, "name": "Ishita Roy", "relation": "Spouse", "birth_date": "1993-10-21"},
                {"dependent_id": 25, "emp_id": 125, "name": "Ananya Arora", "relation": "Daughter", "birth_date": "2021-08-08"}
            ]
        },

        "job": {
    "job_id": {"type": "int", "primary_key": True},
    "job_title": {"type": "varchar"},
    "min_salary": {"type": "float"},
    "max_salary": {"type": "float"},
    "sample_data": [
        {"job_id": 1, "job_title": "Software Engineer", "min_salary": 50000.0, "max_salary": 100000.0},
        {"job_id": 2, "job_title": "HR Manager", "min_salary": 60000.0, "max_salary": 90000.0},
        {"job_id": 3, "job_title": "Data Analyst", "min_salary": 45000.0, "max_salary": 85000.0},
        {"job_id": 4, "job_title": "Finance Executive", "min_salary": 40000.0, "max_salary": 75000.0},
        {"job_id": 5, "job_title": "Marketing Specialist", "min_salary": 42000.0, "max_salary": 80000.0},
        {"job_id": 6, "job_title": "Legal Advisor", "min_salary": 65000.0, "max_salary": 110000.0},
        {"job_id": 7, "job_title": "Project Manager", "min_salary": 75000.0, "max_salary": 120000.0},
        {"job_id": 8, "job_title": "Operations Head", "min_salary": 70000.0, "max_salary": 115000.0},
        {"job_id": 9, "job_title": "Quality Analyst", "min_salary": 50000.0, "max_salary": 90000.0},
        {"job_id": 10, "job_title": "Support Engineer", "min_salary": 40000.0, "max_salary": 70000.0},
        {"job_id": 11, "job_title": "UI/UX Designer", "min_salary": 45000.0, "max_salary": 85000.0},
        {"job_id": 12, "job_title": "Research Scientist", "min_salary": 60000.0, "max_salary": 105000.0},
        {"job_id": 13, "job_title": "Business Analyst", "min_salary": 55000.0, "max_salary": 95000.0},
        {"job_id": 14, "job_title": "Database Administrator", "min_salary": 52000.0, "max_salary": 100000.0},
        {"job_id": 15, "job_title": "DevOps Engineer", "min_salary": 60000.0, "max_salary": 110000.0},
        {"job_id": 16, "job_title": "Cybersecurity Analyst", "min_salary": 58000.0, "max_salary": 108000.0},
        {"job_id": 17, "job_title": "Content Manager", "min_salary": 40000.0, "max_salary": 78000.0},
        {"job_id": 18, "job_title": "Product Manager", "min_salary": 72000.0, "max_salary": 125000.0},
        {"job_id": 19, "job_title": "Cloud Engineer", "min_salary": 65000.0, "max_salary": 115000.0},
        {"job_id": 20, "job_title": "Network Administrator", "min_salary": 47000.0, "max_salary": 89000.0}
    ]
},

        "job_history": {
            "emp_id": {"type": "int", "foreign_key": "employee.emp_id","primary_key": True},
            "start_date": {"type": "string","primary_key": True},
            "end_date": {"type": "string"},
            "job_id": {"type": "int", "foreign_key": "job.job_id"},
            "dept_id": {"type": "int", "foreign_key": "department.dept_id"},
            "primary_key": ["emp_id", "start_date"],
            "sample_data": [
                {"emp_id": 101, "start_date": "2012-06-01", "end_date": "2015-01-09", "job_id": 10, "dept_id": 1},
                {"emp_id": 102, "start_date": "2014-03-12", "end_date": "2020-05-01", "job_id": 1, "dept_id": 2},
                {"emp_id": 103, "start_date": "2013-01-10", "end_date": "2016-06-01", "job_id": 3, "dept_id": 3},
                {"emp_id": 104, "start_date": "2017-08-15", "end_date": "2020-12-31", "job_id": 4, "dept_id": 4},
                {"emp_id": 105, "start_date": "2015-02-20", "end_date": "2022-03-15", "job_id": 5, "dept_id": 5},
                {"emp_id": 106, "start_date": "2018-09-01", "end_date": "2021-09-01", "job_id": 6, "dept_id": 6},
                {"emp_id": 107, "start_date": "2011-04-10", "end_date": "2014-10-10", "job_id": 7, "dept_id": 7},
                {"emp_id": 108, "start_date": "2016-01-01", "end_date": "2018-05-30", "job_id": 8, "dept_id": 8},
                {"emp_id": 109, "start_date": "2019-02-05", "end_date": "2022-08-05", "job_id": 9, "dept_id": 9},
                {"emp_id": 110, "start_date": "2013-07-01", "end_date": "2016-07-01", "job_id": 2, "dept_id": 1},
                {"emp_id": 111, "start_date": "2014-11-11", "end_date": "2017-11-11", "job_id": 11, "dept_id": 10},
                {"emp_id": 112, "start_date": "2015-03-15", "end_date": "2020-03-15", "job_id": 12, "dept_id": 11},
                {"emp_id": 113, "start_date": "2016-06-20", "end_date": "2019-12-31", "job_id": 13, "dept_id": 12},
                {"emp_id": 114, "start_date": "2017-01-01", "end_date": "2021-01-01", "job_id": 14, "dept_id": 13},
                {"emp_id": 115, "start_date": "2018-08-08", "end_date": "2022-08-08", "job_id": 15, "dept_id": 14},
                {"emp_id": 116, "start_date": "2013-05-25", "end_date": "2016-05-25", "job_id": 16, "dept_id": 15},
                {"emp_id": 117, "start_date": "2014-10-01", "end_date": "2020-10-01", "job_id": 17, "dept_id": 16},
                {"emp_id": 118, "start_date": "2016-12-12", "end_date": "2020-12-12", "job_id": 18, "dept_id": 17},
                {"emp_id": 119, "start_date": "2017-09-09", "end_date": "2022-09-09", "job_id": 19, "dept_id": 18},
                {"emp_id": 120, "start_date": "2012-03-01", "end_date": "2016-03-01", "job_id": 20, "dept_id": 19}
            ]
        }

    }

def validate_schema(schema):
    # Map schema types to Python types
    type_mapping = {
        "string": str,
        "varchar": str,
        "char(1)": str,
        "int": int,
        "float": float
    }

    for table_name, table_def in schema.items():
        sample_data = table_def.get("sample_data", [])
        columns = {col: col_def for col, col_def in table_def.items() if isinstance(col_def, dict) and "type" in col_def}

        # Validate each row in sample_data
        for row in sample_data:
            # Check that all required columns are present and of correct type
            for col_name, col_def in columns.items():
                if col_name not in row:
                    raise ValueError(f"Missing column '{col_name}' in table '{table_name}' sample_data.")
                if row[col_name] is not None:
                    expected_type = type_mapping.get(col_def["type"])
                    if expected_type and not isinstance(row[col_name], expected_type):
                        raise ValueError(
                            f"Invalid type for column '{col_name}' in table '{table_name}'. "
                            f"Expected {col_def['type']}, got {type(row[col_name]).__name__}."
                        )

            # Check for extra keys
            for key in row.keys():
                if key not in columns:
                    raise ValueError(f"Unexpected column '{key}' in table '{table_name}' sample_data.")

        # Primary key validation
        primary_keys = [col for col, col_def in columns.items() if col_def.get("primary_key")]
        if primary_keys:
            seen_keys = set()
            for row in sample_data:
                pk_values = tuple(row[pk] for pk in primary_keys)
                if pk_values in seen_keys:
                    raise ValueError(f"Duplicate primary key {pk_values} in table '{table_name}'.")
                seen_keys.add(pk_values)

        # Foreign key validation
        for col, col_def in columns.items():
            if "foreign_key" in col_def:
                ref_table, ref_col = col_def["foreign_key"].split(".")
                ref_data = schema.get(ref_table, {}).get("sample_data", [])
                ref_values = {r[ref_col] for r in ref_data if r[ref_col] is not None}
                for row in sample_data:
                    if row[col] is not None and row[col] not in ref_values:
                        raise ValueError(
                            f"Foreign key constraint violation in table '{table_name}', column '{col}'. "
                            f"Value '{row[col]}' not found in '{ref_table}.{ref_col}'."
                        )

    return True

def test_schema():
    schema = get_company_schema()
    try:
        if validate_schema(schema):
            print("✅ Company schema validation passed.")
    except ValueError as e:
        print(f"❌ Schema validation failed: {e}")


if __name__ == "__main__":
    test_schema()
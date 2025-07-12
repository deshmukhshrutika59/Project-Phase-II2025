def get_university_schema():
    return {
        "classroom": {
            "building": {"type": "string", "primary_key": True},
            "room_no": {"type": "string", "primary_key": True},
            "capacity": {"type": "int"},
            "sample_data": [
                {"building": "Vikram Sarabhai", "room_no": "101", "capacity": 50},
                {"building": "CV Raman", "room_no": "514", "capacity": 120},
                {"building": "APJ Abdul Kalam", "room_no": "3128", "capacity": 100},
                {"building": "Homi Bhabha", "room_no": "514", "capacity": 70},
                {"building": "Homi Bhabha", "room_no": "100", "capacity": 30},
                {"building": "APJ Abdul Kalam", "room_no": "500", "capacity": 10},
                {"building": "Vikram Sarabhai", "room_no": "102", "capacity": 60},
                {"building": "CV Raman", "room_no": "215", "capacity": 90},
                {"building": "Homi Bhabha", "room_no": "206", "capacity": 80},
                {"building": "Vikram Sarabhai", "room_no": "305", "capacity": 40},
                {"building": "CV Raman", "room_no": "410", "capacity": 150},
                {"building": "Homi Bhabha", "room_no": "120", "capacity": 50}
            ]

        },

        "department": {
            "dept_name": {"type": "string", "primary_key": True},
            "building": {"type": "string"},
            "budget": {"type": "float"},
            "sample_data": [
                {"dept_name": "Biotechnology", "building": "Homi Bhabha Block", "budget": 95000.0},
                {"dept_name": "Computer Science and Engineering", "building": "APJ Abdul Kalam Block", "budget": 125000.0},
                {"dept_name": "Electrical and Electronics Engineering", "building": "Visvesvaraya Block", "budget": 110000.0},
                {"dept_name": "Commerce and Finance", "building": "Chanakya Bhavan", "budget": 105000.0},
                {"dept_name": "History and Culture", "building": "CV Raman Hall", "budget": 60000.0},
                {"dept_name": "Indian Classical Music", "building": "Vikram Sarabhai Auditorium", "budget": 85000.0},
                {"dept_name": "Physics", "building": "Homi Bhabha Block", "budget": 90000.0}
            ]
        },

        "course": {
            "course_id": {"type": "string", "primary_key": True},
            "title": {"type": "string"},
            "dept_name": {"type": "string", "foreign_key": "department.dept_name"},
            "credits": {"type": "int"},
            "sample_data": [
                {"course_id": "BIO-101", "title": "Introduction to Biology", "dept_name": "Biotechnology", "credits": 4},
                {"course_id": "BIO-301", "title": "Genetics and Molecular Biology", "dept_name": "Biotechnology", "credits": 4},
                {"course_id": "BIO-399", "title": "Computational Biology", "dept_name": "Biotechnology", "credits": 3},
                {"course_id": "CS-101", "title": "Introduction to Computer Science", "dept_name": "Computer Science and Engineering", "credits": 4},                {"course_id": "CS-190", "title": "Game Design and Development", "dept_name": "Computer Science and Engineering", "credits": 4},
                {"course_id": "CS-315", "title": "Introduction to Robotics", "dept_name": "Computer Science and Engineering", "credits": 3},
                {"course_id": "CS-319", "title": "Digital Image Processing", "dept_name": "Computer Science and Engineering", "credits": 3},
                {"course_id": "CS-347", "title": "Database Systems", "dept_name": "Computer Science and Engineering", "credits": 3},
                {"course_id": "EE-181", "title": "Fundamentals of Digital Systems", "dept_name": "Electrical and Electronics Engineering", "credits": 3},
                {"course_id": "COM-201", "title": "Investment and Portfolio Management", "dept_name": "Commerce and Finance", "credits": 3},
                {"course_id": "HIS-351", "title": "History of Modern India", "dept_name": "History and Culture", "credits": 3},
                {"course_id": "FIN-201", "title": "Financial Management", "dept_name": "Commerce and Finance", "credits": 3},  
                {"course_id": "MU-199", "title": "Indian Classical Music and Media", "dept_name": "Indian Classical Music", "credits": 3},
                {"course_id": "PHY-101", "title": "Principles of Physics", "dept_name": "Physics", "credits": 4},
                {"course_id": "PHY-102", "title": "Introduction to Physics", "dept_name": "Physics", "credits": 3}
            ]

        },

        "instructor": {
            "ID": {"type": "string", "primary_key": True},
            "name": {"type": "string"},
            "dept_name": {"type": "string", "foreign_key": "department.dept_name"},
            "salary": {"type": "float"},
            "sample_data": [
                {"ID": "10101", "name": "Dr. Srinivasan", "dept_name": "Computer Science and Engineering", "salary": 65000.0},
                {"ID": "12121", "name": "Prof. Mehta", "dept_name": "Commerce and Finance", "salary": 90000.0},
                {"ID": "15151", "name": "Dr. A. R. Rahman", "dept_name": "Indian Classical Music", "salary": 40000.0},
                {"ID": "22222", "name": "Dr. C. V. Raman", "dept_name": "Physics", "salary": 95000.0},
                {"ID": "32343", "name": "Dr. Romila Thapar", "dept_name": "History and Culture", "salary": 60000.0},
                {"ID": "33456", "name": "Dr. Homi Bhabha", "dept_name": "Physics", "salary": 87000.0},
                {"ID": "45565", "name": "Dr. A. P. Jayaraman", "dept_name": "Computer Science and Engineering", "salary": 75000.0},
                {"ID": "58583", "name": "Prof. Irfan Habib", "dept_name": "History and Culture", "salary": 62000.0},
                {"ID": "76543", "name": "Prof. Nirmala Sitharaman", "dept_name": "Commerce and Finance", "salary": 80000.0},
                {"ID": "76766", "name": "Dr. Venkat Ramakrishnan", "dept_name": "Biotechnology", "salary": 72000.0},
                {"ID": "83821", "name": "Dr. V. Rajaraman", "dept_name": "Computer Science and Engineering", "salary": 92000.0},
                {"ID": "98345", "name": "Dr. Kiran Bedi", "dept_name": "Electrical and Electronics Engineering", "salary": 80000.0}
            ]
        },

        "section": {
            "course_id": {"type": "string", "foreign_key": "course.course_id", "primary_key": True},
            "sec_id": {"type": "string", "primary_key": True},
            "semester": {"type": "string", "primary_key": True},
            "year": {"type": "int", "primary_key": True},
            "building": {"type": "string", "foreign_key": "classroom.building"},
            "room_no": {"type": "string", "foreign_key": "classroom.room_no"},
            "time_slot_id": {"type": "string", "foreign_key": "time_slot.time_slot_id"},
            "sample_data": [
    {"course_id": "BIO-101", "sec_id": "1", "semester": "Summer", "year": 2009, "building": "APJ Abdul Kalam", "room_no": "514", "time_slot_id": "B1"},
    {"course_id": "BIO-301", "sec_id": "1", "semester": "Summer", "year": 2010, "building": "APJ Abdul Kalam", "room_no": "514", "time_slot_id": "A1"},
    {"course_id": "CS-101", "sec_id": "1", "semester": "Fall", "year": 2009, "building": "Homi Bhabha", "room_no": "101", "time_slot_id": "H"},
    {"course_id": "CS-101", "sec_id": "1", "semester": "Spring", "year": 2010, "building": "Homi Bhabha", "room_no": "101", "time_slot_id": "F"},
    {"course_id": "CS-190", "sec_id": "1", "semester": "Spring", "year": 2009, "building": "APJ Abdul Kalam", "room_no": "3128", "time_slot_id": "E"},
    {"course_id": "CS-190", "sec_id": "2", "semester": "Spring", "year": 2009, "building": "APJ Abdul Kalam", "room_no": "3128", "time_slot_id": "A1"},
    {"course_id": "CS-315", "sec_id": "1", "semester": "Spring", "year": 2010, "building": "Vikram Sarabhai", "room_no": "120", "time_slot_id": "D1"},
    {"course_id": "CS-319", "sec_id": "1", "semester": "Spring", "year": 2010, "building": "Vikram Sarabhai", "room_no": "100", "time_slot_id": "B1"},
    {"course_id": "CS-319", "sec_id": "2", "semester": "Spring", "year": 2010, "building": "APJ Abdul Kalam", "room_no": "3128", "time_slot_id": "C1"},
    {"course_id": "CS-347", "sec_id": "1", "semester": "Fall", "year": 2009, "building": "APJ Abdul Kalam", "room_no": "3128", "time_slot_id": "A1"},
    {"course_id": "EE-181", "sec_id": "1", "semester": "Spring", "year": 2009, "building": "APJ Abdul Kalam", "room_no": "3128", "time_slot_id": "C1"},
    {"course_id": "FIN-201", "sec_id": "1", "semester": "Spring", "year": 2010, "building": "Homi Bhabha", "room_no": "101", "time_slot_id": "B1"},
    {"course_id": "HIS-351", "sec_id": "1", "semester": "Spring", "year": 2010, "building": "APJ Abdul Kalam", "room_no": "514", "time_slot_id": "C1"},
    {"course_id": "MU-199", "sec_id": "1", "semester": "Spring", "year": 2010, "building": "Homi Bhabha", "room_no": "101", "time_slot_id": "D1"},
    {"course_id": "PHY-101", "sec_id": "1", "semester": "Fall", "year": 2009, "building": "Vikram Sarabhai", "room_no": "100", "time_slot_id": "A1"}
]
        },

        "teaches": {
            "ID": {"type": "string", "foreign_key": "instructor.ID", "primary_key": True},
            "course_id": {"type": "string", "foreign_key": "section.course_id", "primary_key": True},
            "sec_id": {"type": "string", "foreign_key": "section.sec_id", "primary_key": True},
            "semester": {"type": "string", "foreign_key": "section.semester", "primary_key": True},
            "year": {"type": "int", "foreign_key": "section.year", "primary_key": True},
            "sample_data": [
                {"ID": "10101", "course_id": "CS-101", "sec_id": "1", "semester": "Fall", "year": 2009},
                {"ID": "10101", "course_id": "CS-315", "sec_id": "1", "semester": "Spring", "year": 2010},
                {"ID": "10101", "course_id": "CS-347", "sec_id": "1", "semester": "Fall", "year": 2009},
                {"ID": "12121", "course_id": "FIN-201", "sec_id": "1", "semester": "Spring", "year": 2010},
                {"ID": "15151", "course_id": "MU-199", "sec_id": "1", "semester": "Spring", "year": 2010},
                {"ID": "22222", "course_id": "PHY-101", "sec_id": "1", "semester": "Fall", "year": 2009},
                {"ID": "32343", "course_id": "HIS-351", "sec_id": "1", "semester": "Spring", "year": 2010},
                {"ID": "45565", "course_id": "CS-101", "sec_id": "1", "semester": "Spring", "year": 2010},
                {"ID": "45565", "course_id": "CS-319", "sec_id": "1", "semester": "Spring", "year": 2010},
                {"ID": "76766", "course_id": "BIO-101", "sec_id": "1", "semester": "Summer", "year": 2009},
                {"ID": "76766", "course_id": "BIO-301", "sec_id": "1", "semester": "Summer", "year": 2010},
                {"ID": "83821", "course_id": "CS-190", "sec_id": "1", "semester": "Spring", "year": 2009},
                {"ID": "83821", "course_id": "CS-190", "sec_id": "2", "semester": "Spring", "year": 2009},
                {"ID": "83821", "course_id": "CS-319", "sec_id": "2", "semester": "Spring", "year": 2010},
                {"ID": "98345", "course_id": "EE-181", "sec_id": "1", "semester": "Spring", "year": 2009}
            ]
        },

        "student": {
            "ID": {"type": "string", "primary_key": True},
            "name": {"type": "string"},
            "dept_name": {"type": "string", "foreign_key": "department.dept_name"},
            "tot_cred": {"type": "int"},
           "sample_data": [
        {"ID": "00128", "name": "Rajesh Kumar", "dept_name": "Computer Science and Engineering", "tot_cred": 102},
        {"ID": "12345", "name": "Anjali Sharma", "dept_name": "Computer Science and Engineering", "tot_cred": 32},
        {"ID": "19991", "name": "Arjun Mehta", "dept_name": "History and Culture", "tot_cred": 80},
        {"ID": "23121", "name": "Priya Desai", "dept_name": "Commerce and Finance", "tot_cred": 110},
        {"ID": "44553", "name": "Siddharth Rao", "dept_name": "Physics", "tot_cred": 56},
        {"ID": "45678", "name": "Neha Verma", "dept_name": "Physics", "tot_cred": 46},
        {"ID": "54321", "name": "Vikram Singh", "dept_name": "Computer Science and Engineering", "tot_cred": 54},
        {"ID": "55739", "name": "Ishita Kapoor", "dept_name": "Indian Classical Music", "tot_cred": 38},
        {"ID": "70557", "name": "Rahul Jain", "dept_name": "Physics", "tot_cred": 0},
        {"ID": "76543", "name": "Sneha Iyer", "dept_name": "Computer Science and Engineering", "tot_cred": 58},
        {"ID": "76653", "name": "Amitabh Reddy", "dept_name": "Electrical and Electronics Engineering", "tot_cred": 60},
        {"ID": "98765", "name": "Divya Nair", "dept_name": "Electrical and Electronics Engineering", "tot_cred": 98},
        {"ID": "98988", "name": "Karan Malhotra", "dept_name": "Biotechnology", "tot_cred": 120}
    ]
        },

        "takes": {
            "ID": {"type": "string", "foreign_key": "student.ID"},
            "course_id": {"type": "string", "foreign_key": "course.course_id"},
            "sec_id": {"type": "string", "foreign_key": "section.sec_id"},
            "semester": {"type": "string", "foreign_key": "section.semester"},
            "year": {"type": "int", "foreign_key": "section.year"},
            "grade": {"type": "string"},
            "sample_data": [
                {"ID": "00128", "course_id": "CS-101", "sec_id": "1", "semester": "Fall", "year": 2009, "grade": "A"},
                {"ID": "00128", "course_id": "CS-347", "sec_id": "1", "semester": "Fall", "year": 2009, "grade": "A"},
                {"ID": "12345", "course_id": "CS-101", "sec_id": "1", "semester": "Fall", "year": 2009, "grade": "C"},
                {"ID": "12345", "course_id": "CS-190", "sec_id": "2", "semester": "Spring", "year": 2009, "grade": "A"},
                {"ID": "12345", "course_id": "CS-315", "sec_id": "1", "semester": "Spring", "year": 2010, "grade": "A"},
                {"ID": "12345", "course_id": "CS-347", "sec_id": "1", "semester": "Fall", "year": 2009, "grade": "A"},
                {"ID": "19991", "course_id": "HIS-351", "sec_id": "1", "semester": "Spring", "year": 2010, "grade": "B"},
                {"ID": "23121", "course_id": "FIN-201", "sec_id": "1", "semester": "Spring", "year": 2010, "grade": "C+"},
                {"ID": "44553", "course_id": "PHY-101", "sec_id": "1", "semester": "Fall", "year": 2009, "grade": "B"},
                {"ID": "45678", "course_id": "CS-101", "sec_id": "1", "semester": "Fall", "year": 2009, "grade": "F"},
                {"ID": "45678", "course_id": "CS-101", "sec_id": "1", "semester": "Spring", "year": 2010, "grade": "B+"},
                {"ID": "45678", "course_id": "CS-319", "sec_id": "1", "semester": "Spring", "year": 2010, "grade": "B"},
                {"ID": "54321", "course_id": "CS-101", "sec_id": "1", "semester": "Fall", "year": 2009, "grade": "A"},
                {"ID": "54321", "course_id": "CS-190", "sec_id": "2", "semester": "Spring", "year": 2009, "grade": "B+"},
                {"ID": "55739", "course_id": "MU-199", "sec_id": "1", "semester": "Spring", "year": 2010, "grade": "A"},
                {"ID": "76543", "course_id": "CS-101", "sec_id": "1", "semester": "Fall", "year": 2009, "grade": "A"},
                {"ID": "76543", "course_id": "CS-319", "sec_id": "2", "semester": "Spring", "year": 2010, "grade": "A"},
                {"ID": "76653", "course_id": "EE-181", "sec_id": "1", "semester": "Spring", "year": 2009, "grade": "C"},
                {"ID": "98765", "course_id": "CS-101", "sec_id": "1", "semester": "Fall", "year": 2009, "grade": "C"},
                {"ID": "98765", "course_id": "CS-315", "sec_id": "1", "semester": "Spring", "year": 2010, "grade": "B"},
                {"ID": "98988", "course_id": "BIO-101", "sec_id": "1", "semester": "Summer", "year": 2009, "grade": "A"},
                {"ID": "98988", "course_id": "BIO-301", "sec_id": "1", "semester": "Summer", "year": 2010, "grade": "B"}
            ]

        },

        
        "advisor": {
            "sid": {"type": "string", "foreign_key": "student.ID", "primary_key": True},
            "iid": {"type": "string", "foreign_key": "instructor.ID", "primary_key": True},
            "sample_data": [
                {"sid": "00128", "iid": "45565"},
                {"sid": "12345", "iid": "10101"},
                {"sid": "23121", "iid": "76543"},
                {"sid": "44553", "iid": "22222"},
                {"sid": "45678", "iid": "22222"},
                {"sid": "76543", "iid": "45565"},
                {"sid": "76653", "iid": "98345"},
                {"sid": "98765", "iid": "98345"},
                {"sid": "98988", "iid": "76766"}
            ]
        },

        "time_slot": {
            "time_slot_id": {"type": "string", "primary_key": True},
            "day": {"type": "string"},
            "start_time": {"type": "string"},
            "end_time": {"type": "string"},
            "sample_data": [
                {"time_slot_id": "A1", "day": "M", "start_time": "08:00", "end_time": "08:50"},
                {"time_slot_id": "A2", "day": "W", "start_time": "08:00", "end_time": "08:50"},
                {"time_slot_id": "A3", "day": "F", "start_time": "08:00", "end_time": "08:50"},
                {"time_slot_id": "B1", "day": "M", "start_time": "09:00", "end_time": "09:50"},
                {"time_slot_id": "B2", "day": "W", "start_time": "09:00", "end_time": "09:50"},
                {"time_slot_id": "B3", "day": "F", "start_time": "09:00", "end_time": "09:50"},
                {"time_slot_id": "C1", "day": "M", "start_time": "11:00", "end_time": "11:50"},
                {"time_slot_id": "C2", "day": "W", "start_time": "11:00", "end_time": "11:50"},
                {"time_slot_id": "C3", "day": "F", "start_time": "11:00", "end_time": "11:50"},
                {"time_slot_id": "D1", "day": "M", "start_time": "13:00", "end_time": "13:50"},
                {"time_slot_id": "D2", "day": "W", "start_time": "13:00", "end_time": "13:50"},
                {"time_slot_id": "D3", "day": "F", "start_time": "13:00", "end_time": "13:50"},
                {"time_slot_id": "E", "day": "T", "start_time": "10:00", "end_time": "10:50"},
                {"time_slot_id": "F", "day": "W", "start_time": "14:00", "end_time": "14:50"},
                {"time_slot_id": "H", "day": "M", "start_time": "15:00", "end_time": "15:50"}
            ]

        },

        "prereq": {
            "course_id": {"type": "string", "foreign_key": "course.course_id", "primary_key": True},
            "prereq_id": {"type": "string", "foreign_key": "course.course_id", "primary_key": True},
            "sample_data": [
                {"course_id": "BIO-301", "prereq_id": "BIO-101"},
                {"course_id": "BIO-399", "prereq_id": "BIO-101"},
                {"course_id": "CS-190", "prereq_id": "CS-101"},
                {"course_id": "CS-315", "prereq_id": "CS-101"},
                {"course_id": "CS-319", "prereq_id": "CS-101"},
                {"course_id": "CS-347", "prereq_id": "CS-101"},
                {"course_id": "EE-181", "prereq_id": "CS-101"}
            ]

        }
    }

def validate_schema(schema):
    # Map schema types to Python types
    type_mapping = {
        "string": str,
        "int": int,
        "float": float,
    }

    for table_name, table_def in schema.items():
        sample_data = table_def.get("sample_data", [])
        columns = {col: col_def for col, col_def in table_def.items() if isinstance(col_def, dict) and "type" in col_def}

        # Validate each row in sample_data
        for row in sample_data:
            # Check that all keys in the row match the schema
            for col_name, col_def in columns.items():
                if col_name not in row:
                    raise ValueError(f"Missing column '{col_name}' in table '{table_name}' sample_data.")
                expected_type = type_mapping.get(col_def["type"])
                if expected_type and not isinstance(row[col_name], expected_type):
                    raise ValueError(
                        f"Invalid type for column '{col_name}' in table '{table_name}'. "
                        f"Expected {col_def['type']}, got {type(row[col_name]).__name__}."
                    )

            # Check for extra keys in the row
            for key in row.keys():
                if key not in columns:
                    raise ValueError(f"Unexpected column '{key}' in table '{table_name}' sample_data.")

        # Validate primary keys
        primary_keys = [col for col, col_def in columns.items() if col_def.get("primary_key")]
        if primary_keys:
            seen_keys = set()
            for row in sample_data:
                pk_values = tuple(row[pk] for pk in primary_keys)
                if pk_values in seen_keys:
                    raise ValueError(f"Duplicate primary key {pk_values} in table '{table_name}'.")
                seen_keys.add(pk_values)

        # Validate foreign keys
        for col, col_def in columns.items():
            if "foreign_key" in col_def:
                ref_table, ref_col = col_def["foreign_key"].split(".")
                ref_table_data = schema.get(ref_table, {}).get("sample_data", [])
                ref_values = {row[ref_col] for row in ref_table_data}
                for row in sample_data:
                    if row[col] not in ref_values:
                        raise ValueError(
                            f"Foreign key constraint violation in table '{table_name}', column '{col}'. "
                            f"Value '{row[col]}' not found in '{ref_table}.{ref_col}'."
                        )
    return True


def test_schema():
    schema = get_university_schema()
    try:
        if validate_schema(schema):
            print("Schema validation passed.")
    except ValueError as e:
        print(f"Schema validation failed: {e}")


if __name__ == "__main__":
    test_schema()
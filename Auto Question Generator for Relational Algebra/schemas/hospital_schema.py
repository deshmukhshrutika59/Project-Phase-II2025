def get_hospital_schema():
    return {
        "patient": {
            "patient_id": {"type": "string", "primary_key": True},
            "name": {"type": "string"},
            "age": {"type": "int"},
            "gender": {"type": "string"},
            "address": {"type": "string"},
            "phone": {"type": "string"},
            "sample_data": [
                {"patient_id": "P001", "name": "Amit Sharma", "age": 30, "gender": "M", "address": "23 MG Road, Delhi", "phone": "9876543210"},
                {"patient_id": "P002", "name": "Sneha Patel", "age": 45, "gender": "F", "address": "78 Nehru Street, Ahmedabad", "phone": "9123456789"},
                {"patient_id": "P003", "name": "Ravi Kumar", "age": 27, "gender": "M", "address": "56 Brigade Road, Bengaluru", "phone": "9090909090"},
                {"patient_id": "P004", "name": "Pooja Reddy", "age": 35, "gender": "F", "address": "14 Jubilee Hills, Hyderabad", "phone": "9345678912"},
                {"patient_id": "P005", "name": "Arjun Singh", "age": 50, "gender": "M", "address": "88 Rajpur Road, Dehradun", "phone": "9810012345"},
                {"patient_id": "P006", "name": "Neha Iyer", "age": 29, "gender": "F", "address": "19 T Nagar, Chennai", "phone": "9845123456"},
                {"patient_id": "P007", "name": "Mohammed Imran", "age": 60, "gender": "M", "address": "21 Charminar Rd, Hyderabad", "phone": "9988776655"},
                {"patient_id": "P008", "name": "Kavita Joshi", "age": 42, "gender": "F", "address": "45 FC Road, Pune", "phone": "9765432100"},
                {"patient_id": "P009", "name": "Sanjay Mehta", "age": 33, "gender": "M", "address": "302 Salt Lake, Kolkata", "phone": "9876501234"},
                {"patient_id": "P010", "name": "Anjali Deshmukh", "age": 38, "gender": "F", "address": "1 Koregaon Park, Pune", "phone": "9823012345"},
                {"patient_id": "P011", "name": "Vikram Raj", "age": 48, "gender": "M", "address": "88 Anna Nagar, Chennai", "phone": "9944332211"},
                {"patient_id": "P012", "name": "Ritika Das", "age": 36, "gender": "F", "address": "56 Gariahat Rd, Kolkata", "phone": "9830022233"},
                {"patient_id": "P013", "name": "Harish Bhatt", "age": 55, "gender": "M", "address": "72 Satellite, Ahmedabad", "phone": "9900112233"},
                {"patient_id": "P014", "name": "Divya Kapoor", "age": 47, "gender": "F", "address": "10 Hauz Khas, Delhi", "phone": "9811981198"},
                {"patient_id": "P015", "name": "Rajiv Nair", "age": 41, "gender": "M", "address": "6 Marine Drive, Mumbai", "phone": "9777776666"}
            ]
        },

        "doctor": {
            "doctor_id": {"type": "string", "primary_key": True},
            "name": {"type": "string"},
            "specialization": {"type": "string"},
            "phone": {"type": "string"},
            "salary": {"type": "float"},
            "sample_data": [
                {"doctor_id": "D001", "name": "Dr. Rajeev Malhotra", "specialization": "Cardiology", "phone": "9876543210", "salary": 150000.0},
                {"doctor_id": "D002", "name": "Dr. Anjali Mehta", "specialization": "Oncology", "phone": "9123456789", "salary": 130000.0},
                {"doctor_id": "D003", "name": "Dr. Vikram Desai", "specialization": "Neurology", "phone": "9090909090", "salary": 145000.0},
                {"doctor_id": "D004", "name": "Dr. Swati Reddy", "specialization": "Pediatrics", "phone": "9345678912", "salary": 125000.0},
                {"doctor_id": "D005", "name": "Dr. Arjun Kapoor", "specialization": "General Surgery", "phone": "9810012345", "salary": 140000.0},
                {"doctor_id": "D006", "name": "Dr. Neeraj Nair", "specialization": "Neurosurgery", "phone": "9845123456", "salary": 155000.0},
                {"doctor_id": "D007", "name": "Dr. Priya Joshi", "specialization": "Orthopedics", "phone": "9988776655", "salary": 135000.0},
                {"doctor_id": "D008", "name": "Dr. Imran Khan", "specialization": "Urology", "phone": "9765432100", "salary": 138000.0},
                {"doctor_id": "D009", "name": "Dr. Ramesh Iyer", "specialization": "Psychiatry", "phone": "9876501234", "salary": 120000.0},
                {"doctor_id": "D010", "name": "Dr. Kavita Shah", "specialization": "Endocrinology", "phone": "9823012345", "salary": 142000.0},
                {"doctor_id": "D011", "name": "Dr. Aditya Verma", "specialization": "Dermatology", "phone": "9944332211", "salary": 128000.0},
                {"doctor_id": "D012", "name": "Dr. Meenakshi Das", "specialization": "Gastroenterology", "phone": "9830022233", "salary": 134000.0},
                {"doctor_id": "D013", "name": "Dr. Sanjay Bhatt", "specialization": "Hematology", "phone": "9900112233", "salary": 129000.0},
                {"doctor_id": "D014", "name": "Dr. Nisha Kulkarni", "specialization": "Pulmonology", "phone": "9811981198", "salary": 132000.0},
                {"doctor_id": "D015", "name": "Dr. Manish Gupta", "specialization": "Rheumatology", "phone": "9777776666", "salary": 126000.0}
            ]
        },

        "department": {
            "dept_id": {"type": "string", "primary_key": True},
            "name": {"type": "string"},
            "head_id": {"type": "string", "foreign_key": "doctor.doctor_id"},
            "budget": {"type": "float"},
            "sample_data": [
                {"dept_id": "DEP01", "name": "Cardiology", "head_id": "D001", "budget": 500000.0},
                {"dept_id": "DEP02", "name": "Oncology", "head_id": "D002", "budget": 450000.0},
                {"dept_id": "DEP03", "name": "Neurology", "head_id": "D003", "budget": 470000.0},
                {"dept_id": "DEP04", "name": "Pediatrics", "head_id": "D004", "budget": 400000.0},
                {"dept_id": "DEP05", "name": "Surgery", "head_id": "D005", "budget": 550000.0},
                {"dept_id": "DEP06", "name": "Neurosurgery", "head_id": "D006", "budget": 600000.0},
                {"dept_id": "DEP07", "name": "Pediatric Surgery", "head_id": "D007", "budget": 420000.0},
                {"dept_id": "DEP08", "name": "Orthopedics", "head_id": "D008", "budget": 430000.0},
                {"dept_id": "DEP09", "name": "Plastic Surgery", "head_id": "D009", "budget": 460000.0},
                {"dept_id": "DEP10", "name": "Cardiothoracic Surgery", "head_id": "D010", "budget": 510000.0},
                {"dept_id": "DEP11", "name": "Trauma Surgery", "head_id": "D012", "budget": 480000.0},
                {"dept_id": "DEP12", "name": "General Surgery", "head_id": "D013", "budget": 470000.0},
                {"dept_id": "DEP13", "name": "Endocrinology", "head_id": "D015", "budget": 390000.0},
                {"dept_id": "DEP14", "name": "Radiology", "head_id": "D014", "budget": 440000.0},
                {"dept_id": "DEP15", "name": "Urology", "head_id": "D011", "budget": 410000.0}
            ]


        },

        "appointment": {
            "appointment_id": {"type": "string", "primary_key": True},
            "patient_id": {"type": "string", "foreign_key": "patient.patient_id"},
            "doctor_id": {"type": "string", "foreign_key": "doctor.doctor_id"},
            "date": {"type": "string"},
            "time": {"type": "string"},
            "sample_data": [
                {"appointment_id": "A001", "patient_id": "P001", "doctor_id": "D001", "date": "2025-05-01", "time": "10:00"},
                {"appointment_id": "A002", "patient_id": "P002", "doctor_id": "D002", "date": "2025-05-02", "time": "11:00"},
                {"appointment_id": "A003", "patient_id": "P003", "doctor_id": "D003", "date": "2025-05-03", "time": "09:30"},
                {"appointment_id": "A004", "patient_id": "P004", "doctor_id": "D004", "date": "2025-05-04", "time": "14:00"},
                {"appointment_id": "A005", "patient_id": "P005", "doctor_id": "D005", "date": "2025-05-05", "time": "13:00"},
                {"appointment_id": "A006", "patient_id": "P006", "doctor_id": "D006", "date": "2025-05-06", "time": "10:30"},
                {"appointment_id": "A007", "patient_id": "P007", "doctor_id": "D007", "date": "2025-05-07", "time": "15:00"},
                {"appointment_id": "A008", "patient_id": "P008", "doctor_id": "D008", "date": "2025-05-08", "time": "12:00"},
                {"appointment_id": "A009", "patient_id": "P009", "doctor_id": "D009", "date": "2025-05-09", "time": "11:30"},
                {"appointment_id": "A010", "patient_id": "P010", "doctor_id": "D010", "date": "2025-05-10", "time": "14:30"},
                {"appointment_id": "A011", "patient_id": "P011", "doctor_id": "D011", "date": "2025-05-11", "time": "13:30"},
                {"appointment_id": "A012", "patient_id": "P012", "doctor_id": "D012", "date": "2025-05-12", "time": "16:00"},
                {"appointment_id": "A013", "patient_id": "P013", "doctor_id": "D013", "date": "2025-05-13", "time": "10:15"},
                {"appointment_id": "A014", "patient_id": "P014", "doctor_id": "D014", "date": "2025-05-14", "time": "09:45"},
                {"appointment_id": "A015", "patient_id": "P015", "doctor_id": "D015", "date": "2025-05-15", "time": "11:45"}
            ]
        },

        "treatment": {
            "treatment_id": {"type": "string", "primary_key": True},
            "appointment_id": {"type": "string", "foreign_key": "appointment.appointment_id"},
            "diagnosis": {"type": "string"},
            "prescription": {"type": "string"},
            "sample_data": [
                {"treatment_id": "T001", "appointment_id": "A001", "diagnosis": "High BP", "prescription": "Beta Blockers"},
                {"treatment_id": "T002", "appointment_id": "A002", "diagnosis": "Cancer", "prescription": "Chemotherapy"},
                {"treatment_id": "T003", "appointment_id": "A003", "diagnosis": "Migraine", "prescription": "Painkillers"},
                {"treatment_id": "T004", "appointment_id": "A004", "diagnosis": "Flu", "prescription": "Antivirals"},
                {"treatment_id": "T005", "appointment_id": "A005", "diagnosis": "Appendicitis", "prescription": "Surgery"},
                {"treatment_id": "T006", "appointment_id": "A006", "diagnosis": "Diabetes", "prescription": "Insulin"},
                {"treatment_id": "T007", "appointment_id": "A007", "diagnosis": "Asthma", "prescription": "Inhalers"},
                {"treatment_id": "T008", "appointment_id": "A008", "diagnosis": "Anemia", "prescription": "Iron Supplements"},
                {"treatment_id": "T009", "appointment_id": "A009", "diagnosis": "Back Pain", "prescription": "Physiotherapy"},
                {"treatment_id": "T010", "appointment_id": "A010", "diagnosis": "Fracture", "prescription": "Casting"},
                {"treatment_id": "T011", "appointment_id": "A011", "diagnosis": "Thyroid", "prescription": "Levothyroxine"},
                {"treatment_id": "T012", "appointment_id": "A012", "diagnosis": "Ulcer", "prescription": "Antacids"},
                {"treatment_id": "T013", "appointment_id": "A013", "diagnosis": "Arthritis", "prescription": "NSAIDs"},
                {"treatment_id": "T014", "appointment_id": "A014", "diagnosis": "Sinusitis", "prescription": "Decongestants"},
                {"treatment_id": "T015", "appointment_id": "A015", "diagnosis": "Hypertension", "prescription": "ACE Inhibitors"}
            ]
        },

        "room": {
            "room_no": {"type": "string", "primary_key": True},
            "room_type": {"type": "string"},
            "status": {"type": "string"},
            "sample_data": [
                {"room_no": "R101", "room_type": "ICU", "status": "Occupied"},
                {"room_no": "R102", "room_type": "General", "status": "Available"},
                {"room_no": "R103", "room_type": "Private", "status": "Occupied"},
                {"room_no": "R104", "room_type": "ICU", "status": "Available"},
                {"room_no": "R105", "room_type": "General", "status": "Occupied"},
                {"room_no": "R106", "room_type": "Private", "status": "Available"},
                {"room_no": "R107", "room_type": "ICU", "status": "Occupied"},
                {"room_no": "R108", "room_type": "General", "status": "Available"},
                {"room_no": "R109", "room_type": "Private", "status": "Occupied"},
                {"room_no": "R110", "room_type": "ICU", "status": "Available"},
                {"room_no": "R111", "room_type": "General", "status": "Occupied"},
                {"room_no": "R112", "room_type": "Private", "status": "Available"},
                {"room_no": "R113", "room_type": "ICU", "status": "Occupied"},
                {"room_no": "R114", "room_type": "General", "status": "Available"},
                {"room_no": "R115", "room_type": "Private", "status": "Occupied"}
            ]
        },

        "admission": {
            "admission_id": {"type": "string", "primary_key": True},
            "patient_id": {"type": "string", "foreign_key": "patient.patient_id"},
            "room_no": {"type": "string", "foreign_key": "room.room_no"},
            "admit_date": {"type": "string"},
            "discharge_date": {"type": "string"},
            "sample_data": [
                {"admission_id": "AD001", "patient_id": "P001", "room_no": "R101", "admit_date": "2025-04-20", "discharge_date": "2025-04-25"},
                {"admission_id": "AD002", "patient_id": "P002", "room_no": "R102", "admit_date": "2025-04-22", "discharge_date": "2025-04-28"},
                {"admission_id": "AD003", "patient_id": "P003", "room_no": "R103", "admit_date": "2025-04-26", "discharge_date": "2025-05-01"},
                {"admission_id": "AD004", "patient_id": "P004", "room_no": "R104", "admit_date": "2025-05-01", "discharge_date": "2025-05-06"},
                {"admission_id": "AD005", "patient_id": "P005", "room_no": "R105", "admit_date": "2025-05-03", "discharge_date": "2025-05-08"},
                {"admission_id": "AD006", "patient_id": "P006", "room_no": "R106", "admit_date": "2025-05-04", "discharge_date": "2025-05-09"},
                {"admission_id": "AD007", "patient_id": "P007", "room_no": "R107", "admit_date": "2025-05-06", "discharge_date": "2025-05-11"},
                {"admission_id": "AD008", "patient_id": "P008", "room_no": "R108", "admit_date": "2025-05-07", "discharge_date": "2025-05-12"},
                {"admission_id": "AD009", "patient_id": "P009", "room_no": "R109", "admit_date": "2025-05-08", "discharge_date": "2025-05-13"},
                {"admission_id": "AD010", "patient_id": "P010", "room_no": "R110", "admit_date": "2025-05-10", "discharge_date": "2025-05-15"},
                {"admission_id": "AD011", "patient_id": "P011", "room_no": "R111", "admit_date": "2025-05-12", "discharge_date": "2025-05-17"},
                {"admission_id": "AD012", "patient_id": "P012", "room_no": "R112", "admit_date": "2025-05-14", "discharge_date": "2025-05-19"},
                {"admission_id": "AD013", "patient_id": "P013", "room_no": "R113", "admit_date": "2025-05-16", "discharge_date": "2025-05-21"},
                {"admission_id": "AD014", "patient_id": "P014", "room_no": "R114", "admit_date": "2025-05-18", "discharge_date": "2025-05-23"},
                {"admission_id": "AD015", "patient_id": "P015", "room_no": "R115", "admit_date": "2025-05-20", "discharge_date": "2025-05-25"}
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
    schema = get_hospital_schema()
    try:
        if validate_schema(schema):
            print("Schema validation passed.")
    except ValueError as e:
        print(f"Schema validation failed: {e}")


if __name__ == "__main__":
    test_schema()
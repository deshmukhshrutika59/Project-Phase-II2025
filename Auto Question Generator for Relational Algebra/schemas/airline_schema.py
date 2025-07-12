def get_airline_schema():
    return {
        "aircraft": {
            "aircraft_id": {"type": "string", "primary_key": True},
            "model": {"type": "string"},
            "capacity": {"type": "int"},
            "sample_data": [
                {"aircraft_id": "A001", "model": "Air India Express 737", "capacity": 180},
                {"aircraft_id": "A002", "model": "IndiGo A320neo", "capacity": 150},
                {"aircraft_id": "A003", "model": "Vistara 787-9 Dreamliner", "capacity": 300},
                {"aircraft_id": "A004", "model": "Air India A380 Maharaja", "capacity": 500},
                {"aircraft_id": "A005", "model": "SpiceJet 777-300ER", "capacity": 280},
                {"aircraft_id": "A006", "model": "Vistara A350-900", "capacity": 350},
                {"aircraft_id": "A007", "model": "Air India 747-400", "capacity": 400},
                {"aircraft_id": "A008", "model": "Alliance Air ATR 72", "capacity": 100},
                {"aircraft_id": "A009", "model": "IndiGo ATR 42", "capacity": 90},
                {"aircraft_id": "A010", "model": "Akasa Air A321XLR", "capacity": 220},
                {"aircraft_id": "A011", "model": "IndiGo 737 MAX 8", "capacity": 210},
                {"aircraft_id": "A012", "model": "Air India A330-200", "capacity": 250},
                {"aircraft_id": "A013", "model": "SpiceJet 767-300", "capacity": 270},
                {"aircraft_id": "A014", "model": "Vistara 787 Dreamliner", "capacity": 350},
                {"aircraft_id": "A015", "model": "Air India A340 Maharaja", "capacity": 350}
            ]
        },

        "airport": {
            "airport_id": {"type": "string", "primary_key": True},
            "name": {"type": "string"},
            "city": {"type": "string"},
            "country": {"type": "string"},
            "sample_data": [
                {"airport_id": "DEL", "name": "Indira Gandhi International", "city": "New Delhi", "country": "India"},
                {"airport_id": "BOM", "name": "Chhatrapati Shivaji Maharaj International", "city": "Mumbai", "country": "India"},
                {"airport_id": "BLR", "name": "Kempegowda International", "city": "Bengaluru", "country": "India"},
                {"airport_id": "MAA", "name": "Chennai International", "city": "Chennai", "country": "India"},
                {"airport_id": "HYD", "name": "Rajiv Gandhi International", "city": "Hyderabad", "country": "India"},
                {"airport_id": "CCU", "name": "Netaji Subhas Chandra Bose International", "city": "Kolkata", "country": "India"},
                {"airport_id": "AMD", "name": "Sardar Vallabhbhai Patel International", "city": "Ahmedabad", "country": "India"},
                {"airport_id": "COK", "name": "Cochin International", "city": "Kochi", "country": "India"},
                {"airport_id": "PNQ", "name": "Pune Airport", "city": "Pune", "country": "India"},
                {"airport_id": "GOI", "name": "Goa International (Dabolim)", "city": "Goa", "country": "India"},
                {"airport_id": "SXR", "name": "Sheikh ul-Alam International", "city": "Srinagar", "country": "India"},
                {"airport_id": "IXC", "name": "Shaheed Bhagat Singh International", "city": "Chandigarh", "country": "India"},
                {"airport_id": "LKO", "name": "Chaudhary Charan Singh International", "city": "Lucknow", "country": "India"},
                {"airport_id": "BBI", "name": "Biju Patnaik International", "city": "Bhubaneswar", "country": "India"},
                {"airport_id": "TRV", "name": "Trivandrum International", "city": "Thiruvananthapuram", "country": "India"}
            ]
        },

        "flight": {
            "flight_id": {"type": "string", "primary_key": True},
            "aircraft_id": {"type": "string", "foreign_key": "aircraft.aircraft_id"},
            "departure_airport": {"type": "string", "foreign_key": "airport.airport_id"},
            "arrival_airport": {"type": "string", "foreign_key": "airport.airport_id"},
            "departure_time": {"type": "datetime"},
            "arrival_time": {"type": "datetime"},
            "sample_data": [
                {"flight_id": "F001", "aircraft_id": "A001", "departure_airport": "DEL", "arrival_airport": "BOM", "departure_time": "2025-06-01 07:00", "arrival_time": "2025-06-01 09:00"},
                {"flight_id": "F002", "aircraft_id": "A002", "departure_airport": "BLR", "arrival_airport": "DEL", "departure_time": "2025-06-02 10:30", "arrival_time": "2025-06-02 13:15"},
                {"flight_id": "F003", "aircraft_id": "A003", "departure_airport": "HYD", "arrival_airport": "CCU", "departure_time": "2025-06-03 15:45", "arrival_time": "2025-06-03 18:20"},
                {"flight_id": "F004", "aircraft_id": "A004", "departure_airport": "MAA", "arrival_airport": "DEL", "departure_time": "2025-06-04 08:00", "arrival_time": "2025-06-04 10:45"},
                {"flight_id": "F005", "aircraft_id": "A005", "departure_airport": "GOI", "arrival_airport": "BLR", "departure_time": "2025-06-05 09:30", "arrival_time": "2025-06-05 10:30"},
                {"flight_id": "F006", "aircraft_id": "A006", "departure_airport": "DEL", "arrival_airport": "AMD", "departure_time": "2025-06-06 16:00", "arrival_time": "2025-06-06 17:30"},
                {"flight_id": "F007", "aircraft_id": "A007", "departure_airport": "CCU", "arrival_airport": "COK", "departure_time": "2025-06-07 12:00", "arrival_time": "2025-06-07 14:45"},
                {"flight_id": "F008", "aircraft_id": "A008", "departure_airport": "PNQ", "arrival_airport": "DEL", "departure_time": "2025-06-08 11:45", "arrival_time": "2025-06-08 13:30"},
                {"flight_id": "F009", "aircraft_id": "A009", "departure_airport": "TRV", "arrival_airport": "MAA", "departure_time": "2025-06-09 17:00", "arrival_time": "2025-06-09 18:20"},
                {"flight_id": "F010", "aircraft_id": "A010", "departure_airport": "LKO", "arrival_airport": "DEL", "departure_time": "2025-06-10 18:30", "arrival_time": "2025-06-10 20:00"},
                {"flight_id": "F011", "aircraft_id": "A011", "departure_airport": "COK", "arrival_airport": "HYD", "departure_time": "2025-06-11 10:00", "arrival_time": "2025-06-11 12:00"},
                {"flight_id": "F012", "aircraft_id": "A012", "departure_airport": "SXR", "arrival_airport": "DEL", "departure_time": "2025-06-12 14:00", "arrival_time": "2025-06-12 15:45"},
                {"flight_id": "F013", "aircraft_id": "A013", "departure_airport": "BBI", "arrival_airport": "MAA", "departure_time": "2025-06-13 20:00", "arrival_time": "2025-06-13 21:45"},
                {"flight_id": "F014", "aircraft_id": "A014", "departure_airport": "IXC", "arrival_airport": "DEL", "departure_time": "2025-06-14 05:00", "arrival_time": "2025-06-14 06:30"},
                {"flight_id": "F015", "aircraft_id": "A015", "departure_airport": "DEL", "arrival_airport": "TRV", "departure_time": "2025-06-15 08:00", "arrival_time": "2025-06-15 11:00"}
            ]
        },

        "passenger": {
            "passenger_id": {"type": "string", "primary_key": True},
            "name": {"type": "string"},
            "passport_number": {"type": "string"},
            "dob": {"type": "date"},
            "nationality": {"type": "string"},
            "sample_data": [
                {"passenger_id": "P001", "name": "Amit Sharma", "passport_number": "K1234567", "dob": "1990-05-15", "nationality": "India"},
                {"passenger_id": "P002", "name": "Neha Verma", "passport_number": "M2345678", "dob": "1985-07-20", "nationality": "India"},
                {"passenger_id": "P003", "name": "Mohammed Ali", "passport_number": "U3456789", "dob": "1992-11-10", "nationality": "UAE"},
                {"passenger_id": "P004", "name": "Riya Sen", "passport_number": "Z4567890", "dob": "1988-01-30", "nationality": "India"},
                {"passenger_id": "P005", "name": "Rohan Mehta", "passport_number": "H5678901", "dob": "1994-03-22", "nationality": "India"},
                {"passenger_id": "P006", "name": "Priya Nair", "passport_number": "F6789012", "dob": "1987-09-17", "nationality": "India"},
                {"passenger_id": "P007", "name": "Karan Patel", "passport_number": "B7890123", "dob": "1993-11-01", "nationality": "India"},
                {"passenger_id": "P008", "name": "Sneha Reddy", "passport_number": "T8901234", "dob": "1991-06-05", "nationality": "India"},
                {"passenger_id": "P009", "name": "Ananya Das", "passport_number": "C9012345", "dob": "1989-12-12", "nationality": "India"},
                {"passenger_id": "P010", "name": "Siddharth Iyer", "passport_number": "L0123456", "dob": "1990-08-23", "nationality": "India"},
                {"passenger_id": "P011", "name": "Rahul Khanna", "passport_number": "V1234567", "dob": "1995-01-09", "nationality": "India"},
                {"passenger_id": "P012", "name": "Meera Joshi", "passport_number": "S2345678", "dob": "1996-04-14", "nationality": "India"},
                {"passenger_id": "P013", "name": "Aditya Malhotra", "passport_number": "J3456789", "dob": "1992-07-17", "nationality": "India"},
                {"passenger_id": "P014", "name": "Kavya Pillai", "passport_number": "N4567890", "dob": "1994-10-11", "nationality": "India"},
                {"passenger_id": "P015", "name": "Tanvi Deshmukh", "passport_number": "R5678901", "dob": "1998-02-28", "nationality": "India"}
            ]
        },

        "ticket": {
            "ticket_id": {"type": "string", "primary_key": True},
            "passenger_id": {"type": "string", "foreign_key": "passenger.passenger_id"},
            "flight_id": {"type": "string", "foreign_key": "flight.flight_id"},
            "seat_number": {"type": "string"},
            "price": {"type": "float"},
            "sample_data": [
                {"ticket_id": "T001", "passenger_id": "P001", "flight_id": "F001", "seat_number": "12A", "price": 500.00},
                {"ticket_id": "T002", "passenger_id": "P002", "flight_id": "F002", "seat_number": "23B", "price": 600.00},
                {"ticket_id": "T003", "passenger_id": "P003", "flight_id": "F003", "seat_number": "7C", "price": 700.00},
                {"ticket_id": "T004", "passenger_id": "P004", "flight_id": "F004", "seat_number": "15D", "price": 750.00},
                {"ticket_id": "T005", "passenger_id": "P005", "flight_id": "F005", "seat_number": "18A", "price": 400.00},
                {"ticket_id": "T006", "passenger_id": "P006", "flight_id": "F006", "seat_number": "5B", "price": 550.00},
                {"ticket_id": "T007", "passenger_id": "P007", "flight_id": "F007", "seat_number": "3C", "price": 620.00},
                {"ticket_id": "T008", "passenger_id": "P008", "flight_id": "F008", "seat_number": "9D", "price": 680.00},
                {"ticket_id": "T009", "passenger_id": "P009", "flight_id": "F009", "seat_number": "16E", "price": 490.00},
                {"ticket_id": "T010", "passenger_id": "P010", "flight_id": "F010", "seat_number": "21A", "price": 530.00},
                {"ticket_id": "T011", "passenger_id": "P011", "flight_id": "F011", "seat_number": "13B", "price": 750.00},
                {"ticket_id": "T012", "passenger_id": "P012", "flight_id": "F012", "seat_number": "8F", "price": 710.00},
                {"ticket_id": "T013", "passenger_id": "P013", "flight_id": "F013", "seat_number": "4A", "price": 650.00},
                {"ticket_id": "T014", "passenger_id": "P014", "flight_id": "F014", "seat_number": "10B", "price": 720.00},
                {"ticket_id": "T015", "passenger_id": "P015", "flight_id": "F015", "seat_number": "2D", "price": 780.00}
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
    schema = get_airline_schema()
    try:
        if validate_schema(schema):
            print("Schema validation passed.")
    except ValueError as e:
        print(f"Schema validation failed: {e}")


if __name__ == "__main__":
    test_schema()
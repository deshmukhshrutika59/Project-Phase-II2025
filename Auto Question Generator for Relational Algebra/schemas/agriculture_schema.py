def get_agriculture_schema():
    return {
        "farmers": {
            "farmer_id": {"type": "int", "primary_key": True},
            "name": {"type": "string"},
            "age": {"type": "int"},
            "gender": {"type": "string"},
            "region": {"type": "string"},
            "sample_data": [
                {"farmer_id": 1, "name": "Ravi", "age": 45, "gender": "M", "region": "North"},
                {"farmer_id": 2, "name": "Sita", "age": 38, "gender": "F", "region": "South"},
                {"farmer_id": 3, "name": "Mohan", "age": 50, "gender": "M", "region": "East"},
                {"farmer_id": 4, "name": "Geeta", "age": 34, "gender": "F", "region": "West"},
                {"farmer_id": 5, "name": "Anil", "age": 40, "gender": "M", "region": "Central"},
                {"farmer_id": 6, "name": "Radha", "age": 29, "gender": "F", "region": "North"},
                {"farmer_id": 7, "name": "Ramesh", "age": 52, "gender": "M", "region": "South"},
                {"farmer_id": 8, "name": "Sunita", "age": 43, "gender": "F", "region": "East"},
                {"farmer_id": 9, "name": "Karan", "age": 31, "gender": "M", "region": "West"},
                {"farmer_id": 10, "name": "Meena", "age": 36, "gender": "F", "region": "Central"},
                {"farmer_id": 11, "name": "Vikram", "age": 47, "gender": "M", "region": "North"},
                {"farmer_id": 12, "name": "Priya", "age": 28, "gender": "F", "region": "South"},
                {"farmer_id": 13, "name": "Ajay", "age": 44, "gender": "M", "region": "East"},
                {"farmer_id": 14, "name": "Neha", "age": 37, "gender": "F", "region": "West"},
                {"farmer_id": 15, "name": "Manoj", "age": 49, "gender": "M", "region": "Central"},
                {"farmer_id": 16, "name": "Pooja", "age": 32, "gender": "F", "region": "North"},
                {"farmer_id": 17, "name": "Arjun", "age": 41, "gender": "M", "region": "South"},
                {"farmer_id": 18, "name": "Lata", "age": 35, "gender": "F", "region": "East"}
            ]
        },

        "fields": {
            "field_id": {"type": "int", "primary_key": True},
            "farmer_id": {"type": "int", "foreign_key": "farmers.farmer_id"},
            "area": {"type": "float"},
            "location": {"type": "string"},
           "sample_data": [
                {"field_id": 101, "farmer_id": 1, "area": 2.5, "location": "Rampur"},
                {"field_id": 102, "farmer_id": 1, "area": 1.2, "location": "Bhagalpur"},
                {"field_id": 103, "farmer_id": 2, "area": 3.0, "location": "Karjat"},
                {"field_id": 104, "farmer_id": 3, "area": 4.1, "location": "Barabanki"},
                {"field_id": 105, "farmer_id": 4, "area": 5.0, "location": "Nandurbar"},
                {"field_id": 106, "farmer_id": 5, "area": 2.8, "location": "Chhindwara"},
                {"field_id": 107, "farmer_id": 6, "area": 3.5, "location": "Palakkad"},
                {"field_id": 108, "farmer_id": 7, "area": 4.3, "location": "Yavatmal"},
                {"field_id": 109, "farmer_id": 8, "area": 6.0, "location": "Betul"},
                {"field_id": 110, "farmer_id": 9, "area": 2.2, "location": "Guntur"},
                {"field_id": 111, "farmer_id": 10, "area": 1.8, "location": "Latur"},
                {"field_id": 112, "farmer_id": 11, "area": 3.7, "location": "Bundelkhand"},
                {"field_id": 113, "farmer_id": 12, "area": 4.9, "location": "Kota"},
                {"field_id": 114, "farmer_id": 13, "area": 2.1, "location": "Purnia"},
                {"field_id": 115, "farmer_id": 14, "area": 3.3, "location": "Nagapattinam"},
                {"field_id": 116, "farmer_id": 15, "area": 5.5, "location": "Gadag"},
                {"field_id": 117, "farmer_id": 16, "area": 3.0, "location": "Sambalpur"},
                {"field_id": 118, "farmer_id": 17, "area": 4.0, "location": "Nalgonda"},
                {"field_id": 119, "farmer_id": 18, "area": 3.5, "location": "Malda"}
            ]
        },

        "crops": {
            "crop_id": {"type": "int", "primary_key": True},
            "field_id": {"type": "int", "foreign_key": "fields.field_id"},
            "crop_type": {"type": "string"},
            "season": {"type": "string"},
            "sample_data": [
                {"crop_id": 201, "field_id": 101, "crop_type": "Wheat", "season": "Rabi"},
                {"crop_id": 202, "field_id": 102, "crop_type": "Rice", "season": "Kharif"},
                {"crop_id": 203, "field_id": 103, "crop_type": "Maize", "season": "Zaid"},
                {"crop_id": 204, "field_id": 104, "crop_type": "Sugarcane", "season": "Annual"},
                {"crop_id": 205, "field_id": 105, "crop_type": "Barley", "season": "Rabi"},
                {"crop_id": 206, "field_id": 106, "crop_type": "Cotton", "season": "Kharif"},
                {"crop_id": 207, "field_id": 107, "crop_type": "Sorghum", "season": "Kharif"},
                {"crop_id": 208, "field_id": 108, "crop_type": "Peas", "season": "Rabi"},
                {"crop_id": 209, "field_id": 109, "crop_type": "Groundnut", "season": "Zaid"},
                {"crop_id": 210, "field_id": 110, "crop_type": "Mustard", "season": "Rabi"},
                {"crop_id": 211, "field_id": 111, "crop_type": "Paddy", "season": "Kharif"},
                {"crop_id": 212, "field_id": 112, "crop_type": "Lentil", "season": "Rabi"},
                {"crop_id": 213, "field_id": 113, "crop_type": "Jute", "season": "Kharif"},
                {"crop_id": 214, "field_id": 114, "crop_type": "Chickpea", "season": "Rabi"},
                {"crop_id": 215, "field_id": 115, "crop_type": "Millet", "season": "Zaid"},
                {"crop_id": 216, "field_id": 116, "crop_type": "Soybean", "season": "Kharif"},
                {"crop_id": 217, "field_id": 117, "crop_type": "Tobacco", "season": "Annual"},
                {"crop_id": 218, "field_id": 118, "crop_type": "Sunflower", "season": "Zaid"},
                {"crop_id": 219, "field_id": 119, "crop_type": "Beans", "season": "Rabi"}
            ]
        },

        "harvest": {
            "harvest_id": {"type": "int", "primary_key": True},
            "field_id": {"type": "int", "foreign_key": "fields.field_id"},
            "crop_id": {"type": "int", "foreign_key": "crops.crop_id"},
            "harvest_date": {"type": "date"},
            "quantity": {"type": "float"},
            "unit": {"type": "string"},
            "sample_data": [
                {"harvest_id": 501, "field_id": 101, "crop_id": 201, "harvest_date": "2024-03-15", "quantity": 500.0, "unit": "kg"},
                {"harvest_id": 502, "field_id": 102, "crop_id": 202, "harvest_date": "2024-09-10", "quantity": 1200.0, "unit": "kg"},
                {"harvest_id": 503, "field_id": 103, "crop_id": 203, "harvest_date": "2024-05-20", "quantity": 800.0, "unit": "kg"},
                {"harvest_id": 504, "field_id": 104, "crop_id": 204, "harvest_date": "2024-11-25", "quantity": 1500.0, "unit": "kg"},
                {"harvest_id": 505, "field_id": 105, "crop_id": 201, "harvest_date": "2024-04-10", "quantity": 600.0, "unit": "kg"},
                {"harvest_id": 506, "field_id": 106, "crop_id": 202, "harvest_date": "2024-10-05", "quantity": 1100.0, "unit": "kg"},
                {"harvest_id": 507, "field_id": 107, "crop_id": 203, "harvest_date": "2024-06-15", "quantity": 850.0, "unit": "kg"},
                {"harvest_id": 508, "field_id": 108, "crop_id": 204, "harvest_date": "2024-12-01", "quantity": 1600.0, "unit": "kg"},
                {"harvest_id": 509, "field_id": 109, "crop_id": 201, "harvest_date": "2024-03-25", "quantity": 550.0, "unit": "kg"},
                {"harvest_id": 510, "field_id": 110, "crop_id": 202, "harvest_date": "2024-09-15", "quantity": 1150.0, "unit": "kg"},
                {"harvest_id": 511, "field_id": 111, "crop_id": 203, "harvest_date": "2024-05-25", "quantity": 900.0, "unit": "kg"},
                {"harvest_id": 512, "field_id": 112, "crop_id": 204, "harvest_date": "2024-11-30", "quantity": 1700.0, "unit": "kg"},
                {"harvest_id": 513, "field_id": 113, "crop_id": 201, "harvest_date": "2024-04-05", "quantity": 650.0, "unit": "kg"},
                {"harvest_id": 514, "field_id": 114, "crop_id": 202, "harvest_date": "2024-10-20", "quantity": 1300.0, "unit": "kg"},
                {"harvest_id": 515, "field_id": 115, "crop_id": 203, "harvest_date": "2024-06-10", "quantity": 875.0, "unit": "kg"}
            ]

        },

        "pesticides": {
            "pesticide_id": {"type": "int", "primary_key": True},
            "crop_id": {"type": "int", "foreign_key": "crops.crop_id"},
            "application_date": {"type": "date"},
            "pesticide_type": {"type": "string"},
            "quantity": {"type": "float"},
            "unit": {"type": "string"},
            "sample_data": [
                {"pesticide_id": 601, "crop_id": 201, "application_date": "2024-03-10", "pesticide_type": "Insecticide", "quantity": 2.5, "unit": "liters"},
                {"pesticide_id": 602, "crop_id": 202, "application_date": "2024-08-05", "pesticide_type": "Fungicide", "quantity": 3.0, "unit": "liters"},
                {"pesticide_id": 603, "crop_id": 203, "application_date": "2024-05-15", "pesticide_type": "Herbicide", "quantity": 1.5, "unit": "liters"},
                {"pesticide_id": 604, "crop_id": 204, "application_date": "2024-10-10", "pesticide_type": "Insecticide", "quantity": 4.0, "unit": "liters"},
                {"pesticide_id": 605, "crop_id": 201, "application_date": "2024-03-20", "pesticide_type": "Fungicide", "quantity": 3.2, "unit": "liters"},
                {"pesticide_id": 606, "crop_id": 202, "application_date": "2024-08-12", "pesticide_type": "Insecticide", "quantity": 2.0, "unit": "liters"},
                {"pesticide_id": 607, "crop_id": 203, "application_date": "2024-05-25", "pesticide_type": "Herbicide", "quantity": 1.8, "unit": "liters"},
                {"pesticide_id": 608, "crop_id": 204, "application_date": "2024-10-20", "pesticide_type": "Fungicide", "quantity": 3.5, "unit": "liters"},
                {"pesticide_id": 609, "crop_id": 201, "application_date": "2024-04-05", "pesticide_type": "Insecticide", "quantity": 2.2, "unit": "liters"},
                {"pesticide_id": 610, "crop_id": 202, "application_date": "2024-08-18", "pesticide_type": "Herbicide", "quantity": 1.9, "unit": "liters"},
                {"pesticide_id": 611, "crop_id": 203, "application_date": "2024-06-10", "pesticide_type": "Fungicide", "quantity": 2.8, "unit": "liters"},
                {"pesticide_id": 612, "crop_id": 204, "application_date": "2024-11-01", "pesticide_type": "Insecticide", "quantity": 4.3, "unit": "liters"},
                {"pesticide_id": 613, "crop_id": 201, "application_date": "2024-04-12", "pesticide_type": "Herbicide", "quantity": 1.7, "unit": "liters"},
                {"pesticide_id": 614, "crop_id": 202, "application_date": "2024-08-25", "pesticide_type": "Insecticide", "quantity": 2.4, "unit": "liters"},
                {"pesticide_id": 615, "crop_id": 203, "application_date": "2024-06-20", "pesticide_type": "Fungicide", "quantity": 2.3, "unit": "liters"}
            ]

        },

        "weather": {
            "weather_id": {"type": "int", "primary_key": True},
            "field_id": {"type": "int", "foreign_key": "fields.field_id"},
            "date": {"type": "date"},
            "temperature": {"type": "float"},
            "humidity": {"type": "float"},
            "rainfall": {"type": "float"},
            "wind_speed": {"type": "float"},
            "sample_data": [
                {"weather_id": 701, "field_id": 101, "date": "2024-03-10", "temperature": 28.5, "humidity": 65.0, "rainfall": 5.2, "wind_speed": 12.5},
                {"weather_id": 702, "field_id": 102, "date": "2024-08-05", "temperature": 30.0, "humidity": 70.0, "rainfall": 3.1, "wind_speed": 10.2},
                {"weather_id": 703, "field_id": 103, "date": "2024-05-15", "temperature": 26.5, "humidity": 60.5, "rainfall": 8.4, "wind_speed": 14.3},
                {"weather_id": 704, "field_id": 104, "date": "2024-10-10", "temperature": 22.3, "humidity": 55.2, "rainfall": 0.0, "wind_speed": 8.7},
                {"weather_id": 705, "field_id": 101, "date": "2024-03-20", "temperature": 27.8, "humidity": 66.3, "rainfall": 4.5, "wind_speed": 11.0},
                {"weather_id": 706, "field_id": 102, "date": "2024-08-12", "temperature": 29.5, "humidity": 72.1, "rainfall": 1.2, "wind_speed": 9.3},
                {"weather_id": 707, "field_id": 103, "date": "2024-05-25", "temperature": 27.0, "humidity": 63.0, "rainfall": 6.3, "wind_speed": 12.0},
                {"weather_id": 708, "field_id": 104, "date": "2024-10-20", "temperature": 21.5, "humidity": 58.9, "rainfall": 0.0, "wind_speed": 7.5},
                {"weather_id": 709, "field_id": 101, "date": "2024-04-05", "temperature": 28.0, "humidity": 64.0, "rainfall": 2.0, "wind_speed": 10.8},
                {"weather_id": 710, "field_id": 102, "date": "2024-08-18", "temperature": 31.2, "humidity": 75.0, "rainfall": 3.9, "wind_speed": 11.5},
                {"weather_id": 711, "field_id": 103, "date": "2024-06-10", "temperature": 25.2, "humidity": 62.0, "rainfall": 5.5, "wind_speed": 13.4},
                {"weather_id": 712, "field_id": 104, "date": "2024-11-01", "temperature": 20.0, "humidity": 50.0, "rainfall": 0.0, "wind_speed": 6.0},
                {"weather_id": 713, "field_id": 101, "date": "2024-04-12", "temperature": 29.3, "humidity": 67.0, "rainfall": 1.8, "wind_speed": 10.5},
                {"weather_id": 714, "field_id": 102, "date": "2024-08-25", "temperature": 30.7, "humidity": 74.0, "rainfall": 2.2, "wind_speed": 9.9},
                {"weather_id": 715, "field_id": 103, "date": "2024-06-20", "temperature": 26.0, "humidity": 60.2, "rainfall": 7.1, "wind_speed": 11.8}
            ]

            },


        "irrigation": {
            "irrigation_id": {"type": "int", "primary_key": True},
            "field_id": {"type": "int", "foreign_key": "fields.field_id"},
            "method": {"type": "string"},
            "water_source": {"type": "string"},
            "sample_data": [
                {"irrigation_id": 301, "field_id": 101, "method": "Drip", "water_source": "Well"},
                {"irrigation_id": 302, "field_id": 102, "method": "Sprinkler", "water_source": "Canal"},
                {"irrigation_id": 303, "field_id": 103, "method": "Flood", "water_source": "River"},
                {"irrigation_id": 304, "field_id": 104, "method": "Drip", "water_source": "Borewell"},
                {"irrigation_id": 305, "field_id": 105, "method": "Sprinkler", "water_source": "Reservoir"},
                {"irrigation_id": 306, "field_id": 106, "method": "Flood", "water_source": "Lake"},
                {"irrigation_id": 307, "field_id": 107, "method": "Drip", "water_source": "Well"},
                {"irrigation_id": 308, "field_id": 108, "method": "Sprinkler", "water_source": "Canal"},
                {"irrigation_id": 309, "field_id": 109, "method": "Flood", "water_source": "River"},
                {"irrigation_id": 310, "field_id": 110, "method": "Drip", "water_source": "Borewell"},
                {"irrigation_id": 311, "field_id": 111, "method": "Sprinkler", "water_source": "Reservoir"},
                {"irrigation_id": 312, "field_id": 112, "method": "Flood", "water_source": "Lake"},
                {"irrigation_id": 313, "field_id": 113, "method": "Drip", "water_source": "Well"},
                {"irrigation_id": 314, "field_id": 114, "method": "Sprinkler", "water_source": "Canal"},
                {"irrigation_id": 315, "field_id": 115, "method": "Flood", "water_source": "River"}
            ]

        },

        "fertilizers": {
            "fertilizer_id": {"type": "int", "primary_key": True},
            "crop_id": {"type": "int", "foreign_key": "crops.crop_id"},
            "fertilizer_type": {"type": "string"},
            "quantity": {"type": "int"},  # in kg
            "sample_data": [
                {"fertilizer_id": 401, "crop_id": 201, "fertilizer_type": "NPK", "quantity": 50},
                {"fertilizer_id": 402, "crop_id": 202, "fertilizer_type": "Urea", "quantity": 30},
                {"fertilizer_id": 403, "crop_id": 203, "fertilizer_type": "DAP", "quantity": 40},
                {"fertilizer_id": 404, "crop_id": 204, "fertilizer_type": "Compost", "quantity": 60},
                {"fertilizer_id": 405, "crop_id": 205, "fertilizer_type": "MOP", "quantity": 35},
                {"fertilizer_id": 406, "crop_id": 206, "fertilizer_type": "Zinc Sulphate", "quantity": 25},
                {"fertilizer_id": 407, "crop_id": 207, "fertilizer_type": "Single Super Phosphate", "quantity": 45},
                {"fertilizer_id": 408, "crop_id": 208, "fertilizer_type": "Bone Meal", "quantity": 55},
                {"fertilizer_id": 409, "crop_id": 209, "fertilizer_type": "Ammonium Sulphate", "quantity": 50},
                {"fertilizer_id": 410, "crop_id": 210, "fertilizer_type": "Green Manure", "quantity": 60},
                {"fertilizer_id": 411, "crop_id": 211, "fertilizer_type": "Bio-fertilizer", "quantity": 20},
                {"fertilizer_id": 412, "crop_id": 212, "fertilizer_type": "Vermicompost", "quantity": 30},
                {"fertilizer_id": 413, "crop_id": 213, "fertilizer_type": "NPK", "quantity": 40},
                {"fertilizer_id": 414, "crop_id": 214, "fertilizer_type": "Urea", "quantity": 35},
                {"fertilizer_id": 415, "crop_id": 215, "fertilizer_type": "DAP", "quantity": 45},
                {"fertilizer_id": 416, "crop_id": 216, "fertilizer_type": "Compost", "quantity": 55},
                {"fertilizer_id": 417, "crop_id": 217, "fertilizer_type": "Organic Mix", "quantity": 50},
                {"fertilizer_id": 418, "crop_id": 218, "fertilizer_type": "MOP", "quantity": 40},
                {"fertilizer_id": 419, "crop_id": 219, "fertilizer_type": "Urea", "quantity": 60}
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
    schema = get_agriculture_schema()
    try:
        if validate_schema(schema):
            print("Schema validation passed.")
    except ValueError as e:
        print(f"Schema validation failed: {e}")


if __name__ == "__main__":
    test_schema()
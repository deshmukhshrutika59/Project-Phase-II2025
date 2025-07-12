import random
from schemas.university_schema import get_university_schema
from schemas.agriculture_schema import get_agriculture_schema
from schemas.hospital_schema import get_hospital_schema
from schemas.airline_schema import get_airline_schema 
from schemas.company_schema import get_company_schema

def get_schema_by_name():
    # List of available schemas
    schemas = ["university", "agriculture", "hospital" , "airline" , "company"]
    
    # Randomly choose a schema
    schema_name = random.choice(schemas)
    
    # Return the corresponding schema
    if schema_name == "university":
        return get_university_schema()
    elif schema_name == "agriculture":
        return get_agriculture_schema()
    elif schema_name == "hospital":
        return get_hospital_schema()
    elif schema_name == "airline":
        return get_airline_schema()
    elif schema_name == "company":
        return get_company_schema()
    else:
        raise ValueError(f"Unknown schema: {schema_name}")

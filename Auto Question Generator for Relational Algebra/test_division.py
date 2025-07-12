import unittest
from schemas.schema import get_schema_by_name
from unit_test.division import DivisionGenerator

class TestDivisionQuestionGenerator(unittest.TestCase):
    def test_all_question_generators(self):
        schema = get_schema_by_name()
        total_questions = 0
        dataset = []

        for table1_name, table1_schema in schema.items():
            for table2_name, table2_schema in schema.items():
                if table1_name == table2_name:
                    continue  # skip self-division

                print(f"\n{'=' * 60}")
                print(f"TABLES: {table1_name} ÷ {table2_name}")
                print(f"{'=' * 60}")

                # Print schema info for table1
                print(f"\nSchema for {table1_name}:")
                for attr, info in table1_schema.items():
                    if isinstance(info, dict) and attr != "sample_data":
                        print(f"  - {attr} ({info.get('type', 'N/A')})")
                pk1 = [attr for attr, info in table1_schema.items()
                       if isinstance(info, dict) and info.get("primary_key")]
                print("Primary Key(s):", pk1 or "None")
                fk1 = []
                for attr, info in table1_schema.items():
                    if isinstance(info, dict) and "foreign_key" in info:
                        fk1.append((attr, info["foreign_key"]))
                if "__foreign_keys__" in table1_schema:
                    for entry in table1_schema["__foreign_keys__"]:
                        fk1.append((entry["columns"], entry["references"]))
                print("Foreign Key(s):", fk1 or "None")

                # Print schema info for table2
                print(f"\nSchema for {table2_name}:")
                for attr, info in table2_schema.items():
                    if isinstance(info, dict) and attr != "sample_data":
                        print(f"  - {attr} ({info.get('type', 'N/A')})")
                pk2 = [attr for attr, info in table2_schema.items()
                       if isinstance(info, dict) and info.get("primary_key")]
                print("Primary Key(s):", pk2 or "None")
                fk2 = []
                for attr, info in table2_schema.items():
                    if isinstance(info, dict) and "foreign_key" in info:
                        fk2.append((attr, info["foreign_key"]))
                if "__foreign_keys__" in table2_schema:
                    for entry in table2_schema["__foreign_keys__"]:
                        fk2.append((entry["columns"], entry["references"]))
                print("Foreign Key(s):", fk2 or "None")

                # Initialize generator
                gen = DivisionGenerator(table1_name, table2_name, table1_schema, table2_schema)

                for level in ["level1", "level2", "level3"]:
                    print(f"\n--- ALL QUESTION TYPES: {level.upper()} ---")
                    try:
                        # Use get_all_questions if you followed the previous class, else adapt to your method name
                        questions = gen.generate_all_question_types(level=level)
                        for q in questions:
                            qtype = q.get("type", "UNKNOWN")
                            print(f"\n[{qtype}] Level: {q.get('level', level.upper())}")

                            if "error" in q:
                                print(f"Error: {q['error']}")
                            else:
                                if "question" in q:
                                    print(f"Q: {q['question']}")
                                if "answer" in q:
                                    print(f"A: {q['answer']}")
                                if "options" in q:
                                    for k, v in q["options"].items():
                                        print(f"  {k}) {v}")
                                if "pairs" in q:
                                    for op, desc in q["pairs"]:
                                        print(f"  {op}: {desc}")
                                if "tree" in q:
                                    print("Relational Algebra Tree:")
                                    print(q["tree"])

                            dataset.append({**q, "Table1": table1_name, "Table2": table2_name})
                            total_questions += 1
                        print()
                    except Exception as e:
                        print(f"[Error] Generating questions for {table1_name} ÷ {table2_name}, level {level.upper()}: {e}")

        print(f"\n{'=' * 60}")
        print(f"Total Questions Generated: {total_questions}")
        print(f"{'=' * 60}")

if __name__ == "__main__":
    unittest.main()
import unittest
from schemas.schema import get_schema_by_name
from unit_test.group_by import GroupByQuestionGenerator

class TestGroupByQuestionGenerators(unittest.TestCase):
    def test_all_question_generators(self):
        schema = get_schema_by_name()
        total_questions = 0
        dataset = []

        for table_name, table_schema in schema.items():
            print(f"\n{'=' * 60}")
            print(f"TABLE: {table_name}")
            print(f"{'=' * 60}")

            # Print schema info
            print("Attributes and Types:")
            for attr, info in table_schema.items():
                if isinstance(info, dict) and attr != "sample_data":
                    print(f"  - {attr} ({info.get('type', 'N/A')})")

            # Primary and Foreign Keys
            pk = [attr for attr, info in table_schema.items()
                  if isinstance(info, dict) and info.get("primary_key")]
            print("Primary Key(s):", pk or "None")

            fk = []
            for attr, info in table_schema.items():
                if isinstance(info, dict) and "foreign_key" in info:
                    fk.append((attr, info["foreign_key"]))
            if "__foreign_keys__" in table_schema:
                for entry in table_schema["__foreign_keys__"]:
                    fk.append((entry["columns"], entry["references"]))
            print("Foreign Key(s):", fk or "None")

            # Initialize generator
            gen = GroupByQuestionGenerator(table_name, table_schema)

            for level in ["level1", "level2", "level3"]:
                print(f"\n--- ALL QUESTION TYPES: {level.upper()} ---")
                try:
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

                        dataset.append({**q, "Table": table_name})
                        total_questions += 1
                    print()
                except Exception as e:
                    print(f"[Error] Generating questions for {table_name}, level {level.upper()}: {e}")

        print(f"\n{'=' * 60}")
        print(f"Total Questions Generated: {total_questions}")
        print(f"{'=' * 60}")

if __name__ == "__main__":
    unittest.main()

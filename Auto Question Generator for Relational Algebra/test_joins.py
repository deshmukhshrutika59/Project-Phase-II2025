import unittest
from schemas.schema import get_schema_by_name
from unit_test.join import JoinGenerator

class TestJoinGenerator(unittest.TestCase):
    def test_generate_questions_by_join_type(self):
        schema = get_schema_by_name()
        total_questions = 0
        dataset = []

        question_types = ["OEQ", "MCQ", "TFQ", "MTQ", "DIQ", "ECQ", "BQ"]
        levels = ["level1", "level2", "level3"]
        join_types = ["inner", "left_outer", "right_outer", "full_outer", "equijoin", "natural", "self"]

        for table_name, table_schema in schema.items():
            print(f"\n{'=' * 80}")
            print(f"TABLE: {table_name}")
            print(f"{'=' * 80}")

            join_gen = JoinGenerator(table_name, table_schema)

            for jt in join_types:
                print(f"\n{'-' * 60}")
                print(f"JOIN TYPE: {jt}")
                print(f"{'-' * 60}")

                for level in levels:
                    print(f"\n>>> LEVEL: {level.upper()}")

                    for q_type in question_types:
                        print(f"\n[{q_type}] Questions:")

                        method_name = f"generate_{q_type.lower()}"
                        if not hasattr(join_gen, method_name):
                            print(f"  [Skipped] Method '{method_name}' not implemented.")
                            continue

                        method = getattr(join_gen, method_name)

                        for _ in range(2):  # 2 samples per type per level
                            try:
                                result = method(level=level, join_type=jt)
                                if not result:
                                    print(f"  [Skipped] No data for {q_type} at {level} for join type '{jt}'")
                                    continue

                                print(f"  Q: {result.get('question', '[No question]')}")

                                if "tree" in result:
                                    print(f"  Tree:\n{result['tree']}")
                                if "options" in result:
                                    for key, val in result["options"].items():
                                        print(f"    {key}) {val}")
                                if "pairs" in result:
                                    for left, right in result["pairs"]:
                                        print(f"    {left} ↔ {right}")
                                print(f"  A: {result.get('answer', '[No answer]')}")

                                total_questions += 1
                                dataset.append({
                                    "Question": result.get("question"),
                                    "Answer": result.get("answer"),
                                    "Operation": jt,
                                    "Level": level.upper(),
                                    "Type": q_type,
                                    "Table": table_name
                                })

                            except Exception as e:
                                print(f"  [Error] {q_type} {jt} {level} for table '{table_name}': {e}")

        print(f"\n{'=' * 80}")
        print(f"✅ Total Join Questions Generated: {total_questions}")
        print(f"{'=' * 80}")

if __name__ == "__main__":
    unittest.main()

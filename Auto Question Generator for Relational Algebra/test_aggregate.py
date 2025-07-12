import unittest
from schemas.schema import get_schema_by_name
from unit_test.aggregate import AggregateGenerator

class TestAggregateGenerator(unittest.TestCase):
    def test_generate_questions_by_aggregate_type(self):
        schema = get_schema_by_name()
        total_questions = 0
        dataset = []

        question_types = ["OEQ", "MCQ", "TFQ", "MTQ", "DIQ", "ECQ", "BQ"]
        levels = ["level1", "level2", "level3"]
        agg_ops = ["SUM", "AVG", "MIN", "MAX", "COUNT"]

        for table_name, table_schema in schema.items():
            print(f"\n{'=' * 80}")
            print(f"TABLE: {table_name}")
            print(f"{'=' * 80}")

            agg_gen = AggregateGenerator(table_name, table_schema)

            for agg_type in agg_ops:
                print(f"\n{'-' * 60}")
                print(f"AGGREGATE TYPE: {agg_type}")
                print(f"{'-' * 60}")

                for level in levels:
                    print(f"\n>>> LEVEL: {level.upper()}")

                    for q_type in question_types:
                        print(f"\n[{q_type}] Questions:")

                        for _ in range(2):  # Generate 2 questions per type, per level, per agg
                            try:
                                method = getattr(agg_gen, f"generate_{q_type.lower()}")
                                result = method(level=level, agg_type=agg_type)

                                if not result:
                                    print(f"  [Skipped] No data for {q_type} at {level} for {agg_type}")
                                    continue

                                print(f"  Q: {result['question']}")
                                if "tree" in result:
                                    print(f"  Tree:\n{result['tree']}")
                                if "options" in result:
                                    for key, value in result["options"].items():
                                        print(f"    {key}) {value}")
                                if "pairs" in result:
                                    for op, desc in result["pairs"]:
                                        print(f"    {op}: {desc}")
                                print(f"  A: {result['answer']}")

                                total_questions += 1
                                dataset.append({
                                    "Question": result["question"],
                                    "Answer": result["answer"],
                                    "Operation": agg_type,
                                    "Level": level.upper(),
                                    "Type": q_type,
                                    "Table": table_name
                                })

                            except AttributeError:
                                print(f"  [Skipped] Method for {q_type} not implemented.")
                            except Exception as e:
                                print(f"  [Error] {q_type} {agg_type} {level} for table {table_name}: {e}")

        print(f"\n{'=' * 80}")
        print(f"Total Aggregate Questions Generated: {total_questions}")
        print(f"{'=' * 80}")

if __name__ == "__main__":
    unittest.main()

import random
from schemas.schema import get_schema_by_name

class CrossJoinGenerator:
    def __init__(self, table_name, table_columns):
        self.table1 = table_name
        self.schema1 = table_columns
        self.schema = get_schema_by_name()

        self.table2 = self._find_random_other_table(table_name)
        self.schema2 = self.schema.get(self.table2, {})

        self.columns1 = [col for col in self.schema1 if col != "sample_data"]
        self.columns2 = [col for col in self.schema2 if col != "sample_data"]

        self.sample_data1 = self.schema1.get("sample_data", [])
        self.sample_data2 = self.schema2.get("sample_data", [])

        self.table_name = [self.table1, self.table2]

    def _find_random_other_table(self, exclude_table):
        other_tables = [t for t in self.schema.keys() if t != exclude_table]
        return random.choice(other_tables) if other_tables else exclude_table

    def _find_random_other_table(self, exclude_table):
        other_tables = [t for t in self.schema.keys() if t != exclude_table]
        return random.choice(other_tables) if other_tables else exclude_table

    def _get_sample_values(self, table_name):
        sample_data = self.schema.get(table_name, {}).get("sample_data", [])
        return list(sample_data[0].values()) if sample_data else []

    def _col_phrase(self, col):
        if col.endswith("_id"):
            return f"{col.replace('_', ' ').capitalize()} (ID)"
        elif col == "name":
            return "Name"
        else:
            return col.replace('_', ' ').capitalize()

    def generate_bq(self, level=None):
        level = str(level).lower()
        # Level 1: Basic understanding of cross join
        if level in ["level1", "1"]:
            templates = [
                (f"List all possible combinations of rows from '{self.table1}' and '{self.table2}' using a cross join.", f"{self.table1} × {self.table2}"),
                (f"What is the result of performing a cross join between '{self.table1}' and '{self.table2}'?", f"{self.table1} × {self.table2}"),
                (f"Retrieve every possible pairing of rows between '{self.table1}' and '{self.table2}'.", f"{self.table1} × {self.table2}"),
                (f"If you want to see all possible row combinations from '{self.table1}' and '{self.table2}', which operation would you use?", f"{self.table1} × {self.table2}"),
                (f"How do you combine every row from '{self.table1}' with every row from '{self.table2}'?", f"{self.table1} × {self.table2}")
            ]
            return random.choice(templates)

        # Level 2: Projection after cross join
        elif level in ["level2", "2"]:
            if not self.columns1 or not self.columns2:
                return None, None
            a1 = random.choice(self.columns1)
            a2 = random.choice(self.columns2)
            a1_phrase = self._col_phrase(a1)
            a2_phrase = self._col_phrase(a2)
            templates = [
                (f"After cross joining, show only the {a1_phrase} from '{self.table1}'.", f"π_{a1} ({self.table1} × {self.table2})"),
                (f"Display both {a1_phrase} from '{self.table1}' and {a2_phrase} from '{self.table2}' after a cross join.", f"π_{{{a1}, {a2}}} ({self.table1} × {self.table2})"),
                (f"Which query would you use to see just the {a1_phrase} and {a2_phrase} after cross joining '{self.table1}' and '{self.table2}'?", f"π_{{{a1}, {a2}}} ({self.table1} × {self.table2})"),
                (f"How can you project only the {a1_phrase} from '{self.table1}' after a cross join with '{self.table2}'?", f"π_{a1} ({self.table1} × {self.table2})")
            ]
            return random.choice(templates)

        # Level 3: Advanced, with conditions or aggregation
        elif level in ["level3", "3"]:
            vals1 = self._get_sample_values(self.table1)
            vals2 = self._get_sample_values(self.table2)
            if not self.columns1 or not self.columns2:
                return None, None

            a1 = random.choice(self.columns1)
            a2 = random.choice(self.columns2)
            a1_phrase = self._col_phrase(a1)
            a2_phrase = self._col_phrase(a2)
            advanced_templates = []

            if vals1 and vals2:
                v1 = random.choice(vals1)
                v2 = random.choice(vals2)
                agg = random.choice(["COUNT", "SUM", "AVG"])
                advanced_templates = [
                    (
                        f"If '{self.table1}' has {len(self.sample_data1)} rows and '{self.table2}' has {len(self.sample_data2)} rows, how many rows will the cross join produce?",
                        f"{len(self.sample_data1)} × {len(self.sample_data2)} = {len(self.sample_data1) * len(self.sample_data2)}"
                    ),
                    (
                        f"After a cross join between '{self.table1}' and '{self.table2}', how would you select only those pairs where {self.table1}.{a1} = '{v1}' and {self.table2}.{a2} = '{v2}'?",
                        f"σ {self.table1}.{a1} = '{v1}' and {self.table2}.{a2} = '{v2}' ({self.table1} × {self.table2})"
                    ),
                    (
                        f"Compute the {agg} of {a1_phrase} from the cross join of '{self.table1}' and '{self.table2}'.",
                        f"{agg}({a1}) ({self.table1} × {self.table2})"
                    ),
                    (
                        f"How would you project only {a1_phrase} from '{self.table1}' and {a2_phrase} from '{self.table2}' after a cross join?",
                        f"π_{{{a1}, {a2}}} ({self.table1} × {self.table2})"
                    ),
                    (
                        f"Describe the schema of the result after cross joining '{self.table1}' and '{self.table2}'.",
                        f"All attributes from both '{self.table1}' and '{self.table2}', e.g., {self.table1}.{a1}, {self.table2}.{a2}, ..."
                    ),
                ]
            else:
                advanced_templates = [
                    (
                        f"How would you project only {a1_phrase} from '{self.table1}' and {a2_phrase} from '{self.table2}' after a cross join?",
                        f"π_{{{a1}, {a2}}} ({self.table1} × {self.table2})"
                    ),
                    (
                        f"Describe the schema of the result after cross joining '{self.table1}' and '{self.table2}'.",
                        f"All attributes from both '{self.table1}' and '{self.table2}', e.g., {self.table1}.{a1}, {self.table2}.{a2}, ..."
                    ),
                ]
            return random.choice(advanced_templates)

        else:
            print(f"[Error] Invalid level: {level}")
            return None, None

    def generate_tfq(self, level=None):
        if not isinstance(self.table_name, (list, tuple)) or len(self.table_name) < 2:
            return None

        table1, table2 = self.table_name[:2]

        templates_true = {
            "level1": [
                f"The Cartesian product of '{table1}' and '{table2}' combines each tuple of '{table1}' with every tuple of '{table2}'.",
                f"The operation '{table1} × {table2}' represents a cross join between the two tables.",
                f"A cross join returns all possible pairs of rows from '{table1}' and '{table2}'."
            ],
            "level2": [
                f"In relational algebra, '{table1} × {table2}' will produce a table with every combination of rows from both tables.",
                f"Cross join increases the number of tuples by multiplying the number of tuples in '{table1}' and '{table2}'.",
                f"Cartesian product is a fundamental operation used in join conditions and tuple combination tasks."
            ],
            "level3": [
                f"Before applying any condition between tables '{table1}' and '{table2}', a cross join generates all row pairings.",
                f"The result of a cross join can be filtered using selection operations to simulate conditional joins.",
                f"Cross join is useful when all combinations of rows from two datasets are required initially."
            ]
        }

        templates_false = {
            "level1": [
                f"The operation '{table1} × {table2}' filters rows where attributes match between the tables.",
                f"A Cartesian product only returns matching tuples from '{table1}' and '{table2}'.",
                f"Cross join ignores tuples with null values and only returns valid pairings."
            ],
            "level2": [
                f"In relational algebra, '{table1} × {table2}' is equivalent to a natural join.",
                f"A cross join merges rows based on matching column names and values in '{table1}' and '{table2}'.",
                f"Cartesian product requires a condition to combine rows from two tables."
            ],
            "level3": [
                f"The cross join between '{table1}' and '{table2}' automatically performs selection on common columns.",
                f"In relational algebra, cross joins are not permitted without a matching key.",
                f"A cross join is identical to a theta join with an equality condition."
            ]
        }

        normalized_level = (level or "").lower()
        if normalized_level not in templates_true:
            normalized_level = "level1"

        is_true = random.choice([True, False])
        question_list = templates_true[normalized_level] if is_true else templates_false[normalized_level]
        question = random.choice(question_list)

        return {
            "type": "TFQ",
            "question": question,
            "level": normalized_level.upper(),
            "answer": "True" if is_true else "False",
        }


    def generate_mcq(self, level=None):
        templates = {
            "level1": [
                f"What relational algebra operation should you use to combine all records from '{self.table1}' and '{self.table2}'?",
                f"To generate a result that pairs every row of '{self.table1}' with every row of '{self.table2}', which operation do you apply?",
                f"Which query performs a Cartesian product of '{self.table1}' and '{self.table2}'?",
                f"You need every possible combination of rows between '{self.table1}' and '{self.table2}'. What query fits?"
            ],
            "level2": [
                f"As a database analyst, how would you express a cross join between '{self.table1}' and '{self.table2}' in relational algebra?",
                f"You are tasked with finding all possible row combinations of '{self.table1}' and '{self.table2}'. Choose the right expression.",
                f"What relational algebra query returns all tuple pairs from '{self.table1}' and '{self.table2}'?",
                f"Which of these expressions correctly denotes a cross join between two tables: '{self.table1}' and '{self.table2}'?"
            ],
            "level3": [
                f"To combine every tuple of '{self.table1}' with each tuple of '{self.table2}' for a complex report, which operation should be used?",
                f"Choose the correct relational algebra representation of a Cartesian product between '{self.table1}' and '{self.table2}'.",
                f"Which relational algebra expression yields the full cross-product of tuples from '{self.table1}' and '{self.table2}'?",
                f"In an advanced query, you're asked to get all row combinations from '{self.table1}' and '{self.table2}'. Select the valid expression."
            ]
        }

        normalized_level = (level or "").lower()
        if normalized_level not in templates:
            normalized_level = "level1"

        selected_templates = templates[normalized_level]

        # Relational algebra for cross join
        correct = f"{self.table1} × {self.table2}"
        wrong1 = f"{self.table1} ⨝ {self.table2}"  # natural join
        wrong2 = f"σ(condition) ({self.table1} ⨝ {self.table2})"  # selection with join
        wrong3 = f"π (columns) ({self.table1} ⨝ {self.table2})"  # projection with join

        options = [correct, wrong1, wrong2, wrong3]
        random.shuffle(options)

        answer = chr(options.index(correct) + ord('a'))
        question = random.choice(selected_templates)

        return {
            "type": "MCQ",
            "options": {chr(i + 97): opt for i, opt in enumerate(options)},
            "question": question,
            "level": normalized_level.upper(),
            "answer": f"({answer})"
        }


    def generate_mtq(self, level=None):
        if not isinstance(self.table_name, (list, tuple)) or len(self.table_name) < 2:
            return None

        table1, table2 = self.table_name[:2]

        mtq_pairs = {
            "level1": [
                (f"Cross join between '{table1}' and '{table2}'", f"{table1} × {table2}"),
                (f"Cartesian product of '{table1}' and '{table2}'", f"{table1} × {table2}"),
                (f"Combines each tuple of '{table1}' with every tuple of '{table2}'", f"{table1} × {table2}"),
                (f"Natural join of '{table1}' and '{table2}'", f"σ_{table1}.{table2}"),  # wrong
                (f"Filters tuples where attributes match in '{table1}' and '{table2}'", f"σ_{table1}.{table2}"),  # wrong
            ],
            "level2": [
                (f"The operation combining tuples from '{table1}' and '{table2}' without any condition", f"{table1} × {table2}"),
                (f"Join operation that returns all possible pairs of tuples between '{table1}' and '{table2}'", f"{table1} × {table2}"),
                (f"Natural join of '{table1}' and '{table2}'", f"{table1} ⨝ {table2}"),  # wrong for cross join
                (f"Selection based join on matching attributes between '{table1}' and '{table2}'", f"σ ({table1}.{table2})"),  # wrong
                (f"Projection of attributes from '{table1}' and '{table2}'", f"π ({table1}, {table2})"),  # wrong
            ],
            "level3": [
                (f"Cross join resulting in the Cartesian product of '{table1}' and '{table2}'", f"{table1} × {table2}"),
                (f"Join without any predicate between '{table1}' and '{table2}'", f"{table1} × {table2}"),
                (f"Equi-join between '{table1}' and '{table2}' on attribute 'id'", f"σ_{table1}.id = {table2}.id ({table1} × {table2})"),  # wrong for pure cross join
                (f"Natural join combining tuples where common attributes match from '{table1}' and '{table2}'", f"{table1} ⨝ {table2}"),  # wrong
                (f"Projection of selected attributes from the join of '{table1}' and '{table2}'", f"π_{table1}.name, {table2}.dept ({table1} × {table2})"),  # wrong for pure cross join
            ],
        }

        # Normalize level and default to level1
        lvl = (level or "level1").lower()
        if lvl not in mtq_pairs:
            lvl = "level1"

        pairs = mtq_pairs[lvl]

        # Separate left and right for matching
        left_items = [p[0] for p in pairs]
        right_items = list(set(p[1] for p in pairs))  # unique expressions

        random.shuffle(left_items)
        random.shuffle(right_items)

        return {
        "type": "MTQ",
        "question": f"Match the descriptions on the left with the correct relational algebra expressions on the right for '{table1}' and '{table2}':",
        "level": lvl.upper(),
        "left_items": left_items,
        "right_items": right_items,
        "pairs": pairs  
    }



    def generate_ecq(self, level=None):
        if not isinstance(self.table_name, (list, tuple)) or len(self.table_name) < 2:
            print(f"[ECQ] Need at least two tables for cross join, got: {self.table_name}")
            return None

        level = level.lower() if isinstance(level, str) else "level1"

        table1, table2 = self.table_name[:2]

        templates = {
            "level1": {
                "question": (
                    f"Explain the result of performing a cross join between tables '{table1}' and '{table2}'."
                ),
                "answer": (
                    f"The cross join between '{table1}' and '{table2}' produces the Cartesian product of the two tables, "
                    f"combining every row of '{table1}' with every row of '{table2}', resulting in all possible row pairs."
                )
            },
            "level2": {
                "question": (
                    f"Describe the characteristics and outcome of a cross join operation between '{table1}' and '{table2}', "
                    f"focusing on the size of the resulting relation."
                ),
                "answer": (
                    f"A cross join between '{table1}' and '{table2}' results in a relation whose number of rows is the product of "
                    f"the number of rows in '{table1}' and '{table2}'. This can create a very large result set depending on the sizes of the tables."
                )
            },
            "level3": {
                "question": (
                    f"Discuss the implications of using a cross join between '{table1}' and '{table2}' in relational algebra, "
                    f"including effects on schema, tuple count, and potential performance considerations."
                ),
                "answer": (
                    f"Performing a cross join between '{table1}' and '{table2}' combines all attributes from both tables into the resulting schema. "
                    f"The number of tuples equals the product of tuples in each table, which can significantly increase query size and impact performance. "
                    f"Careful use of selections or joins with conditions is often needed to manage result size."
                )
            }
        }
        qa = templates.get(level, templates["level1"])

        return {
            "type": "ECQ",
            "level": level.upper(),
            "question": qa["question"],
            "answer": qa["answer"]
        }

    def generate_diq(self, level=None):
        if not isinstance(self.table_name, (list, tuple)) or len(self.table_name) < 2:
            print(f"[DIQ] Need at least two tables for cross join, got: {self.table_name}")
            return None

        level = level.lower() if isinstance(level, str) else "level1"

        table1, table2 = self.table_name[:2]
        symbol = "×"
        expression = f"{table1} {symbol} {table2}"

        templates = {
            "level1": [
                f"Write the relational algebra expression for the cross join of tables '{table1}' and '{table2}'.",
                f"How do you represent the Cartesian product of '{table1}' and '{table2}' using relational algebra?",
                f"Provide the expression to join every tuple of '{table1}' with every tuple of '{table2}'.",
                f"Express the operation that combines all rows from '{table1}' and '{table2}' in relational algebra.",
                f"State the relational algebra syntax for a cross join between '{table1}' and '{table2}'.",
                f"How is the Cartesian product of '{table1}' and '{table2}' represented in relational algebra?"
            ],
            "level2": [
                f"Provide the relational algebra query that returns the Cartesian product of '{table1}' and '{table2}'.",
                f"Write a relational algebra expression that joins '{table1}' and '{table2}' to produce all possible tuple pairs.",
                f"How would you denote the operation combining tuples of '{table1}' and '{table2}' without any condition?",
                f"Formulate the cross join operation between '{table1}' and '{table2}' using relational algebra notation.",
                f"Specify the relational algebra format to retrieve all pairings of rows between '{table1}' and '{table2}'.",
                f"Write the correct algebraic syntax to represent a Cartesian product between '{table1}' and '{table2}'."
            ],
            "level3": [
                f"Express in relational algebra the operation that combines every tuple of '{table1}' with every tuple of '{table2}'.",
                f"Write a detailed relational algebra expression to produce the Cartesian product between '{table1}' and '{table2}', highlighting that no conditions are applied.",
                f"Formulate the operation in relational algebra that results in a relation consisting of all possible combinations of tuples from '{table1}' and '{table2}'.",
                f"Describe the cross join operation between '{table1}' and '{table2}' in relational algebra, which pairs each tuple from one table with all tuples of the other.",
                f"Explain the relational algebra query that leads to a full Cartesian product of rows from '{table1}' and '{table2}'.",
                f"How do you express a Cartesian product in relational algebra that multiplies each tuple of '{table1}' with all tuples of '{table2}'?"
            ]
        }

        selected_question = random.choice(templates.get(level, templates["level1"]))
        tree_mermaid = f"graph TD\n  A[\"{table1}\"] --> C[\"{symbol}\"]\n  B[\"{table2}\"] --> C"

        return {
            "type": "DIQ",
            "level": level.upper(),
            "question": selected_question,
            "expression": expression,
            "answer": expression,
            "tree": tree_mermaid,
            "table1": table1,
            "table2": table2,
            "symbol": symbol
        }


    def generate_oeq(self, level=None):
        if not isinstance(self.table_name, (list, tuple)) or len(self.table_name) < 2:
            print(f"[OEQ] Need at least two tables for cross join, got: {self.table_name}")
            return None

        level = level.lower() if isinstance(level, str) else "level1"

        table1, table2 = self.table_name[:2]

        templates = {
            "level1": [
                f"Explain the meaning of the cross join operation between tables '{table1}' and '{table2}'.",
                f"What is the result of performing a cross join on '{table1}' and '{table2}'?",
                f"Describe in simple terms what happens when you apply the cross join between '{table1}' and '{table2}'."
            ],
            "level2": [
                f"Explain how the cross join operation between '{table1}' and '{table2}' combines tuples from both tables.",
                f"Discuss the effect of a cross join on the number of tuples when joining '{table1}' and '{table2}'.",
                f"Describe the relational algebra operation for cross join on '{table1}' and '{table2}' and its output."
            ],
            "level3": [
                f"Explain in detail the relational algebra cross join operation between '{table1}' and '{table2}', including its impact on the resulting relation schema.",
                f"Describe the cross join operation on '{table1}' and '{table2}' in relational algebra, and discuss scenarios where it is used.",
                f"Discuss the properties and implications of the cross join between '{table1}' and '{table2}', especially focusing on the size and structure of the resulting relation."
            ]
        }

        selected_question = random.choice(templates.get(level, templates["level1"]))

        return {
            "type": "OEQ",
            "level": level.upper(),
            "question": selected_question,
            "answer": (
                f"The cross join (Cartesian product) of tables '{table1}' and '{table2}' "
                f"is a relational algebra operation that combines every tuple of '{table1}' with every tuple of '{table2}', "
                f"resulting in a relation with tuples equal to the product of the number of tuples in each table. "
                f"This operation results in a schema combining attributes from both tables."
            )
        }

    def generate_all_question_types(self, level="level1"):
        output = []
        try:
            question, query = self.generate_bq(level=level)
            output.append({
                "type": "BQ",
                "level": level.upper(),
                "question": question,
                "query": query,
                "answer": query,
            })
        except Exception as e:
            output.append({
                "type": "BQ",
                "error": str(e),
                "level": level.upper()
            })

        for func_name in ["generate_tfq", "generate_mcq", "generate_mtq", "generate_ecq", "generate_diq", "generate_oeq"]:
            try:
                method = getattr(self, func_name)
                result = method(level=level)
                output.append({**result, "type": func_name.split("_")[1].upper()})
            except Exception as e:
                output.append({
                    "type": func_name.split("_")[1].upper(),
                    "error": str(e),
                    "level": level
                })
        return output


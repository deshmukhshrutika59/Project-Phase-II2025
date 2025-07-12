import random
from typing import List, Dict
from schemas.schema import get_schema_by_name

class SetOperationGenerator:
    def __init__(self, table_name, table_schema):
        self.table_name = table_name
        self.table_schema = table_schema
        self.columns = [col for col in table_schema if col != "sample_data"]
        self.sample_data = table_schema.get("sample_data", [])
        self.schema = get_schema_by_name() 

    @staticmethod
    def op_symbol(op):
        return {'union': '∪', 'intersection': '∩', 'minus': '-'}.get(op, '?')
    
    def _get_random_column(self):
        columns = [col for col, meta in self.table_schema.items() if isinstance(meta, dict) and col != "sample_data"]
        return random.choice(columns) if columns else None
    
    def _get_random_value(self, column):
        data = self.table_schema.get("sample_data", [])
        values = [str(row[column]) for row in data if column in row]
        return random.choice(values) if values else "default_value"
    
    def _get_random_other_table(self):
        tables = list(get_schema_by_name().keys())
        other_tables = [tbl for tbl in tables if tbl != self.table_name]
        return random.choice(other_tables) if other_tables else self.table_name

    def _format_value(self, value):
        if isinstance(value, str):
            return f"'{value}'"
        elif isinstance(value, (int, float)):
            return str(value)
        else:
            return "default_value"    

    def get_common_columns(self, table1: str, table2: str) -> List[str]:
        if table1 not in self.schema or table2 not in self.schema:
            return []
        columns1 = set(
            col for col, meta in self.schema[table1].items()
            if isinstance(meta, dict) and col != "sample_data"
        )
        columns2 = set(
            col for col, meta in self.schema[table2].items()
            if isinstance(meta, dict) and col != "sample_data"
        )
        return list(columns1 & columns2)

    def get_sample_value(self, table: str, column: str) -> str:
        if table not in self.schema:
            return "default_value"
        data = self.schema[table].get("sample_data", [])
        values = [str(row[column]) for row in data if column in row]
        return random.choice(values) if values else "default_value"

    def generate_condition_and_value(self, table1: str, table2: str, columns: List[str]) -> tuple:
        attempts = 0
        while attempts < 5:
            column = random.choice(columns)
            val1 = self.get_sample_value(table1, column)
            val2 = self.get_sample_value(table2, column)
            if "default_value" not in (val1, val2):
                chosen_val = val1 if val1 == val2 else random.choice([val1, val2])
                return column, f"{column} = '{chosen_val}'"
            attempts += 1
        return columns[0], f"{columns[0]} IS NOT NULL"


    def _col_phrase(self, col):
        # Simple business-friendly phrasing; expand as needed
        if col.endswith("_id"):
            return f"{col.replace('_', ' ').capitalize()} (ID)"
        elif col == "name":
            return "Name"
        else:
            return col.replace('_', ' ').capitalize()

    def generate_bq(self, set_op_type="union", level=None):
        table1 = self.table_name
        tried_tables = set()
        max_attempts = 10
        schema = get_schema_by_name()

        # Try up to max_attempts to find a compatible table
        for _ in range(max_attempts):
            table2 = self._get_random_other_table()
            if table2 in tried_tables:
                continue
            tried_tables.add(table2)
            # Defensive: check table2 exists and has common columns
            if table2 not in schema:
                continue
            common_columns = self.get_common_columns(table1, table2)
            if common_columns:
                break
        else:
            # Fallback: use any other table, even if no common columns
            table2 = self._get_random_other_table()
            common_columns = self.get_common_columns(table1, table2)

        columns_list = random.sample(common_columns, min(2, len(common_columns))) if common_columns else [self.columns[0]]
        columns_str = ", ".join(columns_list)
        col = columns_list[0] if columns_list else self.columns[0]
        col_phrase = self._col_phrase(col)
        columns_phrase = ", ".join(self._col_phrase(c) for c in columns_list)
        condition = f"{col} IS NOT NULL"

        if isinstance(level, str) and level.lower().startswith("level"):
            level_num = int(level[-1])
        else:
            level_num = int(level) if level else 1

        template = {
            "union": {
                1: [
                    "Show all unique records from both '{table1}' and '{table2}' together.",
                    "Combine every row from '{table1}' and '{table2}', but list each row only once.",
                    "If you want to see all the data from '{table1}' and '{table2}' without any duplicates, which operation would you use?",
                    "How can you merge '{table1}' and '{table2}' so that repeated rows appear only once in the result?",
                    "What is the result if you put together all rows from '{table1}' and '{table2}' and remove duplicates?"
                ],
                2: [
                    "How do you get all unique {col_phrase} values from both '{table1}' and '{table2}'?",
                    "Combine the {col_phrase} values from '{table1}' and '{table2}' so that each value appears only once.",
                    "If you want to see every distinct {col_phrase} from both tables, which operation would you use?",
                    "Show a list of all different {col_phrase} found in either '{table1}' or '{table2}'."
                ],
                3: [
                    "Suppose you filter both '{table1}' and '{table2}' for rows where {condition}, then combine and keep only unique rows for {columns_phrase}. What operation is this?",
                    "How do you get all unique rows with {columns_phrase} from '{table1}' and '{table2}' after filtering for {condition}?",
                    "If you want to merge filtered data from '{table1}' and '{table2}' and remove duplicates, which operation do you use?",
                    "After selecting rows with {condition} from both tables, how can you combine them and keep only one copy of each row with {columns_phrase}?"
                ]
            },
            "intersection": {
                1: [
                    "Show only the records that are present in both '{table1}' and '{table2}'.",
                    "Which rows appear in both '{table1}' and '{table2}'?",
                    "How do you find the data that is shared by both '{table1}' and '{table2}'?",
                    "If you want to see only the common entries between '{table1}' and '{table2}', which operation would you use?",
                    "List the rows that exist in both '{table1}' and '{table2}'."
                ],
                2: [
                    "How can you find the {col_phrase} values that exist in both '{table1}' and '{table2}'?",
                    "Show which {col_phrase} values are present in both tables.",
                    "If you want to see which {col_phrase} values are shared by both '{table1}' and '{table2}', which operation do you use?",
                    "List all {col_phrase} values that are found in both '{table1}' and '{table2}'."
                ],
                3: [
                    "Suppose you filter both '{table1}' and '{table2}' for {condition}, then keep only the rows with {columns_phrase} that are present in both. What operation is this?",
                    "How do you find the common rows with {columns_phrase} from '{table1}' and '{table2}' after filtering for {condition}?",
                    "If you want to see which filtered rows are in both '{table1}' and '{table2}', which operation do you use?",
                    "After selecting rows with {condition}, how can you find the rows with {columns_phrase} that both tables have in common?"
                ]
            },
            "minus": {
                1: [
                    "Show the records that are in '{table1}' but not in '{table2}'.",
                    "Which rows exist in '{table1}' but are missing from '{table2}'?",
                    "How do you find the data that is unique to '{table1}' and not found in '{table2}'?",
                    "If you want to see only the entries from '{table1}' that are not in '{table2}', which operation would you use?",
                    "List all rows from '{table1}' that do not appear in '{table2}'."
                ],
                2: [
                    "How can you get the {col_phrase} values that are in '{table1}' but not in '{table2}'?",
                    "Show which {col_phrase} values are unique to '{table1}' and not found in '{table2}'.",
                    "If you want to see which {col_phrase} values are only in '{table1}', which operation do you use?",
                    "List all {col_phrase} values that are present in '{table1}' but not in '{table2}'."
                ],
                3: [
                    "Suppose you filter both '{table1}' and '{table2}' for {condition}, then keep only the rows with {columns_phrase} that are in '{table1}' but not in '{table2}'. What operation is this?",
                    "How do you find the filtered rows with {columns_phrase} that are unique to '{table1}' after applying {condition}?",
                    "If you want to see which filtered rows are only in '{table1}' and not in '{table2}', which operation do you use?",
                    "After selecting rows with {condition}, how can you find the rows with {columns_phrase} that are only in '{table1}'?"
                ]
            }
        }

        if set_op_type not in template:
            return None

        if level_num == 1:
            question = random.choice(template[set_op_type][1]).format(
                table1=table1, table2=table2
            )
            query = f"({table1} {self.op_symbol(set_op_type)} {table2})"
        elif level_num == 2:
            question = random.choice(template[set_op_type][2]).format(
                table1=table1, table2=table2, column=col, col_phrase=col_phrase
            )
            query = f"π_{{{col}}}({table1}) {self.op_symbol(set_op_type)} π_{{{col}}}({table2})"
        elif level_num == 3:
            question = random.choice(template[set_op_type][3]).format(
                table1=table1, table2=table2, condition=condition, columns=columns_str, columns_phrase=columns_phrase
            )
            query = f"π_{{{columns_str}}}((σ_{{{condition}}}({table1})) {self.op_symbol(set_op_type)} (σ_{{{condition}}}({table2})))"
        else:
            question = f"What is the result of {set_op_type.upper()} between '{table1}' and '{table2}'?"
            query = f"{table1} {self.op_symbol(set_op_type)} {table2}"

        return {"question": question, "answer": query}

    def generate_mcq(self, set_op_type = "union", level=None):
        if not self.columns:
            return None
        
        column = self._get_random_column()
        value = self._get_random_value(column)
        formatted_value = self._format_value(value)
        selected_cols = random.sample(self.columns, min(2, len(self.columns)))
        columns_str = ', '.join(selected_cols)
        condition = f"{column} = {formatted_value}"
        table1 = self.table_name
        table2 = self._get_random_other_table()

        templates = {
            "union": {
                1: [
                    f"What is the result of performing a UNION between '{self.table_name}' and '{table2}'?",
                    f"Explain what happens when we perform a UNION on '{self.table_name}' and '{table2}'.",
                    f"What do we get when we apply a UNION operation between '{self.table_name}' and '{table2}'?"
                ],
                2: [
                    f"What is the outcome when we perform a UNION between '{self.table_name}' and '{table2}' on column '{column}'?",
                    f"Show the result of a UNION between '{self.table_name}' and '{table2}' using the column '{column}'.",
                    f"How does the UNION between '{self.table_name}' and '{table2}' look when using column '{column}'?"
                ],
                3: [
                    f"What is the UNION result between '{self.table_name}' and '{table2}' when projecting columns {columns_str}?",
                    f"Describe what happens when we select rows with {condition} from both '{self.table_name}' and '{table2}', then apply UNION and project columns {columns_str}.",
                    f"Explain the outcome of applying SELECT for {condition} on both '{self.table_name}' and '{table2}', followed by a UNION and projection on columns {columns_str}."
                ]
            },
            "intersection": {
                1: [
                    f"What is the result of performing an INTERSECTION between '{self.table_name}' and '{table2}'?",
                    f"What does an INTERSECTION between '{self.table_name}' and '{table2}' yield?",
                    f"Explain the result of an INTERSECTION between '{self.table_name}' and '{table2}'."
                ],
                2: [
                    f"What is the INTERSECTION result of '{self.table_name}' and '{table2}' on column '{column}'?",
                    f"How does the INTERSECTION of '{self.table_name}' and '{table2}' look using column '{column}'?",
                    f"What happens when we perform an INTERSECTION on '{self.table_name}' and '{table2}' based on column '{column}'?"
                ],
                3: [
                    f"Describe the INTERSECTION between '{self.table_name}' and '{table2}' with projection on columns {columns_str} after selecting rows with {condition}.",
                    f"How does the INTERSECTION of '{self.table_name}' and '{table2}' change when projecting columns {columns_str} after selecting {condition}?",
                    f"What is the result of INTERSECTING '{self.table_name}' and '{table2}' after applying SELECT for {condition} and projecting columns {columns_str}?"
                ]
            },
            "minus": {
                1: [
                    f"What happens when we perform a MINUS operation between '{self.table_name}' and '{table2}'?",
                    f"Describe the result of a MINUS operation between '{self.table_name}' and '{table2}'.",
                    f"What do we get when we subtract '{table2}' from '{self.table_name}' using MINUS?"
                ],
                2: [
                    f"What is the result of MINUS between '{self.table_name}' and '{table2}' using column '{column}'?",
                    f"How does the MINUS operation between '{self.table_name}' and '{table2}' look when using column '{column}'?",
                    f"Describe what happens when we apply a MINUS using column '{column}' between '{self.table_name}' and '{table2}'."
                ],
                3: [
                    f"What happens when we perform a MINUS operation between '{self.table_name}' and '{table2}' after selecting rows with {condition} and projecting {columns_str}?",
                    f"Describe the result of a MINUS between '{self.table_name}' and '{table2}' with SELECT {condition} and projection of columns {columns_str}.",
                    f"Explain the result of MINUS between '{self.table_name}' and '{table2}' after applying SELECT for {condition} and projecting columns {columns_str}."
                ]
            }
        }

        level = int(level) if level in [1, 2, 3] else 1
        if set_op_type not in templates:
            return None

        question = random.choice(templates[set_op_type][level])

        # Correct query depending on set_op_type and level
        if level == 1:
            correct = f"{self.table_name} ∪ {table2}" if set_op_type == "union" else \
                    f"{self.table_name} ∩ {table2}" if set_op_type == "intersection" else \
                    f"{self.table_name} - {table2}"
        elif level == 2:
            correct = f"π_{column}({self.table_name}) {self._op_symbol(set_op_type)} π_{column}({table2})"
        else:  # level 3
            correct = f"π_{{{columns_str}}}(σ_{{{condition}}}({self.table_name}) {self._op_symbol(set_op_type)} σ_{{{condition}}}({table2}))"

        wrong = [
            f"{self.table_name} ⨝ {table2}",
            f"π_{column}({self.table_name}) ⨝ π_{column}({table2})",
            f"σ_{{{condition}}}({self.table_name}) ∪ σ_{{{condition}}}({table2})"
        ]
        options = [correct] + random.sample(wrong, 3)
        random.shuffle(options)
        answer = chr(options.index(correct) + ord('a'))

        return {
            "type": "MCQ",
            "question": question,
            "options": {chr(i + 97): opt for i, opt in enumerate(options)},
            "level": f"LEVEL{level}",
            "answer": f"({answer})"
        }

    def generate_tfq(self,set_op_type = "union", level=None):
        if not self.columns:
            return None

        column = self._get_random_column()
        value = self._get_random_value(column)
        formatted_value = self._format_value(value)
        selected_cols = random.sample(self.columns, min(2, len(self.columns)))
        columns_str = ', '.join(selected_cols)
        condition = f"{column} = {formatted_value}"
        table1 = self.table_name
        table2 = self._get_random_other_table()

        tf_templates = {
            "union": {
                1: [
                    (f"The UNION operation between '{self.table_name}' and '{table2}' returns all rows from both tables, including duplicates.", False),
                    (f"UNION combines rows from '{self.table_name}' and '{table2}' and removes duplicates by default.", True),
                    (f"The result of a UNION always contains more rows than either of the original tables.", False)
                ],
                2: [
                    (f"π_{column}({self.table_name}) ∪ π_{column}({table2}) returns unique values of '{column}' from both tables.", True),
                    (f"π_{column}({self.table_name}) ∪ π_{column}({table2}) includes duplicate rows of '{column}'.", False)
                ],
                3: [
                    (f"π_{{{columns_str}}}(σ_{{{condition}}}({self.table_name}) ∪ σ_{{{condition}}}({table2})) returns rows from both tables where {condition} holds true.", True),
                    (f"σ_{{{condition}}}({self.table_name}) ∪ σ_{{{condition}}}({table2}) ignores the condition when performing the UNION.", False)
                ]
            },
            "intersection": {
                1: [
                    (f"The INTERSECTION of '{self.table_name}' and '{table2}' returns rows that exist in both tables.", True),
                    (f"INTERSECTION between two tables returns all rows from the first table.", False),
                    (f"INTERSECTION includes rows only present in one of the tables.", False)
                ],
                2: [
                    (f"π_{column}({self.table_name}) ∩ π_{column}({table2}) returns shared values of '{column}' from both tables.", True),
                    (f"π_{column}({self.table_name}) ∩ π_{column}({table2}) gives a Cartesian product.", False)
                ],
                3: [
                    (f"π_{{{columns_str}}}(σ_{{{condition}}}({self.table_name}) ∩ σ_{{{condition}}}({table2})) gives common rows where {condition} is true in both tables.", True),
                    (f"The result of INTERSECTION ignores the condition applied before the operation.", False)
                ]
            },
            "minus": {
                1: [
                    (f"The MINUS operation returns rows from '{self.table_name}' that are not in '{table2}'.", True),
                    (f"MINUS returns the union of both tables.", False),
                    (f"MINUS and INTERSECTION are interchangeable operations.", False)
                ],
                2: [
                    (f"π_{column}({self.table_name}) - π_{column}({table2}) returns values present in '{self.table_name}' but not in '{table2}'.", True),
                    (f"π_{column}({self.table_name}) - π_{column}({table2}) performs row duplication.", False)
                ],
                3: [
                    (f"π_{{{columns_str}}}(σ_{{{condition}}}({self.table_name}) - σ_{{{condition}}}({table2})) filters rows by {condition} and returns those unique to '{self.table_name}'.", True),
                    (f"The result of a MINUS operation always includes rows from both tables.", False)
                ]
            }
        }

        level = int(level) if level in [1, 2, 3] else 1
        if set_op_type not in tf_templates:
            return None

        tf_list = tf_templates[set_op_type][level]
        question_text, truth_value = random.choice(tf_list)

        return {
            "type": "TFQ",
            "question": question_text,
            "level": f"LEVEL{level}",
            "answer": "(T)" if truth_value else "(F)"
        }

    def generate_mtq(self, set_op_type = "union", level=None):
        if not self.columns:
            return None

        column = self._get_random_column()
        value = self._get_random_value(column)
        formatted_value = self._format_value(value)
        selected_cols = random.sample(self.columns, min(2, len(self.columns)))
        columns_str = ', '.join(selected_cols)
        condition = f"{column} = {formatted_value}"
        table1 = self.table_name
        table2 = self._get_random_other_table()

        mtq_templates = {
            "union": {
                1: [
                    ("UNION removes duplicate rows between two tables.", True),
                    ("UNION includes all rows from both tables without eliminating duplicates.", False),
                    ("The UNION operation is symmetric.", True),
                    ("UNION returns only the rows present in both tables.", False)
                ],
                2: [
                    (f"π_{column}({self.table_name}) ∪ π_{column}({table2}) gives unique values of '{column}' from both tables.", True),
                    (f"π_{column}({self.table_name}) ∪ π_{column}({table2}) allows duplicate values in the result.", False),
                    ("UNION requires both relations to have the same number and type of columns.", True),
                    ("UNION can be applied between tables with different numbers of columns.", False)
                ],
                3: [
                    (f"σ_{{{condition}}}({self.table_name}) ∪ σ_{{{condition}}}({table2}) returns rows from both tables that satisfy {condition}.", True),
                    ("The result of UNION is the same as the Cartesian product.", False),
                    ("You must manually remove duplicates after UNION in relational algebra.", False),
                    ("UNION applies set semantics and removes duplicates by default.", True)
                ]
            },
            "intersection": {
                1: [
                    ("INTERSECTION includes only rows that exist in both input tables.", True),
                    ("INTERSECTION returns all unique rows from both tables.", False),
                    ("INTERSECTION is a commutative operation.", True),
                    ("INTERSECTION includes duplicates from both tables.", False)
                ],
                2: [
                    (f"π_{column}({self.table_name}) ∩ π_{column}({table2}) gives shared '{column}' values.", True),
                    (f"π_{column}({self.table_name}) ∩ π_{column}({table2}) lists all distinct values from both tables.", False),
                    ("INTERSECTION requires the same schema in both relations.", True),
                    ("INTERSECTION can be used with tables having different attributes.", False)
                ],
                3: [
                    (f"σ_{{{condition}}}({self.table_name}) ∩ σ_{{{condition}}}({table2}) gives tuples satisfying {condition} in both tables.", True),
                    ("INTERSECTION ignores matching tuples and only keeps differences.", False),
                    ("INTERSECTION is identical to JOIN in all cases.", False),
                    ("INTERSECTION may return an empty set if there is no overlap.", True)
                ]
            },
            "minus": {
                1: [
                    ("MINUS returns tuples from the first relation that are not in the second.", True),
                    ("MINUS adds new tuples to the second table.", False),
                    ("MINUS is not a commutative operation.", True),
                    ("MINUS operation is the same as INTERSECTION.", False)
                ],
                2: [
                    (f"π_{column}({self.table_name}) - π_{column}({table2}) returns '{column}' values only in '{self.table_name}'.", True),
                    ("MINUS includes all rows from both tables.", False),
                    ("MINUS requires schema compatibility between relations.", True),
                    ("MINUS preserves duplicates in the output.", False)
                ],
                3: [
                    (f"σ_{{{condition}}}({self.table_name}) - σ_{{{condition}}}({table2}) filters rows unique to '{self.table_name}'.", True),
                    ("MINUS behaves exactly like UNION.", False),
                    ("MINUS can be used to exclude specific rows from a dataset.", True),
                    ("MINUS returns rows common to both relations.", False)
                ]
            }
        }

        level = int(level) if level in [1, 2, 3] else 1
        if set_op_type not in mtq_templates:
            return None

        mtq_set = mtq_templates[set_op_type][level]
        random.shuffle(mtq_set)

        # Create options and answers dictionaries
        options = {chr(97 + i): stmt for i, (stmt, truth) in enumerate(mtq_set)}
        answers = {chr(97 + i): "True" if truth else "False" for i, (stmt, truth) in enumerate(mtq_set)}

        # Build formatted question string including options and answers
        options_text = "\n".join(f"{key}) {text}" for key, text in options.items())
        answers_text = "\n".join(f"{key}) {ans}" for key, ans in answers.items())

        question_text = (
            f"Identify whether the following statements about the {set_op_type.upper()} operation are True or False:\n\n"
            f"{options_text}\n\n"
            f"Answers:\n{answers_text}"
        )

        correct_answers = [k for k, v in answers.items() if v == "True"]
        return {
            "type": "MTQ",
            "question": question_text,
            "level": f"LEVEL{level}",
            "answer": f"{', '.join(correct_answers)}"
        }



    def generate_ecq(self,set_op_type = "union", level=None):
        if not self.columns:
            return None

        column = self._get_random_column()
        selected_cols = random.sample(self.columns, min(2, len(self.columns)))
        columns_str = ', '.join(selected_cols)
        table1 = self.table_name
        table2 = self._get_random_other_table()

        # Question templates per operation and level
        ecq_questions = {
            "union": {
                1: [
                    f"Explain the purpose of the UNION operation in relational algebra. How does it affect duplicates when combining data from '{self.table_name}' and '{table2}'?",
                    f"What is the main function of UNION in combining relations like '{self.table_name}' and '{table2}'?",
                ],
                2: [
                    f"Why must '{self.table_name}' and '{table2}' have compatible schemas when performing a UNION? Illustrate your answer using attributes like '{column}'.",
                    f"Explain the importance of schema compatibility for UNION operation between '{self.table_name}' and '{table2}'.",
                ],
                3: [
                    f"Given π({columns_str})({self.table_name}) ∪ π({columns_str})({table2}), explain the result and what happens if some rows appear in both tables.",
                    f"Describe the outcome when UNION is applied to π({columns_str})({self.table_name}) and π({columns_str})({table2}) and overlapping rows exist."
                ],
            },
            "intersection": {
                1: [
                    f"What is the purpose of the INTERSECTION operation in relational algebra, and how does it differ from UNION when comparing '{self.table_name}' and '{table2}'?",
                    f"How does INTERSECTION between '{self.table_name}' and '{table2}' differ from UNION?",
                ],
                2: [
                    f"Explain how INTERSECTION identifies common tuples between '{self.table_name}' and '{table2}'. What must be true about their schemas?",
                    f"Why is schema compatibility required for INTERSECTION between '{self.table_name}' and '{table2}'?",
                ],
                3: [
                    f"Consider π({columns_str})({self.table_name}) ∩ π({columns_str})({table2}). What result do you expect? Provide a practical use case.",
                    f"Describe the result and a real-world application of π({columns_str})({self.table_name}) ∩ π({columns_str})({table2}).",
                ],
            },
            "minus": {
                1: [
                    f"Describe the effect of the MINUS operation on '{self.table_name}' and '{table2}'. What data is excluded?",
                    f"What does MINUS operation between '{self.table_name}' and '{table2}' accomplish?",
                ],
                2: [
                    f"Explain the behavior of π({columns_str})({self.table_name}) - π({columns_str})({table2}) in filtering data.",
                    f"How does π({columns_str})({self.table_name}) - π({columns_str})({table2}) filter data from the first relation?",
                ],
                3: [
                    f"In σ(condition)({self.table_name}) - σ(condition)({table2}), what rows remain after MINUS and why?",
                    f"Explain the result of MINUS after selection conditions applied to '{self.table_name}' and '{table2}'.",
                ],
            },
        }

        # Answer templates per operation and level
        ecq_answers = {
            "union": {
                1: [
                    f"UNION combines tuples from '{self.table_name}' and '{table2}', removing duplicates to provide a unified set of unique rows.",
                    f"The UNION operation merges data from both relations and eliminates duplicate tuples by default."
                ],
                2: [
                    f"'{self.table_name}' and '{table2}' must have compatible schemas for UNION so that attributes like '{column}' match in type and position, allowing tuples to be combined correctly.",
                    f"Schema compatibility ensures UNION operates correctly by aligning attributes such as '{column}' between '{self.table_name}' and '{table2}'."
                ],
                3: [
                    f"π({columns_str})({self.table_name}) ∪ π({columns_str})({table2}) results in a relation containing unique tuples projected from both tables. Rows appearing in both are included once.",
                    f"When some rows appear in both tables, UNION outputs those rows only once in the combined relation."
                ],
            },
            "intersection": {
                1: [
                    f"INTERSECTION returns only tuples that are present in both '{self.table_name}' and '{table2}', unlike UNION which returns all unique tuples from both.",
                    f"The INTERSECTION operation finds common tuples shared by both relations."
                ],
                2: [
                    f"INTERSECTION requires identical schemas so tuples can be accurately compared and matched between '{self.table_name}' and '{table2}'.",
                    f"Schema compatibility is crucial for INTERSECTION to identify and return common tuples."
                ],
                3: [
                    f"π({columns_str})({self.table_name}) ∩ π({columns_str})({table2}) returns tuples projected from both relations that exist in both. For example, students enrolled in both courses.",
                    f"This operation helps find entities like students who are common to both course enrollments."
                ],
            },
            "minus": {
                1: [
                    f"MINUS returns tuples from '{self.table_name}' that are not found in '{table2}', effectively excluding shared data.",
                    f"MINUS operation filters out any tuples present in '{table2}' from '{self.table_name}'."
                ],
                2: [
                    f"π({columns_str})({self.table_name}) - π({columns_str})({table2}) projects columns from both and removes tuples found in '{table2}' from '{self.table_name}'.",
                    f"This operation filters the first relation by subtracting tuples existing in the second relation."
                ],
                3: [
                    f"σ(condition)({self.table_name}) - σ(condition)({table2}) returns rows from '{self.table_name}' satisfying the condition but not found in '{table2}'.",
                    f"After applying conditions, MINUS leaves only rows unique to the first relation that satisfy the condition."
                ],
            },
        }

        level = int(level) if level in [1, 2, 3] else 1
        if set_op_type not in ecq_questions:
            return None

        question = random.choice(ecq_questions[set_op_type][level])
        answer = random.choice(ecq_answers[set_op_type][level])

        return {
            "type": "ECQ",
            "question": question,
            "level": f"LEVEL{level}",
            "answer": answer
        }


    def generate_diq(self, set_op_type="union", level=None):
        table1 = self.table_name
        table2 = self._get_random_other_table()
        table2_data = get_schema_by_name().get(table2, {}).get("sample_data", [])

        # Fallback: If not enough data, return a conceptual DIQ with tree
        if not self.sample_data or not table2_data:
            return {
                "type": "DIQ",
                "question": f"Draw or describe the relational algebra tree for the {set_op_type.upper()} operation between '{table1}' and '{table2}'.",
                "level": f"LEVEL{level if level else 1}",
                "answer": f"{table1} {self.op_symbol(set_op_type)} {table2}",
                "tree": f"{table1}\n{self.op_symbol(set_op_type)}\n{table2}"
            }

        # Try to select columns that exist in most rows
        all_columns = set(self.columns)
        for row in self.sample_data:
            all_columns &= set(row.keys())
        for row in table2_data:
            all_columns &= set(row.keys())
        selected_cols = list(all_columns) if all_columns else self.columns[:1]
        columns_str = ', '.join(selected_cols)

        data1 = [{col: row[col] for col in selected_cols if col in row} for row in self.sample_data[:3]]
        data2 = [{col: row[col] for col in selected_cols if col in row} for row in table2_data[:3]]
        data1 = [row for row in data1 if len(row) == len(selected_cols)]
        data2 = [row for row in data2 if len(row) == len(selected_cols)]

        # Fallback: If still not enough data, return a conceptual DIQ with tree
        if not data1 or not data2:
            return {
                "type": "DIQ",
                "question": f"Draw or describe the relational algebra tree for the {set_op_type.upper()} operation between '{table1}' and '{table2}'.",
                "level": f"LEVEL{level if level else 1}",
                "answer": f"{table1} {self.op_symbol(set_op_type)} {table2}",
                "tree": f"{table1}\n{self.op_symbol(set_op_type)}\n{table2}"
            }

        # Convert to sets for set operations
        set1 = set(tuple(row.items()) for row in data1)
        set2 = set(tuple(row.items()) for row in data2)
        if not set1 or not set2:
            return {
                "type": "DIQ",
                "question": f"Draw or describe the relational algebra tree for the {set_op_type.upper()} operation between '{table1}' and '{table2}'.",
                "level": f"LEVEL{level if level else 1}",
                "answer": f"{table1} {self.op_symbol(set_op_type)} {table2}",
                "tree": f"{table1}\n{self.op_symbol(set_op_type)}\n{table2}"
            }

        union_result = set1 | set2
        intersection_result = set1 & set2
        minus_result = set1 - set2

        def format_table(data, name):
            if not data:
                return f"{name}: (empty table)"
            rows = [", ".join(f"{k}={repr(v)}" for k, v in row.items()) for row in data]
            return f"{name}:\n  " + "\n  ".join(rows)

        def set_to_readable(s):
            return [dict(tup) for tup in s]

        def format_result(result_set):
            return "\n  " + "\n  ".join(", ".join(f"{k}={v!r}" for k, v in row.items()) for row in set_to_readable(result_set))

        table1_str = format_table(data1, self.table_name)
        table2_str = format_table(data2, table2)

        base_prompt = f"{table1_str}\n\n{table2_str}\n\nBased on the above data, "

        level = int(level) if level in [1, 2, 3] else 1
        readable_union = set_to_readable(union_result)
        readable_intersection = set_to_readable(intersection_result)
        readable_minus = set_to_readable(minus_result)

        # Pick a random tuple from each result set if available
        def pick_random_tuple(result_set):
            readable = set_to_readable(result_set)
            return random.choice(readable) if readable else None

        # Build a variety of question/answer templates
        diq_varieties = []

        # 1. How many unique tuples?
        diq_varieties.append({
            "q": f"{base_prompt}how many unique tuples will result from a {set_op_type.upper()} of '{self.table_name}' and '{table2}'?",
            "a": f"Answer: {len(union_result) if set_op_type=='union' else len(intersection_result) if set_op_type=='intersection' else len(minus_result)} unique tuples."
        })

        # 2. List all tuples in the result
        diq_varieties.append({
            "q": f"{base_prompt}list all tuples in the result of {set_op_type.upper()} between '{self.table_name}' and '{table2}'.",
            "a": f"Answer:{format_result(union_result if set_op_type=='union' else intersection_result if set_op_type=='intersection' else minus_result)}"
        })

        # 3. Is a specific tuple present in the result?
        for result_set, op_name in [(union_result, "UNION"), (intersection_result, "INTERSECTION"), (minus_result, "MINUS")]:
            tup = pick_random_tuple(result_set)
            if tup:
                tuple_str = ", ".join(f"{k}={v!r}" for k, v in tup.items())
                diq_varieties.append({
                    "q": f"{base_prompt}is the tuple ({tuple_str}) present in the result of {op_name}?",
                    "a": f"Answer: {'Yes' if set_op_type == op_name.lower() else 'No'}"
                })

        # 4. Which tuples are NOT in the result?
        all_tuples = set1 | set2
        not_in_result = all_tuples - (union_result if set_op_type == "union" else intersection_result if set_op_type == "intersection" else minus_result)
        tup = pick_random_tuple(not_in_result)
        if tup:
            tuple_str = ", ".join(f"{k}={v!r}" for k, v in tup.items())
            diq_varieties.append({
                "q": f"{base_prompt}is the tuple ({tuple_str}) present in the result of {set_op_type.upper()}?",
                "a": "Answer: No"
            })

        # 5. What is the first tuple in the result?
        readable = set_to_readable(union_result if set_op_type == "union" else intersection_result if set_op_type == "intersection" else minus_result)
        if readable:
            tuple_str = ", ".join(f"{k}={v!r}" for k, v in readable[0].items())
            diq_varieties.append({
                "q": f"{base_prompt}what is the first tuple in the result of {set_op_type.upper()}?",
                "a": f"Answer: ({tuple_str})"
            })

        # 6. Which set_op_type would result in the most tuples?
        counts = {
            "UNION": len(union_result),
            "INTERSECTION": len(intersection_result),
            "MINUS": len(minus_result)
        }
        max_op = max(counts, key=counts.get)
        diq_varieties.append({
            "q": f"{base_prompt}which set operation (UNION, INTERSECTION, MINUS) would result in the most tuples?",
            "a": f"Answer: {max_op} ({counts[max_op]} tuples)"
        })

        # Randomly select a DIQ variety for this call
        if diq_varieties:
            chosen = random.choice(diq_varieties)
            # Add a tree field for visualization
            chosen["tree"] = f"{table1}\n{self.op_symbol(set_op_type)}\n{table2}"
            chosen["type"] = "DIQ"
            chosen["level"] = f"LEVEL{level if level else 1}"
            chosen["answer"] = chosen.pop("a")  # Ensure answer is under 'answer'
            chosen["question"] = chosen.pop("q")  # Ensure question is under 'question'
            return chosen
        else:
            # Fallback: conceptual DIQ
            return {
                "type": "DIQ",
                "question": f"Draw or describe the relational algebra tree for the {set_op_type.upper()} operation between '{table1}' and '{table2}'.",
                "level": f"LEVEL{level if level else 1}",
                "answer": f"{table1} {self.op_symbol(set_op_type)} {table2}",
                "tree": f"{table1}\n{self.op_symbol(set_op_type)}\n{table2}"
            }
    
    def generate_oeq(self,set_op_type = "union", level=None):
        if not self.columns:
            return None

        selected_cols = random.sample(self.columns, min(2, len(self.columns)))
        cols_str = ', '.join(selected_cols)
        level = int(level) if level in [1, 2, 3] else 1
        table1 = self.table_name
        table2 = self._get_random_other_table()

        templates = {
            "union": {
                1: [
                    f"What does the UNION of all rows in '{self.table_name}' and '{table2}' represent?",
                    f"Explain the outcome of applying UNION to '{self.table_name}' and '{table2}'."
                ],
                2: [
                    f"Describe the result of the expression π({cols_str})({self.table_name}) ∪ π({cols_str})({table2}).",
                    f"What kind of data is preserved when applying UNION on two relations with the same schema?"
                ],
                3: [
                    f"How would a UNION operation behave when one relation has duplicate entries also found in another? Describe with reference to π({cols_str})({self.table_name}) ∪ π({cols_str})({table2}).",
                    f"In what scenarios would UNION lead to data redundancy removal? Explain with respect to relational algebra."
                ]
            },
            "intersection": {
                1: [
                    f"What does the INTERSECTION of '{self.table_name}' and '{table2}' retrieve?",
                    f"Explain what information is retained in the result of an INTERSECTION operation."
                ],
                2: [
                    f"Describe the outcome of π({cols_str})({self.table_name}) ∩ π({cols_str})({table2}).",
                    f"When would INTERSECTION result in an empty set? Provide reasoning."
                ],
                3: [
                    f"Discuss the semantics of INTERSECTION when applied to relations with constraints (e.g., Age > 20).",
                    f"What considerations must be taken into account when intersecting two relations with overlapping values but different tuples?"
                ]
            },
            "minus": {
                1: [
                    f"What result is produced by applying the MINUS operation: '{self.table_name}' - '{table2}'?",
                    f"Describe the meaning of MINUS in relational algebra using the two relations."
                ],
                2: [
                    f"What does the query π({cols_str})({self.table_name}) - π({cols_str})({table2}) do?",
                    f"Which tuples are retained when a MINUS operation is applied between two relations?"
                ],
                3: [
                    f"Explain how MINUS works when both relations contain overlapping and unique values. Use a theoretical example.",
                    f"In what scenarios might the result of a MINUS operation be identical to the original relation? Justify."
                ]
            }
        }

        if set_op_type not in templates:
            return None

        question_text = random.choice(templates[set_op_type][level])

        # Generate the dynamic answer based on set_op_type and level
        if set_op_type == "union":
            if level == 1:
                answer = f"UNION combines all tuples from both '{self.table_name}' and '{table2}', removing duplicates."
            elif level == 2:
                answer = f"The query π({cols_str})({self.table_name}) ∪ π({cols_str})({table2}) returns all unique rows with columns {cols_str} from both relations."
            else:  # level 3
                answer = f"UNION removes redundancy; if both relations have identical rows, duplicates are removed in the result."

        elif set_op_type == "intersection":
            if level == 1:
                answer = f"INTERSECTION retrieves only the tuples that are present in both '{self.table_name}' and '{table2}'."
            elif level == 2:
                answer = f"The query π({cols_str})({self.table_name}) ∩ π({cols_str})({table2}) returns common tuples on columns {cols_str}."
            else:  # level 3
                answer = f"When constraints are added (e.g., filters), INTERSECTION gives rows that satisfy both constraints and exist in both relations."

        elif set_op_type == "minus":
            if level == 1:
                answer = f"MINUS yields the tuples in '{self.table_name}' that are not present in '{table2}'."
            elif level == 2:
                answer = f"The expression π({cols_str})({self.table_name}) - π({cols_str})({table2}) removes rows that exist in both from '{self.table_name}'."
            else:  # level 3
                answer = f"If none of the tuples in '{self.table_name}' are present in '{table2}', then MINUS returns all tuples of '{self.table_name}'."

        else:
            answer = "Relational algebra set operation."

        # Make sure to return with consistent keys
        return {
            "type": "OEQ",
            "question": question_text,
            "level": f"LEVEL{level}",
            "answer": answer  # Changed key from 'answer_guide' to 'answer' for clarity
        }

    def generate_all_question_types(self, level="level1", set_op_type=None):
        output = []
        try:
            bq = self.generate_bq(level=level, set_op_type=set_op_type)
            output.append({**bq, "type": "BQ"})
        except Exception as e:
            output.append({"type": "BQ", "error": str(e), "level": level})

        for func_name in ["generate_tfq", "generate_mcq", "generate_mtq", "generate_ecq", "generate_diq", "generate_oeq"]:
            try:
                method = getattr(self, func_name)
                result = method(level=level, set_op_type=set_op_type)
                result["type"] = func_name.split("_")[1].upper()
                result["level"] = level.upper()
                output.append(result)
            except Exception as e:
                output.append({
                    "type": func_name.split("_")[1].upper(),
                    "error": str(e),
                    "level": level.upper()
                })

        return output
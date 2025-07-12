import random

class QueryTreeGenerator:
    def __init__(self, table_name, table_schema, related_tables=None):
        self.table_name = table_name
        self.schema = table_schema
        self.related_tables = related_tables or {}

        # Only columns that are dicts (not PK/FK lists or sample_data)
        self.columns = [col for col in table_schema if isinstance(table_schema[col], dict) and col != "sample_data"]
        self.columns_dict = {
            col: details for col, details in table_schema.items()
            if isinstance(details, dict) and "type" in details
        }
        self.sample_data = table_schema.get("sample_data", [])

    def _random_column(self):
        cols = [col for col in self.columns if isinstance(self.schema.get(col, {}), dict)]
        return random.choice(cols) if cols else None

    def _random_condition(self, column):
        col_info = self.schema.get(column, {})
        if not isinstance(col_info, dict):
            return f"{column} = 'value'"
        col_type = col_info.get("type", "string")
        if col_type in ("int", "float"):
            val = random.randint(1, 100)
            op = random.choice([">", "<", ">=", "<=", "="])
            return f"{column} {op} {val}"
        elif col_type == "string":
            val = "'some_value'"
            op = random.choice(["=", "!="])
            return f"{column} {op} {val}"
        else:
            return f"{column} = 'value'"

    def _get_sample_value(self, col):
        sample_data = self.schema.get("sample_data", [])
        if isinstance(sample_data, list):
            return [row[col] for row in sample_data if col in row]
        return []

    def _generate_condition(self):
        for col in self.columns_dict:
            values = self._get_sample_value(col)
            if values:
                value = random.choice(values)
                col_type = self.columns_dict[col]["type"]
                if col_type in ["int", "float"]:
                    return f"{col} > {value}"
                elif col_type == "string":
                    return f"{col} = '{value}'"
        return f"{random.choice(list(self.columns_dict))} IS NOT NULL"


    def _col_phrase(self, col):
        if col.endswith("_id"):
            return f"{col.replace('_', ' ').capitalize()} (ID)"
        elif col == "name":
            return "Name"
        else:
            return col.replace('_', ' ').capitalize()

    def generate_bq(self, level="level1"):
        if not self.columns_dict or not self.sample_data:
            return None

        col_list = list(self.columns_dict.keys())
        selected_cols = random.sample(col_list, min(2, len(col_list)))
        cols_str = ', '.join(selected_cols)
        cols_phrase = ', '.join(self._col_phrase(c) for c in selected_cols)
        condition = self._generate_condition()

        templates = {
            "level1": [
                f"Can you construct the query tree for showing {cols_phrase} from the '{self.table_name}' table?",
                f"Build the relational algebra tree that retrieves only {cols_phrase} from '{self.table_name}'.",
                f"Draw a query tree that simply extracts {cols_phrase} from the '{self.table_name}' relation.",
                f"Show the query tree that performs a basic projection on {cols_phrase} for all tuples in '{self.table_name}'.",
                f"What would the projection tree look like for retrieving {cols_phrase} from the '{self.table_name}' table?"
            ],
            "level2": [
                f"Construct a query tree that selects rows from '{self.table_name}' where {condition}, and then shows {cols_phrase}.",
                f"Draw a query tree for selecting and projecting {cols_phrase} from '{self.table_name}', filtered by the condition: {condition}.",
                f"Generate a query tree that applies selection on '{self.table_name}' with {condition} before showing {cols_phrase}.",
                f"Write the relational algebra tree that filters '{self.table_name}' on {condition} and retrieves only {cols_phrase}.",
                f"Visualize a query tree where we select tuples from '{self.table_name}' satisfying {condition} and then show {cols_phrase}."
            ],
            "level3": []
        }

        # Add Level 3 templates only if related_tables exist
        if self.related_tables:
            for join_table in self.related_tables:
                join_cols = list(set(col_list) & set(self.related_tables[join_table].keys()))
                join_col = join_cols[0] if join_cols else "id"
                join_col_phrase = self._col_phrase(join_col)
                templates["level3"].extend([
                    f"Create a query tree for joining '{self.table_name}' and '{join_table}' on {self.table_name}.{join_col_phrase} = {join_table}.{join_col_phrase}, then select rows where {condition}, and finally show {cols_phrase}.",
                    f"Draw the query tree for a join between '{self.table_name}' and '{join_table}', followed by a selection on {condition}, and showing {cols_phrase}.",
                    f"Build a query tree combining join, selection, and projection using '{self.table_name}' and '{join_table}' on the column '{join_col_phrase}' and filter with {condition}.",
                    f"Generate a relational algebra tree for: join '{self.table_name}' ⨝ '{join_table}', then σ {condition}, and then π {cols_phrase}.",
                    f"What is the query tree for joining '{self.table_name}' and '{join_table}', filtering the result using {condition}, and showing {cols_phrase}?"
                ])

        if level == "level1":
            question = random.choice(templates["level1"])
            query = f"π {cols_str} ({self.table_name})"
            tree = f"""
    π {cols_str}
    |
    {self.table_name}
    """.strip()
            answer = f"Shows the columns {cols_phrase} from all tuples in '{self.table_name}'."

        elif level == "level2":
            question = random.choice(templates["level2"])
            query = f"π {cols_str} (σ {condition} ({self.table_name}))"
            tree = f"""
    π {cols_str}
    |
    σ {condition}
    |
    {self.table_name}
    """.strip()
            answer = f"Selects rows from '{self.table_name}' where {condition}, then shows the columns {cols_phrase}."

        elif level == "level3":
            if self.related_tables:
                join_table = random.choice(list(self.related_tables.keys()))
                join_cols = list(set(col_list) & set(self.related_tables[join_table].keys()))
                join_col = join_cols[0] if join_cols else "id"
                join_col_phrase = self._col_phrase(join_col)

                question = random.choice(templates["level3"])
                query = (f"π {cols_str} (σ {condition} ({self.table_name} ⨝ "
                        f"{self.table_name}.{join_col} = {join_table}.{join_col} {join_table}))")
                tree = f"""
    π {cols_str}
    |
    σ {condition}
    |
    ⨝ {self.table_name}.{join_col} = {join_table}.{join_col}
    /   \\
    {self.table_name}   {join_table}
    """.strip()
                answer = (
                    f"Joins '{self.table_name}' and '{join_table}' on {self.table_name}.{join_col_phrase} = {join_table}.{join_col_phrase}, "
                    f"selects rows where {condition}, then shows the columns {cols_phrase}."
                )
            else:
                question = (
                    f"Construct a query tree for the following: "
                    f"rename '{self.table_name}' to 'T1', select rows where {condition}, then show {cols_phrase}."
                )
                query = f"π {cols_str} (σ {condition} (ρ T1 ({self.table_name})))"
                tree = f"""
    π {cols_str}
    |
    σ {condition}
    |
    ρ T1
    |
    {self.table_name}
    """.strip()
                answer = (
                    f"Renames '{self.table_name}' to 'T1', selects rows where {condition}, then shows the columns {cols_phrase}."
                )
        else:
            return None

        return {
            "question": question,
            "query": query,
            "tree": tree,
            "answer": answer
        }
    # --- Relational Algebra Question Types ---
    def generate_tfq(self, level=None):
        if not self.columns:
            return None
        selected_cols = random.sample(self.columns, min(2, len(self.columns)))
        cols_str = ', '.join(selected_cols)
        example_conditions = [
            f"{selected_cols[0]} = 'ExampleValue'",
            f"{selected_cols[0]} > 10",
            f"{selected_cols[0]} != {selected_cols[1]}" if len(selected_cols) > 1 else f"{selected_cols[0]} != 'Value'"
        ]
        condition = random.choice(example_conditions) if level in ["level2", "level3"] else None
        templates = {
            "level1": [
                f"The relational algebra query π ({cols_str}) ({self.table_name}) projects only the columns {cols_str} from the table '{self.table_name}'. True or False?",
                f"In the query π ({cols_str}) ({self.table_name}), the columns {cols_str} are selected from '{self.table_name}'. Is this statement true or false?",
                f"The projection operation π on '{self.table_name}' with columns {cols_str} extracts exactly those columns. True or False?",
                f"The query π ({cols_str}) ({self.table_name}) returns all rows but only the columns {cols_str} from '{self.table_name}'. True or False?"
            ],
            "level2": [
                f"The query π ({cols_str}) (σ ({condition}) ({self.table_name})) applies a filter condition before projecting columns {cols_str} from '{self.table_name}'. True or False?",
                f"In the relational algebra expression π ({cols_str}) (σ ({condition}) ({self.table_name})), the selection condition is applied after the projection. True or False?",
                f"The query π ({cols_str}) (σ ({condition}) ({self.table_name})) filters rows where {condition} before projecting {cols_str}. True or False?",
                f"Selection and projection can be combined as π ({cols_str}) (σ ({condition}) ({self.table_name})) to filter and then project columns. True or False?"
            ],
            "level3": [
                f"The relational algebra query π ({cols_str}) (σ ({condition}) ({self.table_name})) first projects the columns {cols_str} and then filters by {condition}. True or False?",
                f"In π ({cols_str}) (σ ({condition}) ({self.table_name})), the order of operations is selection followed by projection. True or False?",
                f"The query π ({cols_str}) (σ ({condition}) ({self.table_name})) cannot be simplified into a single operation without changing the result. True or False?",
                f"Applying projection before selection in π ({cols_str}) (σ ({condition}) ({self.table_name})) will produce the same output. True or False?"
            ]
        }
        normalized_level = (level or "").lower()
        if normalized_level not in templates:
            normalized_level = "level1"
        selected_templates = templates[normalized_level]
        question = random.choice(selected_templates)
        if normalized_level == "level1":
            correct_answer = "True"
        elif normalized_level == "level2":
            correct_answer = "False" if "after the projection" in question else "True"
        else:
            if any(phrase in question for phrase in ["first projects", "Applying projection before selection"]):
                correct_answer = "False"
            else:
                correct_answer = "True"
        return {
            "type": "TFQ",
            "question": question,
            "level": normalized_level.upper(),
            "answer": correct_answer
        }

    def generate_mtq(self, level=None):
        if not self.columns:
            return None
        level = (level or "level1").lower()
        col1 = self._random_column()
        col2 = self._random_column()
        while col2 == col1 and len(self.columns) > 1:
            col2 = self._random_column()
        condition_col = self._random_column()

        # Use real sample value if available
        sample_values = self._get_sample_value(condition_col)
        if sample_values:
            value = random.choice(sample_values)
            col_type = self.schema[condition_col]["type"]
            if col_type in ["int", "float"]:
                condition = f"{condition_col} > {value}"
            elif col_type == "string":
                condition = f"{condition_col} = '{value}'"
            else:
                condition = f"{condition_col} = '{value}'"
        else:
            condition = self._random_condition(condition_col)

        queries = {
            "level1": f"π ({col1}) ({self.table_name})",
            "level2": f"σ ({condition}) ({self.table_name})",
            "level3": f"π ({col1}, {col2}) (σ ({condition}) ({self.table_name}))"
        }
        query = queries.get(level, queries["level1"])

        templates = {
            "level1": [
                ("The query {query} returns only the attribute '{col1}'.", True),
                ("The query {query} filters rows based on {condition}.", False),
                ("The query {query} includes the attribute '{col2}'.", False),
                ("Executing {query} will project the column '{col1}'.", True),
                ("The query {query} returns all columns of the table.", False)
            ],
            "level2": [
                ("The query {query} filters tuples where {condition}.", True),
                ("The query {query} projects the column '{col1}'.", False),
                ("The selection condition in {query} involves the attribute '{condition_col}'.", True),
                ("The query {query} returns the entire table without filtering.", False),
                ("The query {query} returns tuples that satisfy {condition}.", True)
            ],
            "level3": [
                ("The query {query} projects columns '{col1}' and '{col2}' after filtering by {condition}.", True),
                ("The query {query} selects tuples where {condition}.", True),
                ("The query {query} returns all attributes without filtering.", False),
                ("The query {query} includes a join operation.", False),
                ("The query {query} uses projection and selection operations.", True)
            ]
        }

        chosen_templates = templates.get(level, templates["level1"])
        statements = []
        pairs = []

        for template, truth in chosen_templates:
            statement = template.format(
                query=query,
                col1=col1,
                col2=col2,
                condition=condition,
                condition_col=condition_col,
                table=self.table_name
            )
            statements.append({"statement": statement, "answer": truth})
            pairs.append((statement, "True" if truth else "False"))

        question_text = f"Evaluate the following statements about the relational algebra query:\n{query}\nMark each as True or False."

        return {
            "type": "MTQ",
            "question": question_text,
            "statements": statements,
            "pairs": pairs,
            "query": query,
            "level": level.upper()
        }

    def generate_mcq(self, level=None):
        if not self.columns:
            return None
        level = (level or "level1").lower()
        col1 = self._random_column()
        col2 = self._random_column()
        while col2 == col1 and len(self.columns) > 1:
            col2 = self._random_column()
        condition_col = self._random_column()
        condition = self._random_condition(condition_col)
        queries = {
            "level1": f"π ({col1}) ({self.table_name})",
            "level2": f"σ ({condition}) ({self.table_name})",
            "level3": f"π ({col1}, {col2}) (σ ({condition}) ({self.table_name}))"
        }
        query = queries.get(level, queries["level1"])
        question_templates = {
            "level1": [
                f"What does the following projection query return?\n{query}",
                f"Which of the following best describes this relational algebra expression?\n{query}",
                f"In the query below, what is the operation performed?\n{query}",
                f"Identify the operation used in this relational algebra expression:\n{query}",
                f"Which attribute(s) does this query select from the table?\n{query}",
                f"What is the result of applying this query on the relation?\n{query}"
            ],
            "level2": [
                f"What is the effect of the selection operator in this query?\n{query}",
                f"Which tuples are selected by the following expression?\n{query}",
                f"What does the selection condition in this relational algebra query do?\n{query}",
                f"In the relational algebra query shown, which rows will satisfy the condition?\n{query}",
                f"Explain the filtering criteria used in the query:\n{query}",
                f"Which tuples remain after applying this selection?\n{query}"
            ],
            "level3": [
                f"What operations are combined in this query?\n{query}",
                f"Which of the following best describes the relational algebra query?\n{query}",
                f"In the given query, what is the order of operations?\n{query}",
                f"How does this query filter and then transform the data?\n{query}",
                f"Explain the sequence of relational algebra operations in the query:\n{query}",
                f"What is the result of combining selection and projection in this query?\n{query}"
            ]
        }
        question = random.choice(question_templates.get(level, question_templates["level1"]))
        if level == "level1":
            correct_answer = f"Returns all tuples with only the attribute '{col1}'."
            wrong_answers = [
                f"Returns all tuples with only the attribute '{col2}'.",
                "Returns all attributes of the table.",
                f"Filters tuples based on a condition on '{condition_col}'."
            ]
        elif level == "level2":
            correct_answer = f"Selects tuples where {condition} holds true."
            wrong_answers = [
                "Projects specified columns.",
                "Renames attributes.",
                "Joins two tables."
            ]
        else:
            correct_answer = f"Performs selection based on condition, then projects columns '{col1}' and '{col2}'."
            wrong_answers = [
                "Performs only selection.",
                "Performs only projection.",
                "Performs join followed by projection."
            ]
        options = wrong_answers + [correct_answer]
        random.shuffle(options)
        labels = ["A", "B", "C", "D"]
        options_dict = {labels[i]: options[i] for i in range(len(options))}
        answer_label = next(label for label, text in options_dict.items() if text == correct_answer)
        return {
            "type": "MCQ",
            "question": question,
            "options": options_dict,
            "answer": answer_label,
            "query": query,
            "level": level.upper()
        }

    def generate_ecq(self, level=None):
        if not self.columns:
            return None

        level = (level or "level1").lower()

        # ECQ: Expression Completion, fill-in-the-blank style
        col1 = self._random_column()
        col2 = self._random_column()
        while col2 == col1 and len(self.columns) > 1:
            col2 = self._random_column()
        condition_col = self._random_column()
        condition = self._random_condition(condition_col)

        templates = {
            "level1": [
                (f"Complete the expression: π {col1} ( ___ ), where we want only '{col1}' from '{self.table_name}'.", f"{self.table_name}"),
                (f"Fill in the blank: σ {col1} > 10 ( ___ ), to select all records from '{self.table_name}' where {col1} > 10.", f"{self.table_name}"),
                (f"Complete the relational algebra: π {col1}, {col2} ( ___ ), to project '{col1}' and '{col2}' from '{self.table_name}'.", f"{self.table_name}"),
            ],
            "level2": [
                (f"Complete the expression: π {col1} ( σ {condition} ( ___ ) ), to project '{col1}' after filtering '{self.table_name}' with {condition}.", f"{self.table_name}"),
                (f"Fill in the blank: σ {condition} ( ___ ), to select all records from '{self.table_name}' where {condition}.", f"{self.table_name}"),
                (f"Complete the relational algebra: π {col1}, {col2} ( σ {condition} ( ___ ) ), to project '{col1}' and '{col2}' after selection.", f"{self.table_name}"),
            ],
            "level3": [
                (f"Complete the expression: π {col1}, {col2} ( σ {condition} ( ρ T1 ( ___ ) ) ), to rename '{self.table_name}' to 'T1', filter, and project.", f"{self.table_name}"),
                (f"Fill in the blank: π {col1} ( σ {condition} ( ___ ⨝ AnotherTable ) ), to join '{self.table_name}' with 'AnotherTable', filter, and project.", f"{self.table_name}"),
                (f"Complete the relational algebra: π {col1}, {col2} ( σ {condition} ( ___ ) ), to project and filter after a rename or join.", f"{self.table_name}"),
            ]
        }

        if level not in templates:
            level = "level1"

        question_template, answer = random.choice(templates[level])

        return {
            "type": "ECQ",
            "question": question_template,
            "level": level.upper(),
            "answer": answer
        }

    def generate_diq(self, level=None):
        if not self.columns:
            return None

        level = (level or "level1").lower()
        selected_cols = random.sample(self.columns, min(2, len(self.columns)))
        cols_str = ', '.join(selected_cols)
        example_conditions = [
            f"{selected_cols[0]} = 'Value1'",
            f"{selected_cols[0]} > 10",
            f"{selected_cols[0]} != {selected_cols[1]}" if len(selected_cols) > 1 else f"{selected_cols[0]} != 'Value2'"
        ]
        condition = random.choice(example_conditions) if level in ["level2", "level3"] else None

        other_table = "AnotherTable"
        other_columns = ["colA", "colB", "colC"]
        other_cols_str = ', '.join(random.sample(other_columns, 2))

        if level == "level1":
            query = f"π ({cols_str}) ({self.table_name})"
            tree = f"""
π ({cols_str})
|
{self.table_name}
""".strip()
            mermaid = f"""graph TD
    A[π ({cols_str})]
    B[{self.table_name}]
    A --> B"""
            answer = f"Projects the columns {cols_str} from all tuples in '{self.table_name}'."

        elif level == "level2":
            query = f"π ({cols_str}) (σ ({condition}) ({self.table_name}))"
            tree = f"""
π ({cols_str})
|
σ ({condition})
|
{self.table_name}
""".strip()
            mermaid = f"""graph TD
    A[π ({cols_str})]
    B[σ ({condition})]
    C[{self.table_name}]
    A --> B
    B --> C"""
            answer = f"Selects rows from '{self.table_name}' where {condition}, then projects the columns {cols_str}."

        elif level == "level3":
            complex_queries = [
                {
                    "query": f"π ({cols_str}) (σ ({condition}) ({self.table_name}))",
                    "tree": f"""
π ({cols_str})
|
σ ({condition})
|
{self.table_name}
""".strip(),
                    "mermaid": f"""graph TD
    A[π ({cols_str})]
    B[σ ({condition})]
    C[{self.table_name}]
    A --> B
    B --> C""",
                    "answer": f"Selects rows from '{self.table_name}' where {condition}, then projects the columns {cols_str}."
                },
                {
                    "query": f"π ({cols_str}) ({self.table_name} ⨝ {other_table})",
                    "tree": f"""
π ({cols_str})
|
⨝ 
/   \\
{self.table_name}   {other_table}
""".strip(),
                    "mermaid": f"""graph TD
    A[π ({cols_str})]
    B[⨝]
    C[{self.table_name}]
    D[{other_table}]
    A --> B
    B --> C
    B --> D""",
                    "answer": f"Performs a natural join between '{self.table_name}' and '{other_table}', then projects the columns {cols_str}."
                },
                {
                    "query": f"π ({cols_str}) (σ ({condition}) (ρ (Renamed_{self.table_name}) ({self.table_name})))",
                    "tree": f"""
π ({cols_str})
|
σ ({condition})
|
ρ (Renamed_{self.table_name})
|
{self.table_name}
""".strip(),
                    "mermaid": f"""graph TD
    A[π ({cols_str})]
    B[σ ({condition})]
    C[ρ (Renamed_{self.table_name})]
    D[{self.table_name}]
    A --> B
    B --> C
    C --> D""",
                    "answer": f"Renames '{self.table_name}' to 'Renamed_{self.table_name}', filters rows with condition {condition}, then projects {cols_str}."
                },
                {
                    "query": f"π ({cols_str}) ((σ ({condition}) ({self.table_name})) ⨝ (σ ({condition}) ({other_table})))",
                    "tree": f"""
π ({cols_str})
|
⨝ 
/   \\
σ ({condition})     σ ({condition})
    |                   |
{self.table_name}     {other_table}
""".strip(),
                    "mermaid": f"""graph TD
    A[π ({cols_str})]
    B[⨝]
    C1[σ ({condition})]
    C2[σ ({condition})]
    D1[{self.table_name}]
    D2[{other_table}]
    A --> B
    B --> C1
    B --> C2
    C1 --> D1
    C2 --> D2""",
                    "answer": f"Filters both '{self.table_name}' and '{other_table}' using {condition}, joins the results, and then projects {cols_str}."
                }
            ]
            chosen = random.choice(complex_queries)
            query, tree, mermaid, answer = chosen["query"], chosen["tree"], chosen["mermaid"], chosen["answer"]
        else:
            return None

        diq_templates = {
            "level1": [
                "Construct the query tree for the following relational algebra expression:\n{query}",
                "Draw the relational algebra tree for:\n{query}",
                "Represent the query '{query}' as a query tree diagram.",
                "Translate this relational algebra expression into its corresponding query tree:\n{query}",
                "What is the query tree representation of:\n{query}?"
            ],
            "level2": [
                "Build the query tree for the relational algebra expression:\n{query}",
                "Sketch the query tree diagram for:\n{query}",
                "Given the relational algebra query '{query}', represent its query tree.",
                "Convert the expression into a query tree:\n{query}",
                "Illustrate the query tree for the following expression:\n{query}"
            ],
            "level3": [
                "Construct a detailed query tree for this relational algebra expression:\n{query}",
                "Draw and explain the query tree representation for:\n{query}",
                "Represent the complex query '{query}' as a query tree diagram.",
                "Translate this advanced relational algebra expression into its query tree:\n{query}",
                "What does the query tree of this expression look like?\n{query}"
            ]
        }

        question_template = random.choice(diq_templates[level])
        question = question_template.format(query=query)

        return {
            "type": "DIQ",
            "question": question,
            "query": query,
            "tree": tree,
            "mermaid": mermaid,
            "answer": answer,
            "level": level.upper()
        }

    def generate_oeq(self, level=None):
        if not self.columns:
            return None

        level = (level or "level1").lower()
        diq_result = self.generate_diq(level)
        if not diq_result:
            return None

        oeq_templates = {
            "level1": [
                "Explain the query tree structure for the relational algebra expression:\n{query}",
                "Describe how the query tree for '{query}' is constructed.",
                "What steps are involved in the query tree representation of:\n{query}?",
                "Provide a detailed explanation of the query tree for:\n{query}",
                "Illustrate and explain the query tree corresponding to the following expression:\n{query}"
            ],
            "level2": [
                "Describe the components and flow of the query tree for:\n{query}",
                "Explain the process represented by the query tree of the expression:\n{query}",
                "What does the query tree of this selection and projection expression look like? Explain:\n{query}",
                "Analyze the query tree structure for the relational algebra query:\n{query}",
                "Provide a detailed description of the query tree for the expression:\n{query}"
            ],
            "level3": [
                "Explain in detail the construction of the query tree for this complex relational algebra expression:\n{query}",
                "Describe how selection, projection, join, and rename are represented in the query tree for:\n{query}",
                "Provide a comprehensive explanation of the query tree for the following expression, including all operations:\n{query}",
                "Analyze the query tree representation of the expression below and explain each node's role:\n{query}",
                "Explain how the query tree combines multiple operations like selection, projection, join, and rename in:\n{query}"
            ]
        }

        question_template = random.choice(oeq_templates.get(level, oeq_templates["level1"]))
        question = question_template.format(query=diq_result["query"])

        return {
            "type": "OEQ",
            "question": question,
            "query": diq_result["query"],
            "tree": diq_result["tree"],
            "mermaid": diq_result["mermaid"],
            "answer": diq_result["answer"],
            "level": level.upper()
        }

    # --- Utility: Get all questions ---
    def generate_all_question_types(self, level="level1"):
        output = []
        try:
            bq = self.generate_bq(level=level)
            output.append({**bq, "type": "BQ"})
        except Exception as e:
            output.append({"type": "BQ", "error": str(e), "level": level})

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
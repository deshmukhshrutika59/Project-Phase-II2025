import random

class ProjectionGenerator:
    def __init__(self, table_name, table_schema):
        self.table_name = table_name
        self.schema = table_schema
        self.columns = {col: details for col, details in table_schema.items() if isinstance(details, dict) and "type" in details}
        self.column_names = list(self.columns.keys())
        self.sample_data = table_schema.get("sample_data", [])

    def _get_random_column(self):
        return random.choice(self.column_names) if self.column_names else None

    def _get_random_value(self, col):
        if not col:
            return None
        values = [row[col] for row in self.sample_data if col in row]
        return random.choice(values) if values else None

    def _format_value(self, value):
        if value is None:
            return "NULL"
        return f"'{value}'" if isinstance(value, str) else value

    def _get_sample_value(self, col):
        return [row[col] for row in self.sample_data if col in row] if self.sample_data else []

    def _col_phrase(self, col):
        return col.replace("_", " ").capitalize()

    def _table_phrase(self):
        name = self.table_name.replace("_", " ").capitalize()
        if not name.endswith('s'):
            name += 's'
        return name

    def _generate_condition(self, exclude_cols=None):
        # Pick a column not in exclude_cols and generate a business-friendly condition
        candidates = [c for c in self.column_names if not exclude_cols or c not in exclude_cols]
        if not candidates:
            return None, None, None
        col = random.choice(candidates)
        values = self._get_sample_value(col)
        if not values:
            return None, None, None
        value = random.choice(values)
        col_type = self.columns[col]["type"]
        if col_type in ["int", "float"]:
            cond = f"{col} = {value}"
        elif col_type == "string":
            cond = f"{col} = '{value}'"
        elif col_type == "bool":
            cond = f"{col} = {str(value).upper()}"
        else:
            cond = f"{col} = {value}"
        return col, value, cond

    def generate_bq(self, level="level1"):
        if not self.columns:
            raise ValueError(f"No valid columns available in table '{self.table_name}'.")
        if not self.sample_data:
            raise ValueError(f"No sample data available for table '{self.table_name}'.")

        normalized_level = level.lower()
        num_cols = {"level1": 1, "level2": 2, "level3": 2}.get(normalized_level, 1)
        selected_columns = random.sample(self.column_names, min(num_cols, len(self.column_names)))
        cols_str = ', '.join([self._col_phrase(c) for c in selected_columns])
        table_phrase = self._table_phrase()

        filter_col, filter_val, filter_cond = None, None, None
        if normalized_level == "level3":
            filter_col, filter_val, filter_cond = self._generate_condition(selected_columns)

        templates = {
            "level1": [
                "Show me only the {cols} for all {table}.",
                "List just the {cols} of every {table}.",
                "Can you give me the {cols} for each {table}?"
            ],
            "level2": [
                "List the {cols} for every {table}.",
                "Show only the {cols} columns for all {table}.",
                "Give me a list of {cols} for each {table}."
            ],
            "level3": [
                "Show the {cols} of all {table} where {filter_col} is {filter_val}.",
                "List the {cols} for {table} whose {filter_col} is {filter_val}.",
                "Give me the {cols} for each {table} with {filter_col} = {filter_val}.",
                "Show the {cols} of all {table} (no filter available)."
            ]
        }

        template_list = templates.get(normalized_level, templates["level1"])

        # If level3 and no filter_col/val, use fallback template
        if normalized_level == "level3" and (not filter_col or filter_val is None):
            template = template_list[-1]
            question = template.format(cols=cols_str, table=table_phrase)
            answer = f"π ({', '.join(selected_columns)}) ({self.table_name})"
        elif normalized_level == "level3":
            template = random.choice(template_list[:-1])
            question = template.format(
                cols=cols_str,
                table=table_phrase,
                filter_col=self._col_phrase(filter_col),
                filter_val=filter_val
            )
            filter_val_fmt = f"'{filter_val}'" if isinstance(filter_val, str) else filter_val
            answer = f"π ({', '.join(selected_columns)}) (σ ({filter_col} = {filter_val_fmt}) ({self.table_name}))"
        else:
            template = random.choice(template_list)
            question = template.format(cols=cols_str, table=table_phrase)
            answer = f"π ({', '.join(selected_columns)}) ({self.table_name})"

        return {
            "type": "BQ",
            "level": level.upper(),
            "question": question,
            "answer": answer
        }
    def generate_mcq(self, level=None):
        if not self.columns:
            return None

        normalized_level = (level or "level1").lower()
        num_cols = {"level1": 1, "level2": 2, "level3": 2}.get(normalized_level, 1)
        selected_cols = random.sample(self.column_names, min(num_cols, len(self.column_names)))
        cols_str = ', '.join([self._col_phrase(c) for c in selected_cols])
        table_phrase = self._table_phrase()

        filter_col, filter_val, filter_cond = None, None, None
        if normalized_level == "level3":
            filter_col, filter_val, filter_cond = self._generate_condition(selected_cols)

        templates = {
            "level1": [
                f"You want a report showing only the {cols_str} for each {table_phrase}. Which query would you use?",
                f"To get just the {cols_str} columns from all {table_phrase}, which expression is correct?",
                f"Which option will help you list only the {cols_str} for all {table_phrase}?",
                f"You want to display only the {cols_str} from all {table_phrase}. Which query is appropriate?"
            ],
            "level2": [
                f"You're tasked with retrieving {cols_str} columns from all {table_phrase}. Which relational algebra expression fits best?",
                f"To generate a summary showing {cols_str} from all {table_phrase}, which projection expression should you use?",
                f"Which query correctly projects the columns {cols_str} from all {table_phrase}?",
                f"For creating a concise view with {cols_str} attributes from all {table_phrase}, pick the correct query."
            ],
            "level3": [
                f"Show only the {cols_str} for all {table_phrase} where {self._col_phrase(filter_col)} is {filter_val}. Which query is correct?" if filter_col and filter_val is not None else
                f"Show only the {cols_str} for all {table_phrase} with a filter. Which query is correct?"
            ]
        }

        selected_templates = templates[normalized_level]
        question = random.choice(selected_templates)

        if normalized_level == "level3" and filter_col and filter_val is not None:
            filter_val_fmt = f"'{filter_val}'" if isinstance(filter_val, str) else filter_val
            correct = f"π ({', '.join(selected_cols)}) (σ ({filter_col} = {filter_val_fmt}) ({self.table_name}))"
            wrong1 = f"σ ({filter_col} = {filter_val_fmt}) (π ({', '.join(selected_cols)}) ({self.table_name}))"
            wrong2 = f"π ({filter_col}) ({self.table_name})"
        else:
            correct = f"π ({', '.join(selected_cols)}) ({self.table_name})"
            wrong1 = f"σ ({', '.join(selected_cols)}) ({self.table_name})"
            wrong_col_candidates = [col for col in self.columns if col not in selected_cols]
            wrong_col = random.choice(wrong_col_candidates) if wrong_col_candidates else random.choice(self.columns)
            wrong2 = f"π ({wrong_col}) ({self.table_name})"

        options = [correct, wrong1, wrong2, "None of the above."]
        random.shuffle(options)
        answer = chr(options.index(correct) + ord('a'))

        return {
            "type": "MCQ",
            "question": question,
            "options": {chr(i + 97): opt for i, opt in enumerate(options)},
            "level": normalized_level.upper(),
            "answer": f"({answer})"
        }

    # The rest of your methods (generate_oeq, generate_tfq, generate_mtq, generate_diq, generate_ecq, generate_all_question_types)
    # remain unchanged, but you can update them similarly for business-friendly phrasing if needed.

    def generate_oeq(self, level=None):
        if not self.columns:
            return None

        normalized_level = (level or "level1").lower()
        num_cols = {"level1": 1, "level2": 2, "level3": 2}.get(normalized_level, 1)
        selected_cols = random.sample(self.column_names, min(num_cols, len(self.column_names)))
        cols_str = ', '.join([self._col_phrase(c) for c in selected_cols])
        table_phrase = self._table_phrase()

        filter_col, filter_val, filter_cond = None, None, None
        if normalized_level == "level3":
            filter_col, filter_val, filter_cond = self._generate_condition(selected_cols)

        templates = {
            "level1": [
                f"How would you write a query to show just the {cols_str} for all {table_phrase}?",
                f"Suppose you need a table with only the {cols_str} from all {table_phrase}. What is the correct relational algebra expression?",
                f"Write a query to display only the {cols_str} for each {table_phrase}.",
                f"How can you get a list of just the {cols_str} columns from all {table_phrase}?",
                f"Which relational algebra expression will return only the {cols_str} for all {table_phrase}?",
                f"How do you extract only the {cols_str} from all {table_phrase} in a query?",
                f"Write a query to list only the {cols_str} for every {table_phrase}.",
                f"How would you retrieve just the {cols_str} for all {table_phrase}?"
            ],
            "level2": [
                f"Write a query to display the {cols_str} for every {table_phrase}.",
                f"How can you get a list of only the {cols_str} columns from all {table_phrase}?",
                f"Which relational algebra expression will return only the {cols_str} for all {table_phrase}?",
                f"How do you extract only the {cols_str} from all {table_phrase} in a query?",
                f"Suppose you want to see just the {cols_str} for each {table_phrase}. What query would you use?",
                f"Write a query to list only the {cols_str} for every {table_phrase}.",
                f"How would you retrieve just the {cols_str} for all {table_phrase}?",
                f"Formulate a projection query to extract {cols_str} attributes from all {table_phrase}.",
                f"How would you write a query to show only the {cols_str} for all {table_phrase}?"
            ],
            "level3": [
                f"Write a relational algebra expression to show the {cols_str} for all {table_phrase} where {self._col_phrase(filter_col)} is {filter_val}." if filter_col and filter_val is not None else
                f"Write a projection query for the {cols_str} columns from all {table_phrase} with a filter.",
                f"How would you express a query that projects {cols_str} from all {table_phrase} while applying a filter on {self._col_phrase(filter_col)}?" if filter_col and filter_val is not None else
                f"How would you write a query to show only the {cols_str} for all {table_phrase} with a filter?",
                f"Create a detailed projection query for columns {cols_str} from all {table_phrase} with a filter on {self._col_phrase(filter_col)}." if filter_col and filter_val is not None else
                f"Write a query to list only the {cols_str} for every {table_phrase} with a filter.",
                f"Suppose you want to see just the {cols_str} for each {table_phrase} where {self._col_phrase(filter_col)} is {filter_val}. What query would you use?" if filter_col and filter_val is not None else
                f"How would you retrieve just the {cols_str} for all {table_phrase} with a filter?"
            ]
        }

        question = random.choice(templates[normalized_level])
        if normalized_level == "level3" and filter_col and filter_val is not None:
            filter_val_fmt = f"'{filter_val}'" if isinstance(filter_val, str) else filter_val
            answer = f"π ({', '.join(selected_cols)}) (σ ({filter_col} = {filter_val_fmt}) ({self.table_name}))"
        else:
            answer = f"π ({', '.join(selected_cols)}) ({self.table_name})"

        return {
            "type": "OEQ",
            "question": question,
            "answer": answer,
            "level": normalized_level.upper()
        }

    def generate_tfq(self, level=None):
        if not self.columns:
            return None

        normalized_level = (level or "level1").lower()
        num_cols = {"level1": 1, "level2": 2, "level3": 2}.get(normalized_level, 1)
        selected_cols = random.sample(self.column_names, min(num_cols, len(self.column_names)))
        cols_str = ', '.join([self._col_phrase(c) for c in selected_cols])
        table_phrase = self._table_phrase()

        filter_col, filter_val, filter_cond = None, None, None
        if normalized_level == "level3":
            filter_col, filter_val, filter_cond = self._generate_condition(selected_cols)

        if normalized_level == "level3" and filter_col and filter_val is not None:
            filter_val_fmt = f"'{filter_val}'" if isinstance(filter_val, str) else filter_val
            correct_expr = f"π ({', '.join(selected_cols)}) (σ ({filter_col} = {filter_val_fmt}) ({self.table_name}))"
            wrong_expr = f"σ ({filter_col} = {filter_val_fmt}) (π ({', '.join(selected_cols)}) ({self.table_name}))"
        else:
            correct_expr = f"π ({', '.join(selected_cols)}) ({self.table_name})"
            wrong_expr = f"σ ({', '.join(selected_cols)}) ({self.table_name})"

        templates = {
            "level1": {
                "true": [
                    f"To create a table with only the {cols_str} from all {table_phrase}, you can use {correct_expr}.",
                    f"{correct_expr} will give you a table with just the {cols_str} columns from all {table_phrase}.",
                    f"If your manager wants a report showing only {cols_str} for each record in all {table_phrase}, {correct_expr} is the right query.",
                    f"Is {correct_expr} the correct way to get only the {cols_str} for all {table_phrase}?",
                    f"Would {correct_expr} return just the {cols_str} columns from all {table_phrase}?"
                ],
                "false": [
                    f"To get only the {cols_str} from all {table_phrase}, you should use {wrong_expr}.",
                    f"{wrong_expr} is the right way to show only the {cols_str} columns from all {table_phrase}.",
                    f"If you want a table with just {cols_str} from all {table_phrase}, you should use {wrong_expr}.",
                    f"Is {wrong_expr} the correct way to get only the {cols_str} for all {table_phrase}?",
                    f"Would {wrong_expr} return just the {cols_str} columns from all {table_phrase}?"
                ]
            },
            "level2": {
                "true": [
                    f"Using {correct_expr} will help you focus on just the {cols_str} columns in all {table_phrase}.",
                    f"To prepare a summary with only {cols_str} from all {table_phrase}, the correct relational algebra expression is {correct_expr}.",
                    f"For generating reports with only {cols_str} columns from all {table_phrase}, {correct_expr} is suitable.",
                    f"Is {correct_expr} the right query to get only the {cols_str} columns from all {table_phrase}?",
                    f"Would {correct_expr} give you just the {cols_str} for all {table_phrase}?"
                ],
                "false": [
                    f"To display only {cols_str} columns in all {table_phrase}, the correct query is {wrong_expr}.",
                    f"To create a summary table with only {cols_str} from all {table_phrase}, use {wrong_expr}.",
                    f"{wrong_expr} is appropriate for projecting only {cols_str} from all {table_phrase}.",
                    f"Is {wrong_expr} the right query to get only the {cols_str} columns from all {table_phrase}?",
                    f"Would {wrong_expr} give you just the {cols_str} for all {table_phrase}?"
                ]
            },
            "level3": {
                "true": [
                    f"When projecting {cols_str} with a filter in all {table_phrase}, {correct_expr} is the right query.",
                    f"{correct_expr} correctly represents projecting columns {cols_str} from all {table_phrase} with a filter.",
                    f"For detailed data analysis, {correct_expr} is the valid relational algebra query to select {cols_str} from all {table_phrase} with a filter.",
                    f"Is {correct_expr} the correct way to get only the {cols_str} for all {table_phrase} where a filter applies?",
                    f"Would {correct_expr} return just the {cols_str} columns from all {table_phrase} with a filter?"
                ],
                "false": [
                    f"To project columns {cols_str} with a filter in all {table_phrase}, {wrong_expr} is the correct expression.",
                    f"{wrong_expr} is used to select columns {cols_str} from all {table_phrase} with a filter.",
                    f"For filtering and projecting {cols_str} in all {table_phrase}, {wrong_expr} is the right choice.",
                    f"Is {wrong_expr} the correct way to get only the {cols_str} for all {table_phrase} where a filter applies?",
                    f"Would {wrong_expr} return just the {cols_str} columns from all {table_phrase} with a filter?"
                ]
            }
        }

        is_true = random.choice([True, False])
        key = "true" if is_true else "false"
        statement = random.choice(templates[normalized_level][key])
        answer = "True" if is_true else "False"

        return {
            "type": "TFQ",
            "question": statement,
            "answer": answer,
            "level": normalized_level.upper()
        }

    def generate_mtq(self, level=None):
        # Define operator-description pairs for each level
        pairs_dict = {
            "level1": [
                ("π", "Show only certain columns (for example, just names or salaries)"),
                ("σ", "Filter records based on a business rule (like only active employees)"),
                ("ρ", "Rename a table or column for clarity")
            ],
            "level2": [
                ("π", "Create a summary with selected fields (such as names and departments)"),
                ("σ", "Find records that match a business condition"),
                ("ρ", "Give a new name to a table"),
                ("∪", "Combine results from two tables (like all customers from two regions)")
            ],
            "level3": [
                ("π", "Project specific columns from a dataset"),
                ("σ", "Select records that satisfy a business filter"),
                ("ρ", "Rename attributes or tables"),
                ("∪", "Union of two datasets"),
                ("⨝", "Join two tables based on a matching value")
            ]
        }

        normalized_level = (level or "level1").lower()
        if normalized_level not in pairs_dict:
            normalized_level = "level1"

        pairs = pairs_dict[normalized_level][:]
        random.shuffle(pairs)

        templates = {
            "level1": [
                "Match each relational algebra operator to its business use:",
                "Pair the symbol with its business meaning:",
                "Which business task matches each relational algebra operator?",
                "Connect each operator to its business description:"
            ],
            "level2": [
                "Match the relational algebra operators with their business descriptions:",
                "Connect each operator symbol with its correct business use case:",
                "Pair each operator with its business scenario:",
                "Which business scenario fits each relational algebra operator?"
            ],
            "level3": [
                "Match each relational algebra operator to the correct business description:",
                "Pair each symbol with the precise business operation it represents:",
                "Which business operation is described by each relational algebra symbol?",
                "Connect each operator to its advanced business use:"
            ]
        }

        question = random.choice(templates[normalized_level])
        options = [(op, f"({chr(97 + i)}) {desc}") for i, (op, desc) in enumerate(pairs)]
        answer = ", ".join([f"{op} → ({chr(97 + i)})" for i, (op, _) in enumerate(pairs)])

        return {
            "type": "MTQ",
            "question": question,
            "pairs": options,
            "answer": answer,
            "level": normalized_level.upper()
        }
    def generate_diq(self, level=None):
        if not self.column_names:
            return None

        selected_cols = random.sample(self.column_names, min(2, len(self.column_names)))
        cols_str = ', '.join([self._col_phrase(c) for c in selected_cols])
        table_phrase = self._table_phrase()

        filter_col = random.choice([c for c in self.column_names if c not in selected_cols] or self.column_names)
        filter_val = None
        if self.sample_data:
            vals = [row[filter_col] for row in self.sample_data if filter_col in row]
            filter_val = random.choice(vals) if vals else None

        tree_templates = {
            "level1": [
                f"    π_{{{cols_str}}}\n      |\n    {table_phrase}",
                f"    π_{{{cols_str}}}\n      |\n    {self.table_name}",
                f"    π_{{{cols_str}}}\n      |\n    Table: {table_phrase}",
                f"    π_{{{cols_str}}}\n      |\n    Source: {self.table_name}"
            ],
            "level2": [
                f"    π_{{{cols_str}}}\n      |\n    σ_{{some_condition}}\n      |\n    {table_phrase}",
                f"    π_{{{cols_str}}}\n      |\n    σ_{{{self._col_phrase(filter_col)} = {filter_val if filter_val is not None else 'value'}}}\n      |\n    {table_phrase}",
                f"    π_{{{cols_str}}}\n      |\n    σ_{{condition on {self._col_phrase(filter_col)}}}\n      |\n    {self.table_name}",
                f"    π_{{{cols_str}}}\n      |\n    σ_{{filter applied}}\n      |\n    Table: {table_phrase}"
            ],
            "level3": [
                f"    π_{{{cols_str}}}\n      |\n    σ_{{{self._col_phrase(filter_col)} > 10}}\n      |\n    {table_phrase}",
                f"    π_{{{cols_str}}}\n      |\n    σ_{{{self._col_phrase(filter_col)} = '{filter_val}'}}\n      |\n    {table_phrase}" if filter_val is not None else
                f"    π_{{{cols_str}}}\n      |\n    σ_{{{self._col_phrase(filter_col)} = value}}\n      |\n    {table_phrase}",
                f"    π_{{{cols_str}}}\n      |\n    σ_{{advanced filter on {self._col_phrase(filter_col)}}}\n      |\n    {self.table_name}",
                f"    π_{{{cols_str}}}\n      |\n    σ_{{complex condition}}\n      |\n    Table: {table_phrase}"
            ]
        }

        question_templates = {
            "level1": [
                "Which columns will be in the result of this projection query?",
                "After running this projection, which data columns will you see?",
                "What information will be included in the output of this projection?",
                "Identify the columns present in the result of this projection operation."
            ],
            "level2": [
                "Which columns are returned after applying this query with selection and projection?",
                "What columns will be present in the result after filtering and projecting?",
                "After this selection and projection, which columns are shown in the output?",
                "List the columns that will appear in the result after applying both selection and projection."
            ],
            "level3": [
                "Which data columns are produced by this relational algebra query tree with filtering?",
                "After applying the filter and projection in this query tree, what columns remain?",
                "What columns will the final result contain after this sequence of operations?",
                "Identify the columns that will be present in the output after all operations in the query tree."
            ]
        }

        normalized_level = (level or "level1").lower()
        tree = random.choice(tree_templates.get(normalized_level, tree_templates["level1"]))
        question = random.choice(question_templates.get(normalized_level, question_templates["level1"]))

        return {
            "type": "DIQ",
            "question": question,
            "tree": tree,
            "answer": f"{{{cols_str}}}",
            "level": normalized_level.upper()
        }

    def generate_ecq(self, level="level1"):
        if not self.columns:
            return None

        level = level.lower() if isinstance(level, str) else "level1"

        valid_columns = [col for col in self.columns if isinstance(col, str) and col.strip()]
        if not valid_columns:
            print(f"[ECQ] No valid columns found for table: {self.table_name}")
            return None

        selected_col = random.choice(valid_columns)
        col_phrase = self._col_phrase(selected_col)
        table_phrase = self._table_phrase()

        level1_qs = [
            (
                f"Explain what happens when you use the projection operator π to select '{col_phrase}' from all {table_phrase}.",
                f"The projection operator π({selected_col})({self.table_name}) returns only the '{col_phrase}' column from all {table_phrase}, removing any duplicate entries."
            ),
            (
                f"What is the result of applying π to '{col_phrase}' in {table_phrase}?",
                f"Applying π({selected_col})({self.table_name}) gives a relation with just the '{col_phrase}' column, with duplicates removed."
            ),
            (
                f"If you use π to get only '{col_phrase}' from all {table_phrase}, what will the output look like?",
                f"The output will be a list of unique '{col_phrase}' values from all {table_phrase}."
            ),
            (
                f"Describe the effect of the projection operator π on the '{col_phrase}' column in {table_phrase}.",
                f"π({selected_col})({self.table_name}) selects only the '{col_phrase}' column and removes duplicate rows."
            ),
            (
                f"What does π({selected_col})({self.table_name}) do in terms of the data you see?",
                f"It shows only the '{col_phrase}' column from all {table_phrase}, with no duplicate values."
            )
        ]

        level2_qs = [
            (
                f"Describe how using π to project '{col_phrase}' from {table_phrase} affects the data, especially regarding duplicates.",
                f"The projection operator π({selected_col})({self.table_name}) extracts the '{col_phrase}' column from all {table_phrase} and eliminates duplicate rows, so the result contains only unique values for that column."
            ),
            (
                f"What happens to duplicate values when π is used to select '{col_phrase}' from {table_phrase}?",
                f"Duplicates are removed, so only unique '{col_phrase}' values remain in the result."
            ),
            (
                f"How does the projection operator π impact the '{col_phrase}' column and the overall data in {table_phrase}?",
                f"It reduces the data to just the '{col_phrase}' column and ensures all values are unique."
            ),
            (
                f"If you apply π to '{col_phrase}' in {table_phrase}, what changes occur in the result set?",
                f"The result set will only have the '{col_phrase}' column, and all duplicate rows will be removed."
            ),
            (
                f"Explain the outcome of projecting '{col_phrase}' from {table_phrase} using π, focusing on uniqueness.",
                f"Projecting '{col_phrase}' with π ensures the output contains only unique values for that column."
            )
        ]

        level3_qs = [
            (
                f"Discuss the effect of applying π to '{col_phrase}' in {table_phrase}: how are duplicates handled, and what happens to the table's structure?",
                f"The projection operator π({selected_col})({self.table_name}) produces a new relation with only the '{col_phrase}' column, removing any duplicate rows to ensure uniqueness. This reduces the table's structure to just the projected column, which may result in loss of other information from the original table."
            ),
            (
                f"What are the implications of using π on '{col_phrase}' in {table_phrase} for the schema and data?",
                f"Using π on '{col_phrase}' changes the schema to include only that column and removes duplicate rows, possibly losing other data."
            ),
            (
                f"How does the projection operator π({selected_col})({self.table_name}) affect the relation's schema and duplicate rows?",
                f"It keeps only the '{col_phrase}' column in the schema and ensures all rows are unique for that column."
            ),
            (
                f"Explain what information might be lost when π is used to select only '{col_phrase}' from {table_phrase}.",
                f"All columns except '{col_phrase}' are dropped, so any information in those columns is lost in the result."
            ),
            (
                f"Describe the behavior of π({selected_col})({self.table_name}) in terms of output columns and duplicate removal.",
                f"The output will have only the '{col_phrase}' column, and all duplicate values will be removed."
            )
        ]

        templates = {
            "level1": level1_qs,
            "level2": level2_qs,
            "level3": level3_qs
        }

        qa_pair = random.choice(templates.get(level, level1_qs))

        return {
            "type": "ECQ",
            "level": level.upper(),
            "question": qa_pair[0],
            "answer": qa_pair[1]
        }

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
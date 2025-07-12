import random
class SelectionGenerator:
    def __init__(self, table_name, table_schema):
        self.table_name = table_name
        self.schema = table_schema
        self.columns = [col for col in table_schema if isinstance(table_schema[col], dict) and 'type' in table_schema[col]]
        self.sample_data = table_schema.get("sample_data", [])

    def _get_sample_value(self, col):
        return [row[col] for row in self.sample_data if col in row] if self.sample_data else []
    
    def _get_random_column(self):
        return random.choice(self.columns) if self.columns else None

    def _get_random_value(self, col):
        if not col:
            return None
        values = [row[col] for row in self.sample_data if col in row]
        return random.choice(values) if values else None

    def _auto_phrase(self, col, val=None):
        col_nice = col.replace("_", " ").capitalize()
        if col.endswith("_id"):
            phrase = f"{col_nice.replace(' id', '')} ID"
        elif col in ["name"]:
            phrase = "name"
        elif col in ["dept_name", "department"]:
            phrase = "department"
        elif col in ["city", "country", "region", "location"]:
            phrase = col_nice
        elif col in ["age", "year", "cgpa", "salary", "price", "amount", "budget", "capacity", "stock"]:
            phrase = col_nice
        else:
            phrase = col_nice
        if val is not None:
            # Use "is" for most columns, "named" for name columns
            if col in ["name"]:
                return f"{phrase} named {val}"
            elif col.endswith("_id"):
                return f"{phrase} = {val}"
            else:
                return f"{phrase} is {val}"
        return phrase

    def _table_phrase(self):
        # Pluralize table name for business-friendly entity reference
        name = self.table_name.replace("_", " ").capitalize()
        if not name.endswith('s'):
            name += 's'
        return name

    def _format_value(self, value):
        if value is None:
            return "NULL"
        return f"'{value}'" if isinstance(value, str) else value
    
    def generate_bq(self, level="level1"):
        if not self.columns:
            raise ValueError(f"No columns found in schema for table '{self.table_name}'.")
        if not self.sample_data:
            raise ValueError(f"No sample data available for table '{self.table_name}'.")

        used_combinations = set()
        table_phrase = self._table_phrase()  # <-- Add this line

        level_templates = {
                "level1": [
                    ("List {col_phrase}.", "="),
                    ("Show all {col_phrase}.", "="),
                    ("How many {table_phrase} are there with {col_phrase}?", "="), 
                    ("Which {col_phrase} can you find?", "="),
                    ("Give details of {col_phrase}.", "="),
                    ("Find {col_phrase}.", "="),
                    ("Display {col_phrase}.", "="),
                    ("Tell me about {col_phrase}.", "="),
                ],
                "level2": [
                    ("List {col_phrase} with values greater than {val}.", ">"),
                    ("Show {col_phrase} with values less than {val}.", "<"),
                    ("Find {col_phrase} with at least {val}.", ">="),
                    ("Display {col_phrase} with at most {val}.", "<="),
                    ("List {col_phrase} not equal to {val}.", "!="),
                    ("Show both {col1_phrase} and {col2_phrase}.", "AND"),
                    ("Find either {col1_phrase} or {col2_phrase}.", "OR"),
                    ("Give details of {col1_phrase} and {col2_phrase}.", "AND"),
                    ("Display {col1_phrase} or {col2_phrase}.", "OR"),
                ],
                "level3": [
                    ("List {col_phrase} between {val} and {val2}.", "BETWEEN"),
                    ("Show {col_phrase} either {val} or {val2}.", "IN"),
                    ("Find {col_phrase} with some value.", "IS NOT NULL"),
                    ("Display {col_phrase} matching pattern {pattern}.", "LIKE"),
                    ("Show both {col1_phrase} and {col2_phrase}.", "AND"),
                    ("Find either {col1_phrase} or {col2_phrase}.", "OR"),
                    ("Give details of {col1_phrase} and {col2_phrase}.", "AND"),
                    ("Display {col1_phrase} or {col2_phrase}.", "OR"),
                ]
            }
        level_order = ["level1", "level2", "level3"]
        levels_to_use = level_order[: level_order.index(level) + 1]

        all_templates = []
        for lvl in levels_to_use:
            all_templates.extend(level_templates[lvl])

        random.shuffle(all_templates)
        for template, op in all_templates:
            if op in ["=", ">", "<", ">=", "<=", "!="]:
                col = random.choice(self.columns)
                values = self._get_sample_value(col)
                if not values:
                    continue
                val = random.choice(values)
                key = (col, val, op)
                if key in used_combinations:
                    continue
                used_combinations.add(key)
                val_fmt = f"'{val}'" if isinstance(val, str) else val

                col_phrase = self._auto_phrase(col, val_fmt)
                col_phrase_no_val = self._auto_phrase(col)  # <-- Add this line

                # Use col_phrase_no_val for all comparison ops except '='
                if op in [">", "<", ">=", "<=", "!="] and "{col_phrase}" in template:
                    q = template.format(col_phrase=col_phrase_no_val, val=val_fmt, table_phrase=table_phrase)
                else:
                    q = template.format(col_phrase=col_phrase, val=val_fmt, table_phrase=table_phrase)
                ra = f"σ ({col} {op} {val_fmt})({self.table_name})"
                return {"question": q, "answer": ra, "level": level}

            elif op in ["AND", "OR"]:
                if len(self.columns) < 2:
                    continue
                col1, col2 = random.sample(self.columns, 2)
                values1 = self._get_sample_value(col1)
                values2 = self._get_sample_value(col2)
                if not values1 or not values2:
                    continue
                val1, val2 = random.choice(values1), random.choice(values2)
                key = (col1, val1, col2, val2, op)
                if key in used_combinations:
                    continue
                used_combinations.add(key)
                val1_fmt = f"'{val1}'" if isinstance(val1, str) else val1
                val2_fmt = f"'{val2}'" if isinstance(val2, str) else val2

                col1_phrase = self._auto_phrase(col1, val1_fmt)
                col2_phrase = self._auto_phrase(col2, val2_fmt)
                q = template.format(col1_phrase=col1_phrase, val1=val1_fmt, col2_phrase=col2_phrase, val2=val2_fmt)
                ra = f"σ ({col1} = {val1_fmt} {op} {col2} = {val2_fmt})({self.table_name})"
                return {"question": q, "answer": ra, "level": level}

            elif op == "BETWEEN":
                col = random.choice(self.columns)
                values = self._get_sample_value(col)
                if not values or len(values) < 2:
                    continue
                val1, val2 = sorted(random.sample(values, 2))
                key = (col, val1, val2, op)
                if key in used_combinations:
                    continue
                used_combinations.add(key)
                v1 = f"'{val1}'" if isinstance(val1, str) else val1
                v2 = f"'{val2}'" if isinstance(val2, str) else val2
                col_phrase = self._auto_phrase(col)
                q = template.format(col_phrase=col_phrase, val=v1, val2=v2)
                ra = f"σ ({col} BETWEEN {v1} AND {v2})({self.table_name})"
                return {"question": q, "answer": ra, "level": level}

            elif op == "IN":
                col = random.choice(self.columns)
                values = self._get_sample_value(col)
                if not values or len(values) < 2:
                    continue
                val1, val2 = random.sample(values, 2)
                key = (col, val1, val2, op)
                if key in used_combinations:
                    continue
                used_combinations.add(key)
                v1 = f"'{val1}'" if isinstance(val1, str) else val1
                v2 = f"'{val2}'" if isinstance(val2, str) else val2
                col_phrase = self._auto_phrase(col)
                q = template.format(col_phrase=col_phrase, val=v1, val2=v2)
                ra = f"σ ({col} IN ({v1}, {v2}))({self.table_name})"
                return {"question": q, "answer": ra, "level": level}

            elif op == "IS NOT NULL":
                col = random.choice(self.columns)
                key = (col, op)
                if key in used_combinations:
                    continue
                used_combinations.add(key)
                col_phrase = self._auto_phrase(col)
                q = template.format(col_phrase=col_phrase)
                ra = f"σ ({col} IS NOT NULL)({self.table_name})"
                return {"question": q, "answer": ra, "level": level}

            elif op == "LIKE":
                col = random.choice(self.columns)
                values = self._get_sample_value(col)
                if not values:
                    continue
                val = random.choice(values)
                if not isinstance(val, str):
                    continue
                pattern = f"%{val[1:-1]}%" if len(val) > 2 else f"%{val}%"
                key = (col, pattern, op)
                if key in used_combinations:
                    continue
                used_combinations.add(key)
                col_phrase = self._auto_phrase(col)
                q = template.format(col_phrase=col_phrase, pattern=pattern)
                ra = f"σ ({col} LIKE '{pattern}')({self.table_name})"
                return {"question": q, "answer": ra, "level": level}

        return {
            "question": "Not enough valid data to generate a basic selection question.",
            "answer": "N/A",
            "level": level
        }

    def generate_tfq(self, level=None):
        col = self._get_random_column()
        value = self._get_random_value(col)
        val_fmt = self._format_value(value)

        if col is None or value is None:
            return {
                "type": "TFQ",
                "question": "Not enough data to generate question.",
                "answer": "N/A",
                "level": level.upper() if level else "-"
            }

        col_phrase = self._auto_phrase(col, val_fmt)
        col_phrase_no_val = self._auto_phrase(col)

        templets = {
            "level1": [
                (f"True or False: π({col})({self.table_name}) means selecting only the {col_phrase_no_val} for all records.", lambda: True),
                (f"True or False: σ({col} = {val_fmt})({self.table_name}) filters {col_phrase}.", lambda: True),
                (f"True or False: π({col})(σ({col} = {val_fmt})({self.table_name})) first filters {col_phrase}, then selects only the {col_phrase_no_val}.", lambda: True),
                (f"True or False: π({col})(σ({col} = {val_fmt})({self.table_name})) returns all columns where {col_phrase_no_val} is {val_fmt}.", lambda: False),
                (f"True or False: σ({col} ≠ {val_fmt})({self.table_name}) returns records where {col_phrase_no_val} is not {val_fmt}.", lambda: True),
                (f"True or False: π({col})({self.table_name}) filters records where {col_phrase_no_val} is {val_fmt}.", lambda: False),
                ("True or False: Projection (π) is used to select columns from a table.", lambda: True),
                ("True or False: Selection (σ) filters records based on a condition.", lambda: True),
                (f"True or False: σ({col} > {val_fmt})({self.table_name}) returns records where {col_phrase_no_val} is greater than {val_fmt}.", lambda: True),
                (f"True or False: π({col})(σ({col} = {val_fmt})({self.table_name})) and σ({col} = {val_fmt})(π({col})({self.table_name})) always return the same result.", lambda: False),
            ],
            "level2": [
                (f"True or False: π* (σ({col} = {val_fmt})({self.table_name})) returns all columns where {col_phrase} is {val_fmt}.", lambda: True),
                (f"True or False: σ({col} = {val_fmt})(π({col})({self.table_name})) applies selection after projection.", lambda: False),
                (f"True or False: Projecting out a column and then trying to select on that column causes an error.", lambda: True),
                (f"True or False: σ({col} = {val_fmt}) followed by π({col}) returns only the {col_phrase} values matching the condition.", lambda: True),
                (f"True or False: π({col}) ∘ σ({col} = {val_fmt}) is a valid operator chain (selection then projection).", lambda: True),
                ("True or False: The order of selection and projection operations affects the output in relational algebra.", lambda: True),
                ("True or False: Projection (π) removes unwanted columns from the output.", lambda: True),
                (f"True or False: σ({col} > {val_fmt})({self.table_name}) selects records where {col_phrase} is greater than {val_fmt}.", lambda: True),
                ("True or False: Selection (σ) can be applied only after projection (π).", lambda: False),
                (f"True or False: π({col})(σ({col} = {val_fmt})({self.table_name})) always returns more rows than σ({col} = {val_fmt})({self.table_name}).", lambda: False),
            ],
            "level3": [
                ("True or False: Projection (π) can filter records based on a condition.", lambda: False),
                (f"True or False: π({col}) followed by σ({col} = {val_fmt}) is equivalent to σ({col} = {val_fmt}) followed by π({col}).", lambda: False),
                ("True or False: The order of selection (σ) and projection (π) is interchangeable in relational algebra.", lambda: False),
                ("True or False: Selecting on a column that has been projected out will cause an error.", lambda: True),
                (f"True or False: σ({col} > {val_fmt})({self.table_name}) selects records where {col_phrase} is greater than {val_fmt} regardless of projection.", lambda: True),
                ("True or False: Projection (π) only selects columns, it never filters records.", lambda: True),
                ("True or False: Selection (σ) filters records based on conditions but keeps all columns.", lambda: True),
                ("True or False: π and σ operations are the same and can be used interchangeably.", lambda: False),
                ("True or False: The composition π(σ(R)) means projecting after selection on relation R.", lambda: True),
                ("True or False: Selection can reduce the number of records but projection reduces the number of columns.", lambda: True),
            ],
        }
        chosen_level = level.lower() if level and level.lower() in templets else "level1"
        question, answer_func = random.choice(templets[chosen_level])
        answer = answer_func()

        return {
            "type": "TFQ",
            "level": chosen_level.upper(),
            "question": question,
            "answer": "True" if answer else "False"
        }

    def generate_mcq(self, level=None):
        col = self._get_random_column()
        value = self._get_random_value(col)
        val_fmt = self._format_value(value)

        if col is None or value is None:
            return {
                "type": "MCQ",
                "question": "Not enough data to create a question.",
                "options": {},
                "answer": "N/A",
                "level": level.upper() if level else "-"
            }

        options_pool = {
            "proj_after_select": f"π({col})(σ({col} = {val_fmt})({self.table_name}))",
            "select_all": f"σ({col} = {val_fmt})({self.table_name})",
            "project_only": f"π({col})({self.table_name})",
            "not_equal_select": f"σ({col} ≠ {val_fmt})({self.table_name})",
            "project_all_attrs": f"π* (σ({col} = {val_fmt})({self.table_name}))",
            "invalid": "None of these options are correct."
        }

        templates_by_level = {
            "level1": [
                (f"Which expression gives you the {col} values only for the rows where {col} is exactly {val_fmt}?", "proj_after_select"),
                (f"Which expression finds all rows where {col} equals {val_fmt}?", "select_all"),
                (f"Which expression shows only the {col} column for every row in the table?", "project_only"),
                (f"Which expression would show rows where {col} is not {val_fmt}?", "not_equal_select"),
                (f"Which expression selects rows where {col} equals {val_fmt} and then gives you all the columns?", "project_all_attrs"),
            ],
            "level2": [
                (f"Which expression selects rows with {col} equal to {val_fmt} and then shows only the {col} column?", "proj_after_select"),
                (f"Which expression selects rows where {col} is different from {val_fmt}?", "not_equal_select"),
                (f"Which expression returns all columns but only for rows where {col} equals {val_fmt}?", "project_all_attrs"),
                (f"Which expression just gives you the {col} column for all rows without filtering?", "project_only"),
                (f"Which expression picks rows where {col} equals {val_fmt} without reducing columns?", "select_all"),
            ],
            "level3": [
                (f"Which of these is NOT a valid relational algebra expression?", "invalid"),
                (f"Which expression first finds rows where {col} equals {val_fmt} and then shows only the {col} column?", "proj_after_select"),
                (f"Which expression applies selection before projection on {col}?", "proj_after_select"),
                (f"Which expression filters rows where {col} is not {val_fmt}?", "not_equal_select"),
                (f"Which expression shows only the {col} column for all rows?", "project_only"),
            ],
        }

        chosen_level = level.lower() if level and level.lower() in templates_by_level else "level1"
        templates = templates_by_level[chosen_level]

        question_text, correct_key = random.choice(templates)
        correct_option = options_pool[correct_key]

        # Pick 3 wrong options (or less if fewer)
        wrong_opts = [v for k, v in options_pool.items() if k != correct_key]
        wrong_sample = random.sample(wrong_opts, min(3, len(wrong_opts)))

        choices = [correct_option] + wrong_sample
        random.shuffle(choices)

        return {
            "type": "MCQ",
            "level": chosen_level.upper(),
            "question": question_text,
            "options": {chr(97 + i): opt for i, opt in enumerate(choices)},
            "answer": f"({chr(choices.index(correct_option) + 97)})"
        }


    def generate_mtq(self, level=None):
    # Business-friendly operator explanations
        operator_explanations = {
            "σ": "Filter records based on a condition (e.g., only employees in a certain department)",
            "π": "Show only specific columns (e.g., just names and salaries)",
            "×": "Combine every record from two tables (all possible pairs)",
            "ρ": "Rename a table or a column for clarity",
            "∪": "Combine results from two tables, removing duplicates (like a list of all customers from two regions)",
            "−": "Find records in one table that are not in another (e.g., customers who haven't made a purchase)",
            "⨝": "Combine tables based on matching values (e.g., join employees with their departments)"
        }

        # Choose pool based on level
        if level == 'level1':
            pool = [
                ("σ", operator_explanations["σ"]),
                ("π", operator_explanations["π"]),
                ("×", operator_explanations["×"]),
                ("ρ", operator_explanations["ρ"]),
            ]
        elif level == 'level2':
            pool = [
                ("∪", operator_explanations["∪"]),
                ("−", operator_explanations["−"]),
                ("⨝", operator_explanations["⨝"]),
                ("σ", operator_explanations["σ"]),
                ("π", operator_explanations["π"]),
            ]
        else:  # default or 'level3'
            pool = [
                ("⨝", operator_explanations["⨝"]),
                ("ρ", operator_explanations["ρ"]),
                ("−", operator_explanations["−"]),
                ("×", operator_explanations["×"]),
                ("σ", operator_explanations["σ"]),
                ("∪", operator_explanations["∪"]),
            ]

        # Sample 3 unique pairs
        sample_size = min(3, len(pool))
        pairs = random.sample(pool, sample_size)

        # Extract operators and corresponding business-friendly meanings
        ops = [op for op, _ in pairs]
        meanings = [desc for _, desc in pairs]

        # Shuffle meanings to create options
        shuffled_meanings = meanings[:]
        random.shuffle(shuffled_meanings)

        # Assign labels (a), (b), (c), ...
        labeled_meanings = [(f"({chr(97 + i)})", desc) for i, desc in enumerate(shuffled_meanings)]

        # Format pairs for question display
        formatted_pairs = [(op, f"{label} {desc}") for op, (label, desc) in zip(ops, labeled_meanings)]

        # Generate correct answer mappings
        answer_pairs = []
        for op, desc in pairs:
            letter_index = shuffled_meanings.index(desc)
            letter = chr(97 + letter_index)
            answer_pairs.append(f"{op} → ({letter})")

        return {
            "type": "MTQ",
            "level": level.upper() if level else "-",
            "question": "Match the relational algebra operator to its business meaning:",
            "pairs": formatted_pairs,
            "answer": ", ".join(answer_pairs)
        }



    def generate_ecq(self, level=None):
        col = self._get_random_column()
        if col is None:
            return {
                "type": "ECQ",
                "question": "Not enough data to generate question.",
                "answer": "N/A",
                "level": level.upper() if level else "-"
            }

        value = self._get_random_value(col)
        if value is None:
            return {
                "type": "ECQ",
                "question": "Not enough data to generate question.",
                "answer": "N/A",
                "level": level.upper() if level else "-"
            }

        val_fmt = self._format_value(value)
        is_numeric = isinstance(value, (int, float))
        col_phrase = self._auto_phrase(col, val_fmt)
        col_phrase_no_val = self._auto_phrase(col)

        # Define templates by difficulty level
        if level == 'level1':
            templates = [
                (
                    f"Complete the expression to get {col_phrase} only: π({col})(____)",
                    f"σ({col} = {val_fmt})({self.table_name})"
                ),
                (
                    f"Fill the blank to select records where {col_phrase_no_val} is {val_fmt}: π({col})(____)",
                    f"σ({col} = {val_fmt})({self.table_name})"
                ),
            ]
        elif level == 'level2':
            templates = [
                (
                    f"Complete: ____ {col_phrase_no_val} = {val_fmt} ({self.table_name}), to filter records by {col_phrase_no_val}.",
                    "σ"
                ),
                (
                    f"Fill the missing relation in: π({col})(σ({col} = {val_fmt})(____))",
                    self.table_name
                ),
            ]
        else:
            templates = list(filter(None, [
                (
                    f"Complete the query to get {col_phrase_no_val} from records where {col_phrase_no_val} is not {val_fmt}: π({col})(____)",
                    f"σ({col} ≠ {val_fmt})({self.table_name})"
                ),
                (
                    f"Fill in the blank to retrieve records where {col_phrase_no_val} is greater than {val_fmt} and show only the {col_phrase_no_val}: π({col})(____)",
                    f"σ({col} > {val_fmt})({self.table_name})"
                ) if is_numeric else None,
                (
                    f"Complete the expression: π({col})(____), where the selection filters records with {col_phrase_no_val} less than or equal to {val_fmt}.",
                    f"σ({col} <= {val_fmt})({self.table_name})"
                ) if is_numeric else None,
            ]))

        if not templates:
            return {
                "type": "ECQ",
                "question": "Could not generate a valid question due to unsupported attribute type.",
                "answer": "N/A",
                "level": level.upper() if level else "-"
            }

        question, answer = random.choice(templates)
        return {
            "type": "ECQ",
            "level": level.upper() if level else "-",
            "question": question,
            "answer": answer
        }


    def generate_diq(self, level=None):
        if not self.columns:
            return {
                "type": "DIQ",
                "question": "Not enough data to generate a diagram question.",
                "answer": "N/A",
                "level": level.upper() if level else "-"
            }

        # Sample tree-style layout
        col = random.choice(self.columns)
        values = self._get_sample_value(col)
        if not values:
            return {
                "type": "DIQ",
                "question": "Insufficient sample data for this table.",
                "answer": "N/A",
                "level": level.upper() if level else "-"
            }

        val = random.choice(values)
        val_fmt = f"'{val}'" if isinstance(val, str) else val

        # Define the relational algebra tree
        tree_str = f"π_{col}\n|\nσ_{{{col} = {val_fmt}}}\n|\n{self.table_name}"
        answer_set = f"{{{col}}}"

        return {
            "type": "DIQ",
            "question": f"Given the relational algebra tree:\n{tree_str}\nIdentify the resulting attribute set.",
            "tree": tree_str,
            "answer": answer_set,
            "level": level.upper() if level else "-"
        }




    def generate_oeq(self, level=None):
        col = self._get_random_column()
        if col is None:
            return {
                "type": "OEQ",
                "question": "Not enough data to generate question.",
                "answer": "N/A",
                "level": level.upper() if level else "-"
            }

        value = self._get_random_value(col)
        if value is None:
            return {
                "type": "OEQ",
                "question": "Not enough data to generate question.",
                "answer": "N/A",
                "level": level.upper() if level else "-"
            }

        val_fmt = self._format_value(value)
        is_numeric = isinstance(value, (int, float))
        col_phrase = self._auto_phrase(col, val_fmt)
        col_phrase_no_val = self._auto_phrase(col)

        if level == 'level1':
            templates = [
                (
                    f"Write a relational algebra expression to retrieve the {col_phrase} from the table.",
                    f"π({col})(σ({col} = {val_fmt})({self.table_name}))"
                ),
                (
                    f"Write an expression to get all records where {col_phrase_no_val} is not {val_fmt}.",
                    f"σ({col} ≠ {val_fmt})({self.table_name})"
                ),
            ]
        elif level == 'level2':
            templates = list(filter(None, [
                (
                    f"Write a query to select {col_phrase_no_val} values where {col_phrase_no_val} is greater than {val_fmt}.",
                    f"π({col})(σ({col} > {val_fmt})({self.table_name}))"
                ) if is_numeric else None,
                (
                    f"Write a relational algebra expression to rename the attribute {col_phrase_no_val} as new_{col_phrase_no_val}.",
                    f"ρ(new_{col} / {col})({self.table_name})"
                ),
            ]))
        else:
            templates = list(filter(None, [
                (
                    f"Write an expression to retrieve all records where {col_phrase_no_val} is either {val_fmt} or NULL.",
                    f"σ({col} = {val_fmt} ∨ {col} IS NULL)({self.table_name})"
                ),
                (
                    f"Write a relational algebra expression to find records where {col_phrase_no_val} is less than or equal to {val_fmt}.",
                    f"σ({col} <= {val_fmt})({self.table_name})"
                ) if is_numeric else None,
                (
                    f"Write a query to project the {col_phrase_no_val} from the table after filtering records where {col_phrase_no_val} is not {val_fmt}.",
                    f"π({col})(σ({col} ≠ {val_fmt})({self.table_name}))"
                ),
            ]))

        if not templates:
            return {
                "type": "OEQ",
                "question": "Could not generate a valid question due to missing numeric values or attributes.",
                "answer": "N/A",
                "level": level.upper() if level else "-"
            }

        question, answer = random.choice(templates)

        return {
            "type": "OEQ",
            "level": level.upper() if level else "-",
            "question": question,
            "answer": answer
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

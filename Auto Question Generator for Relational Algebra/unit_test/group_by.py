import random

class GroupByQuestionGenerator:
    def __init__(self, table_name, table_schema):
        self.table_name = table_name
        self.schema = table_schema
        self.columns = {
            col: details for col, details in table_schema.items()
            if isinstance(details, dict) and "type" in details
        }
        self.sample_data = table_schema.get("sample_data", [])

    def _get_columns_by_type(self, dtype):
        return [col for col, props in self.columns.items() if props["type"] == dtype]

    def _get_numeric_cols(self):
        return self._get_columns_by_type("int") + self._get_columns_by_type("float")

    def _get_categorical_cols(self):
        return self._get_columns_by_type("string")

    def _get_sample_value(self, col):
        return [row[col] for row in self.sample_data if col in row]

    def _generate_condition(self, col_list):
        conditions = []
        for col in col_list:
            values = self._get_sample_value(col)
            if not values:
                continue
            value = random.choice(values)
            col_type = self.columns[col]["type"]
            if col_type in ["int", "float"]:
                op = random.choice(["=", ">", "<", ">=", "<="])
                conditions.append(f"{col} {op} {value}")
            elif col_type == "string":
                conditions.append(f"{col} = '{value}'")
        return " AND ".join(conditions)

    def generate_bq(self, level="level1"):
        group_cols = self._get_columns_by_type("string")
        agg_cols = self._get_columns_by_type("int") + self._get_columns_by_type("float")

        if not group_cols or not agg_cols:
            raise ValueError("Not enough valid columns to perform GROUP BY.")

        group_col = random.choice(group_cols)
        agg_col = random.choice(agg_cols)
        agg_func = random.choice(["COUNT", "SUM", "AVG", "MIN", "MAX"])
        condition = ""

        # Business-friendly templates
        templates = {
            "level1": [
                "For each {group}, what is the {func} of {agg} in the '{table}' table?",
                "Show the {func} of {agg} for every {group} in '{table}'.",
                "Provide a summary of {func} of {agg} grouped by {group} from '{table}'."
            ],
            "level2": [
                "For each {group}, what is the {func} of {agg} in '{table}' where {condition}?",
                "Show the {func} of {agg} for every {group} in '{table}' only for records where {condition}.",
                "Provide a summary of {func} of {agg} grouped by {group} from '{table}', filtered by: {condition}."
            ],
            "level3": [
                "Analyze '{table}' by grouping on {group} and computing the {func} of {agg} for records where {condition}.",
                "Provide a grouped summary of '{table}' on {group} with {func} of {agg}, only for entries matching: {condition}.",
                "For business analysis, group '{table}' by {group}, calculate {func} of {agg}, and include only records where: {condition}."
            ]
        }

        level_templates = templates.get(level, templates["level1"])

        # Only level2 and level3 include filtering
        if level in ["level2", "level3"]:
            other_cols = list(set(self.columns.keys()) - {group_col, agg_col})
            if other_cols:
                condition = self._generate_condition(random.sample(other_cols, min(2, len(other_cols))))
            else:
                condition = f"{agg_col} > 0"  # Fallback

            question_template = random.choice(level_templates)
            question = question_template.format(
                table=self.table_name, group=group_col, agg=agg_col, func=agg_func.capitalize(), condition=condition
            )
            query = f"γ {group_col}, {agg_func}({agg_col}) (σ ({condition}) ({self.table_name}))"
        else:
            question_template = random.choice(level_templates)
            question = question_template.format(
                table=self.table_name, group=group_col, agg=agg_col, func=agg_func.capitalize()
            )
            query = f"γ {group_col}, {agg_func}({agg_col}) ({self.table_name})"

        return {
            "question": question,
            "answer": query,
            "level": level.upper()
        }
    
    def generate_mcq(self, level=None):
        numeric_cols = self._get_numeric_cols()
        cat_cols = self._get_categorical_cols()

        if not numeric_cols or not cat_cols:
            return {
                "type": "MCQ",
                "question": f"Table '{self.table_name}' does not have both a string and a numeric column, so a GROUP BY aggregation is not possible.",
                "options": {},
                "level": (level or "LEVEL1").upper(),
                "answer": "N/A"
            }

        group_col = random.choice(cat_cols)
        agg_col = random.choice(numeric_cols)
        op = random.choice(["sum", "avg", "count", "min", "max"])

        templates = {
            "level1": [
                f"Which relational algebra query groups the '{self.table_name}' table by '{group_col}' and calculates the {op} of '{agg_col}'?",
                f"You want to summarize the table '{self.table_name}' by '{group_col}' using {op} on '{agg_col}'. Which expression is correct?",
                f"How can you group '{self.table_name}' by '{group_col}' and apply a {op} function to '{agg_col}'?",
                f"Choose the correct relational algebra query to group '{self.table_name}' on '{group_col}' and compute the {op} of '{agg_col}'."
            ],
            "level2": [
                f"Which of the following expressions correctly applies grouping and aggregation (using {op}) on column '{agg_col}' grouped by '{group_col}' in the '{self.table_name}' table?",
                f"To generate grouped data by '{group_col}' and aggregate values from '{agg_col}' using {op}, which relational algebra expression should be used?",
                f"You are creating a report by grouping '{self.table_name}' by '{group_col}' and applying {op} to '{agg_col}'. Select the correct expression.",
                f"Which relational algebra statement performs γ operation for grouping by '{group_col}' with aggregation {op} on '{agg_col}'?"
            ],
            "level3": [
                f"A detailed analysis is needed on the '{self.table_name}' table by grouping rows by '{group_col}' and aggregating '{agg_col}' using {op}. What is the valid query?",
                f"Which relational algebra expression computes {op} of '{agg_col}' grouped by '{group_col}' while maintaining relational algebra standards?",
                f"You're performing a grouped aggregation analysis on '{self.table_name}' over '{group_col}' and aggregating '{agg_col}' with {op}. Choose the valid expression.",
                f"In the context of advanced data aggregation, which query correctly performs γ {group_col}, {op}({agg_col}) on the table '{self.table_name}'?"
            ]
        }

        normalized_level = (level or "").lower()
        if normalized_level not in templates:
            normalized_level = "level1"

        selected_templates = templates[normalized_level]

        # Correct answer
        correct = f"γ {group_col}, {op}({agg_col}) ({self.table_name})"

        # Wrong answers
        wrong1 = f"π {group_col}, {agg_col} ({self.table_name})"  # just projection
        wrong2 = f"σ {group_col} = '{group_col}' ({self.table_name})"  # just selection
        wrong3 = f"γ {agg_col}, {op}({group_col}) ({self.table_name})"  # wrong grouping

        options = [correct, wrong1, wrong2, wrong3]
        random.shuffle(options)

        answer = chr(options.index(correct) + ord('a'))
        question = random.choice(selected_templates)

        return {
            "type": "MCQ",
            "question": question,
            "options": {chr(i + 97): opt for i, opt in enumerate(options)},
            "level": normalized_level.upper(),
            "answer": f"({answer})"
        }

    def generate_tfq(self, level=None):
        numeric_cols = self._get_numeric_cols()
        cat_cols = self._get_categorical_cols()

        if not numeric_cols or not cat_cols:
            return {
                "type": "TFQ",
                "question": f"Table '{self.table_name}' does not have both a string and a numeric column, so a GROUP BY aggregation is not possible.",
                "answer": "False",
                "level": (level or "LEVEL1").upper()
            }

        group_col = random.choice(cat_cols)
        agg_col = random.choice(numeric_cols)
        operation = random.choice(["count", "sum", "avg", "min", "max"])

        normalized_level = (level or "").lower()
        if normalized_level not in ["level1", "level2", "level3"]:
            normalized_level = "level1"

        true_templates = [
            f"The expression γ {group_col}, {operation}({agg_col}) ({self.table_name}) groups rows by '{group_col}' and computes the {operation} of '{agg_col}'.",
            f"In relational algebra, γ {group_col}, {operation}({agg_col}) ({self.table_name}) is a valid GROUP BY operation.",
            f"To group '{self.table_name}' by '{group_col}' and calculate {operation} on '{agg_col}', γ {group_col}, {operation}({agg_col}) is used.",
            f"Grouping in relational algebra is done using γ, as shown in γ {group_col}, {operation}({agg_col}) ({self.table_name})."
        ]

        false_templates = [
            f"The GROUP BY operator in relational algebra is represented using σ {group_col}, {operation}({agg_col}) ({self.table_name}).",
            f"γ operator filters rows based on conditions like selection.",
            f"In relational algebra, grouping is done using π instead of γ.",
            f"The expression γ {agg_col}, {group_col} ({self.table_name}) calculates {operation} of '{group_col}' grouped by '{agg_col}'."
        ]

        is_true = random.choice([True, False])
        question = random.choice(true_templates if is_true else false_templates)

        return {
            "type": "TFQ",
            "question": question,
            "answer": "True" if is_true else "False",
            "level": normalized_level.upper()
        }

    def generate_mtq(self, level=None):
        numeric_cols = self._get_numeric_cols()
        cat_cols = self._get_categorical_cols()

        if not numeric_cols or not cat_cols:
            return {
                "type": "MTQ",
                "question": f"Table '{self.table_name}' does not have both a string and a numeric column, so a GROUP BY aggregation is not possible.",
                "options": {},
                "level": (level or "LEVEL1").upper(),
                "answers": {},
                "answer": ""
            }

        group_col = random.choice(cat_cols)
        agg_col = random.choice(numeric_cols)
        op = random.choice(["sum", "avg", "count", "min", "max"])

        base_templates = {
            "level1": [
                (f"The query groups records based on the '{group_col}' column.", True),
                (f"The aggregation function applied is {op} on the '{agg_col}' column.", True),
                (f"The query filters rows where '{group_col}' equals some value.", False),
                (f"The query will return one row per unique '{group_col}' value.", True)
            ],
            "level2": [
                (f"The aggregation operation {op} is applied to '{agg_col}' after grouping by '{group_col}'.", True),
                (f"The query performs a selection operation on the '{group_col}' column.", False),
                (f"The output contains grouped tuples along with the aggregated result.", True),
                (f"The γ symbol in relational algebra represents a projection operation.", False)
            ],
            "level3": [
                (f"This query is useful to compute summary statistics grouped by '{group_col}'.", True),
                (f"The query can be used without any grouping columns.", False),
                (f"Aggregation functions like {op} always return a single value for the entire relation.", False),
                (f"Grouping by '{group_col}' followed by {op} aggregation returns results partitioned by unique '{group_col}' values.", True)
            ]
        }

        normalized_level = (level or "").lower()
        if normalized_level not in base_templates:
            normalized_level = "level1"

        statements_with_correct = base_templates[normalized_level]
        statements = [s for s, _ in statements_with_correct]
        correct_answers = [a for _, a in statements_with_correct]

        randomized_answers = correct_answers

        options = {chr(i + 97): stmt for i, stmt in enumerate(statements)}
        answers = {chr(i + 97): val for i, val in enumerate(randomized_answers)}

        answer_letters = [k for k, v in answers.items() if v]
        answer_str = ", ".join(answer_letters)

        question_text = f"Consider the relational algebra query γ_{{{group_col}, {op}({agg_col})}}({self.table_name}). Identify which of the following statements are TRUE:"

        return {
            "type": "MTQ",
            "question": question_text,
            "options": options,
            "level": normalized_level.upper(),
            "answers": answers,
            "answer": answer_str
        }

    def generate_ecq(self, level=None):
        numeric_cols = self._get_numeric_cols()
        cat_cols = self._get_categorical_cols()

        if not numeric_cols or not cat_cols:
            return {
                "type": "ECQ",
                "question": f"Table '{self.table_name}' does not have both a string and a numeric column, so a GROUP BY aggregation is not possible.",
                "options": {},
                "level": (level or "LEVEL1").upper(),
                "answer": "N/A"
            }

        group_col = random.choice(cat_cols)
        agg_col = random.choice(numeric_cols)
        op = random.choice(["sum", "avg", "count", "min", "max"])
        normalized_level = (level or "level1").lower()

        # Try to get a value from sample data for the condition, else use a default
        values = self._get_sample_value(agg_col)
        value = random.choice(values) if values else 100

        templates = {
            "level1": [
                (
                    f"Complete the expression:\n"
                    f"γ_{{{group_col}, {op}({agg_col})}} ( ___ ), where we want to group '{self.table_name}' by '{group_col}' and compute {op} of '{agg_col}'.",
                    f"{self.table_name}"
                ),
                (
                    f"Fill in the blank: π {group_col} ( ___ ), where we want all unique {group_col}s from '{self.table_name}'.",
                    f"{self.table_name}"
                ),
                (
                    f"Complete the relational algebra: σ {group_col} = 'X' ( ___ ), to select all records from '{self.table_name}' where {group_col} is 'X'.",
                    f"{self.table_name}"
                ),
                (
                    f"Fill in the blank: π {agg_col} ( ___ ), to project all {agg_col} values from '{self.table_name}'.",
                    f"{self.table_name}"
                ),
                (
                    f"Complete the expression: γ_{{{group_col}}} ( ___ ), to group '{self.table_name}' by '{group_col}' without aggregation.",
                    f"{self.table_name}"
                ),
            ],
            "level2": [
                (
                    f"Complete the expression:\n"
                    f"γ_{{{group_col}, {op}({agg_col})}} ( σ {agg_col} > {value} ( ___ ) ), to group '{self.table_name}' by '{group_col}' and aggregate {agg_col} > {value}.",
                    f"{self.table_name}"
                ),
                (
                    f"Fill in the blank: π {group_col} ( σ {agg_col} > {value} ( ___ ) ), where we want all {group_col}s from '{self.table_name}' with {agg_col} > {value}.",
                    f"{self.table_name}"
                ),
                (
                    f"Complete the relational algebra: σ {agg_col} < {value} ( ___ ), to select all records from '{self.table_name}' where {agg_col} < {value}.",
                    f"{self.table_name}"
                ),
                (
                    f"Fill in the blank: γ_{{{group_col}, {op}({agg_col})}} ( σ {group_col} = 'Y' ( ___ ) ), to group '{self.table_name}' by '{group_col}' where {group_col} = 'Y'.",
                    f"{self.table_name}"
                ),
                (
                    f"Complete the expression: π {group_col}, {agg_col} ( σ {agg_col} >= {value} ( ___ ) ), to project {group_col} and {agg_col} for records with {agg_col} >= {value}.",
                    f"{self.table_name}"
                ),
            ],
            "level3": [
                (
                    f"Complete the expression:\n"
                    f"π {group_col}, {op}({agg_col}) ( γ_{{{group_col}, {op}({agg_col})}} ( σ {agg_col} > {value} ( ___ ) ) ), to get {group_col} and {op}({agg_col}) for groups with {agg_col} > {value}.",
                    f"{self.table_name}"
                ),
                (
                    f"Fill in the blank: γ_{{{group_col}, {op}({agg_col})}} ( σ {group_col} = '{group_col}' ( ___ ) ), to group '{self.table_name}' by '{group_col}' where {group_col} = '{group_col}'.",
                    f"{self.table_name}"
                ),
                (
                    f"Complete the relational algebra: σ {op}({agg_col}) > {value} ( γ_{{{group_col}, {op}({agg_col})}} ( ___ ) ), to select groups where aggregated {agg_col} is greater than {value}.",
                    f"{self.table_name}"
                ),
                (
                    f"Fill in the blank: π {group_col}, {op}({agg_col}) ( σ {op}({agg_col}) < {value} ( γ_{{{group_col}, {op}({agg_col})}} ( ___ ) ) ), to get groups with aggregated {agg_col} less than {value}.",
                    f"{self.table_name}"
                ),
                (
                    f"Complete the expression: γ_{{{group_col}, {op}({agg_col})}} ( σ {group_col} != 'Z' ( ___ ) ), to group '{self.table_name}' by '{group_col}' excluding 'Z'.",
                    f"{self.table_name}"
                ),
            ]
        }

        if normalized_level not in templates:
            normalized_level = "level1"

        question_template, answer = random.choice(templates[normalized_level])

        return {
            "type": "ECQ",
            "question": question_template,
            "level": normalized_level.upper(),
            "answer": answer
        }
    def generate_diq(self, level=None):
        numeric_cols = self._get_numeric_cols()
        cat_cols = self._get_categorical_cols()

        if not numeric_cols or not cat_cols:
            return {
                "type": "DIQ",
                "question": f"Table '{self.table_name}' does not have both a string and a numeric column, so a GROUP BY aggregation is not possible.",
                "level": (level or "LEVEL1").upper(),
                "answer": "N/A",
                "tree": ""
            }

        group_col = random.choice(cat_cols)
        agg_col = random.choice(numeric_cols)
        op = random.choice(["sum", "avg", "count", "min", "max"])

        templates = {
            "level1": [
                f"Write the relational algebra query to group the '{self.table_name}' table by '{group_col}' and compute the {op} of '{agg_col}'.",
                f"Formulate a relational algebra expression to find the {op} of '{agg_col}' for each unique '{group_col}' in '{self.table_name}'.",
                f"Generate a relational algebra query that groups data by '{group_col}' and calculates the {op} for '{agg_col}'."
            ],
            "level2": [
                f"Write a relational algebra query to group '{self.table_name}' by '{group_col}', computing the {op} of '{agg_col}', with a condition filtering '{group_col}' = some value.",
                f"Construct a relational algebra expression that first filters rows where '{group_col}' equals a specific value, then groups by '{group_col}' and calculates the {op} of '{agg_col}'.",
                f"Create a query that filters '{self.table_name}' by '{group_col}' and then performs grouping by '{group_col}' with aggregation {op} on '{agg_col}'."
            ],
            "level3": [
                f"Write a relational algebra expression that groups '{self.table_name}' by '{group_col}', computes the {op} of '{agg_col}', and applies a selection on the aggregated results where the {op} is greater than a given threshold.",
                f"Formulate a query that performs grouping and aggregation ({op} on '{agg_col}') by '{group_col}', followed by a selection filtering groups with aggregated value exceeding a certain limit.",
                f"Generate a relational algebra expression to group '{self.table_name}' by '{group_col}', aggregate using {op} on '{agg_col}', and select groups based on a condition on the aggregated result."
            ]
        }

        normalized_level = (level or "").lower()
        if normalized_level not in templates:
            normalized_level = "level1"

        question_text = random.choice(templates[normalized_level])

        # Build the tree representation
        if normalized_level == "level1":
            answer = f"γ_{{{group_col}, {op}({agg_col})}}({self.table_name})"
            tree = (
                f"    γ({group_col}, {op}({agg_col}))\n"
                f"         |\n"
                f"    {self.table_name}"
            )
        elif normalized_level == "level2":
            answer = f"σ_{{{group_col} = 'value'}} (γ_{{{group_col}, {op}({agg_col})}}({self.table_name}))"
            tree = (
                f"    σ({group_col} = value)\n"
                f"         |\n"
                f"    γ({group_col}, {op}({agg_col}))\n"
                f"         |\n"
                f"    {self.table_name}"
            )
        else:
            answer = f"σ_{{{op}({agg_col}) > threshold}} (γ_{{{group_col}, {op}({agg_col})}}({self.table_name}))"
            tree = (
                f"    σ({op}({agg_col}) > threshold)\n"
                f"         |\n"
                f"    γ({group_col}, {op}({agg_col}))\n"
                f"         |\n"
                f"    {self.table_name}"
            )

        return {
            "type": "DIQ",
            "question": question_text,
            "level": normalized_level.upper(),
            "answer": answer,
            "tree": tree
        }

    def generate_oeq(self, level=None):
        numeric_cols = self._get_numeric_cols()
        cat_cols = self._get_categorical_cols()

        if not numeric_cols or not cat_cols:
            return {
                "type": "OEQ",
                "question": f"Why can't GROUP BY be performed on table '{self.table_name}'?",
                "level": (level or "LEVEL1").upper(),
                "answer": f"Because the table does not have both a string (for grouping) and a numeric (for aggregation) column."
            }

        group_col = random.choice(cat_cols)
        agg_col = random.choice(numeric_cols)
        op = random.choice(["sum", "avg", "count", "min", "max"])

        templates_and_answers = {
            "level1": [
                (
                    f"What is the purpose of the GROUP BY operation on the '{group_col}' column in the '{self.table_name}' table?",
                    f"The GROUP BY operation groups the rows of the '{self.table_name}' table based on unique values in the '{group_col}' column, "
                    f"allowing aggregation functions like {op} to be applied on each group separately."
                ),
                (
                    f"Explain how the aggregation function {op} works when applied to the '{agg_col}' column grouped by '{group_col}'.",
                    f"The {op} function computes the {op} value of the '{agg_col}' column for each group defined by unique '{group_col}' values, "
                    f"providing summary statistics for each group."
                ),
                (
                    f"Describe the effect of grouping the '{self.table_name}' table by '{group_col}'.",
                    f"Grouping by '{group_col}' organizes the data into subsets where all rows in each subset have the same value for '{group_col}', "
                    f"enabling aggregate calculations like {op} on other columns."
                )
            ],
            "level2": [
                (
                    f"Explain how filtering rows before performing a GROUP BY on '{group_col}' affects the aggregated results on '{agg_col}'.",
                    f"Filtering rows before grouping restricts the dataset to only those rows that satisfy the filter condition, "
                    f"which means the aggregation on '{agg_col}' will be computed only for the filtered data, possibly changing the results."
                ),
                (
                    f"Describe a scenario where grouping by '{group_col}' and calculating the {op} of '{agg_col}' is useful.",
                    f"For example, in a sales database, grouping by '{group_col}' (e.g., 'region') and calculating the {op} of '{agg_col}' (e.g., 'sales') "
                    f"helps summarize total or average sales per region."
                ),
                (
                    f"What is the significance of applying a selection condition before or after the GROUP BY operation in relational algebra?",
                    f"Applying selection before grouping filters the data that will be grouped, while selection after grouping filters the aggregated groups. "
                    f"This difference affects the final aggregated results."
                )
            ],
            "level3": [
                (
                    f"Discuss the differences between performing aggregation with and without grouping by '{group_col}' in relational algebra.",
                    f"Aggregation without grouping applies the function over the entire relation producing a single summary value, while aggregation with grouping "
                    f"partitions the data by '{group_col}' and computes the aggregate per group, resulting in multiple summary rows."
                ),
                (
                    f"Explain how relational algebra handles grouping by '{group_col}' and aggregation when multiple grouping columns are involved.",
                    f"When grouping by multiple columns, relational algebra creates groups based on unique combinations of those columns' values, "
                    f"and aggregation functions are applied within each group."
                ),
                (
                    f"Describe how filtering aggregated results (e.g., groups having {op}('{agg_col}') > some value) can be expressed and why it is important.",
                    f"Filtering aggregated results can be done by applying a selection condition on the aggregation result, known as 'HAVING' in SQL. "
                    f"It is important for focusing on groups that meet certain criteria, like only groups with {op}('{agg_col}') above a threshold."
                )
            ]
        }

        normalized_level = (level or "").lower()
        if normalized_level not in templates_and_answers:
            normalized_level = "level1"

        question, answer = random.choice(templates_and_answers[normalized_level])

        return {
            "type": "OEQ",
            "question": question,
            "level": normalized_level.upper(),
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
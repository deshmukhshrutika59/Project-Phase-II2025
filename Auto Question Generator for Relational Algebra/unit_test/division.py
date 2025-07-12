import random

class DivisionGenerator:
    def __init__(self, table1_name, table2_name, table1_schema, table2_schema):
        self.table1 = table1_name
        self.table2 = table2_name
        self.table1_schema = table1_schema
        self.table2_schema = table2_schema

        self.columns1 = [col for col in table1_schema if col != "sample_data"]
        self.columns2 = [col for col in table2_schema if col != "sample_data"]
        self.sample_data1 = table1_schema.get("sample_data", [])
        self.sample_data2 = table2_schema.get("sample_data", [])

        # For type-aware condition generation
        self.columns1_types = {col: dt for col, dt in table1_schema.items() if isinstance(dt, dict) and "type" in dt}
        self.columns2_types = {col: dt for col, dt in table2_schema.items() if isinstance(dt, dict) and "type" in dt}

    def _get_shared_columns(self):
        return list(set(self.columns1).intersection(self.columns2))

    def _get_primary_key(self):
        for col in self.columns1:
            if col == "id" or col.endswith("_id"):
                return col
        return self.columns1[0] if self.columns1 else "id"

    def _generate_condition(self, shared):
        conditions = []
        for col in shared:
            values = [row[col] for row in self.sample_data1 if col in row]
            if not values:
                continue
            value = random.choice(values)
            col_type = self.columns1_types.get(col, {}).get("type", None)
            if col_type in ["int", "float"]:
                conditions.append(f"{col} = {value}")
            elif col_type == "string" or isinstance(value, str):
                conditions.append(f"{col} = '{value}'")
            elif col_type == "bool":
                conditions.append(f"{col} = {str(value).upper()}")
            else:
                conditions.append(f"{col} = {value}")
        return " AND ".join(conditions) or (f"{shared[0]} IS NOT NULL" if shared else "")

    def generate_bq(self, level="level1"):
        shared_attributes = self._get_shared_columns()
        if not shared_attributes:
            raise ValueError(f"No shared attributes between {self.table1} and {self.table2}.")

        attrs_str = ', '.join(shared_attributes)
        condition = self._generate_condition(shared_attributes)

        # Business-friendly templates
        templates = {
            "level1": [
                f"Which {self.table1} records are associated with every entry in {self.table2}? (e.g., Which employees have completed all required trainings?)",
                f"Find all {self.table1} entries that are linked to every {self.table2} entry. (e.g., Which products are available in all stores?)",
                f"List all {self.table1} items that relate to each and every {self.table2} entry. (e.g., Which students are enrolled in all mandatory courses?)"
            ],
            "level2": [
                f"Retrieve the IDs from {self.table1} that are connected to all records in {self.table2}. (e.g., Which customers have purchased every product?)",
                f"Which {self.table1} identifiers appear with all values of {self.table2}? (e.g., Which suppliers provide all listed materials?)",
                f"Extract the primary keys from {self.table1} that satisfy all associations in {self.table2}. (e.g., Which doctors have appointments with all patients?)"
            ],
            "level3": [
                f"From {self.table1}, get attributes {attrs_str} associated with every {self.table2} entry, but only where {condition}. (e.g., Which employees in a certain department have completed all trainings?)",
                f"Find all tuples in {self.table1} with values ({attrs_str}) linked to all entries of {self.table2}, under the condition {condition}.",
                f"Which combinations of {attrs_str} in {self.table1} relate to all rows in {self.table2} where {condition} applies?"
            ]
        }

        query_templates = {
            "level1": f"{self.table1} ÷ {self.table2}",
            "level2": f"π({self._get_primary_key()})({self.table1} ÷ {self.table2})",
            "level3": f"π({attrs_str}) (σ({condition})({self.table1}) ÷ {self.table2})"
        }

        level = level.lower()
        question = random.choice(templates.get(level, templates["level1"]))
        query = query_templates.get(level, query_templates["level1"])

        return {
            "type": "DIVISION",
            "question": question,
            "query": query,
            "answer": f"The correct relational algebra expression is: {query}",
            "level": level.upper()
        }
    
    def generate_mcq(self, level=None):
        shared = self._get_shared_columns()
        primary = self._get_primary_key()
        level = (level or "level1").lower()

        correct = {
            "level1": f"{self.table1} ÷ {self.table2}",
            "level2": f"π({primary})({self.table1} ÷ {self.table2})",
            "level3": f"π({', '.join(shared)}) (σ({self._generate_condition(shared)})({self.table1}) ÷ {self.table2})"
        }[level]

        wrong1 = f"{self.table1} ⨝ {self.table2}"
        wrong2 = f"π({primary})({self.table1}) ∪ {self.table2}"
        wrong3 = f"σ({self._generate_condition(shared)})({self.table1}) ÷ {self.table2}"

        options = [correct, wrong1, wrong2, wrong3]
        random.shuffle(options)
        answer = chr(options.index(correct) + ord('a'))

        question = f"Which relational algebra expression returns all records from '{self.table1}' that are related to all rows in '{self.table2}'?"

        return {
            "type": "MCQ",
            "question": question,
            "options": {chr(97 + i): opt for i, opt in enumerate(options)},
            "answer": f"({answer})",
            "level": level.upper()
        }

    def generate_oeq(self, level=None):
        shared = self._get_shared_columns()
        primary = self._get_primary_key()
        level = (level or "level1").lower()
        condition = self._generate_condition(shared)

        question_templates = {
            "level1": f"Write a relational algebra query to find all records from '{self.table1}' that are related to every row in '{self.table2}'.",
            "level2": f"Write a query to find {primary} values in '{self.table1}' that are associated with all rows of '{self.table2}'.",
            "level3": f"Construct a query to find ({', '.join(shared)}) from '{self.table1}' associated with every '{self.table2}' entry where {condition}."
        }

        answer_templates = {
            "level1": f"{self.table1} ÷ {self.table2}",
            "level2": f"π({primary})({self.table1} ÷ {self.table2})",
            "level3": f"π({', '.join(shared)}) (σ({condition})({self.table1}) ÷ {self.table2})"
        }

        return {
            "type": "OEQ",
            "question": question_templates[level],
            "answer": answer_templates[level],
            "level": level.upper()
        }

    def generate_tfq(self, level=None):
        level = (level or "level1").lower()
        correct = random.choice([True, False])
        shared = self._get_shared_columns()
        condition = self._generate_condition(shared)

        if correct:
            statement = {
                "level1": f"{self.table1} ÷ {self.table2} finds entries in '{self.table1}' associated with all rows in '{self.table2}'.",
                "level2": f"π(id)({self.table1} ÷ {self.table2}) retrieves identifiers from '{self.table1}' connected to every entry in '{self.table2}'.",
                "level3": f"π({', '.join(shared)}) (σ({condition})({self.table1}) ÷ {self.table2}) selects attributes from '{self.table1}' related to all of '{self.table2}' where {condition}."
            }[level]
        else:
            statement = f"{self.table1} ∪ {self.table2} is used to perform a division operation in relational algebra."

        return {
            "type": "TFQ",
            "question": statement,
            "answer": "True" if correct else "False",
            "level": level.upper()
        }

    def generate_mtq(self, level=None):
        level = (level or "level1").lower()
        pairs = {
            "level1": [
                ("÷", "Find entries associated with all records in another table"),
                ("π", "Project specific columns"),
                ("σ", "Select rows based on condition")
            ],
            "level2": [
                ("÷", "Divide one relation by another to find universal associations"),
                ("π", "Select columns from a table"),
                ("⨝", "Join two relations based on a condition")
            ],
            "level3": [
                ("÷", "Used to find all values in one relation associated with every value in another"),
                ("π", "Projects selected attributes"),
                ("σ", "Applies a condition on rows"),
                ("∪", "Combines tuples from two relations")
            ]
        }[level]

        random.shuffle(pairs)
        answer = ", ".join([f"{p[0]} → ({chr(97 + i)})" for i, p in enumerate(pairs)])

        return {
            "type": "MTQ",
            "question": "Match the relational algebra operators with their correct description:",
            "pairs": [(op, f"({chr(97 + i)}) {desc}") for i, (op, desc) in enumerate(pairs)],
            "answer": answer,
            "level": level.upper()
        }

    def generate_diq(self, level=None):
        level = (level or "level1").lower()
        shared = self._get_shared_columns()
        condition = self._generate_condition(shared)
        tree = {
            "level1": (
                f"    {self.table1}\n"
                f"      |\n"
                f"    ÷\n"
                f"      |\n"
                f"    {self.table2}"
            ),
            "level2": (
                f"    π({self._get_primary_key()})\n"
                f"      |\n"
                f"    ÷\n"
                f"   /   \\\n"
                f"{self.table1}   {self.table2}"
            ),
            "level3": (
                f"    π({', '.join(shared)})\n"
                f"      |\n"
                f"    ÷\n"
                f"   /   \\\n"
                f"σ({condition})   {self.table2}\n"
                f"    |\n"
                f" {self.table1}"
            )
        }[level]

        return {
            "type": "DIQ",
            "tree": tree,
            "question": "What result will this relational algebra expression tree produce?",
            "answer": f"{self.table1} ÷ {self.table2}" if level == "level1" else "Depends on projection/condition",
            "level": level.upper()
        }

    def generate_ecq(self, level=None):
        shared = self._get_shared_columns()
        level = (level or "level1").lower()
        question = (
            f"Explain the purpose of the division operator (÷) in relational algebra using the tables '{self.table1}' and '{self.table2}'."
        )
        answer = (
            f"The division operator (÷) returns those records in '{self.table1}' that are associated with every entry in '{self.table2}'. "
            f"It is useful for expressing queries like: 'Find all {self.table1} that are related to all {self.table2}'."
        )

        return {
            "type": "ECQ",
            "level": level.upper(),
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
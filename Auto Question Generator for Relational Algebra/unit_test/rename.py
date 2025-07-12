import random
import string
class RenameGenerator:
    def __init__(self, table_name=None, table_schema=None):
        self.table_name = table_name
        self.schema = table_schema or {}
        self.columns = [col for col in self.schema if col != "sample_data"]
        self.sample_data = self.schema.get("sample_data", [])

    def random_suffix(self, length=3):
        return ''.join(random.choices(string.ascii_lowercase, k=length))

    def _get_random_column(self):
        return random.choice(self.columns) if self.columns else None

    def generate_bq(self, level="level1"):
        if not self.table_name:
            return {"type": "BQ", "question": "Table name is required.", "answer": "N/A", "level": level.upper()}

        new_name = f"{self.table_name}_{self.random_suffix()}"
        templates = [
            "Suppose you want to call the '{table}' table '{new_name}'. How would you write this in relational algebra?",
            "Your manager asks you to rename the table '{table}' to '{new_name}'. What is the correct expression?",
            "The business wants to change the name of the '{table}' table to '{new_name}'. Write the relational algebra for this.",
            "You need to update the system so that the '{table}' table is now known as '{new_name}'. How do you do this in relational algebra?",
            "Rename the '{table}' table to '{new_name}' as per the new business requirement. What is the relational algebra expression?"
        ]

        question = random.choice(templates).format(table=self.table_name, new_name=new_name)
        answer = f"ρ {new_name}({self.table_name})"

        return {"type": "BQ", "question": question, "answer": answer, "level": level.upper()}


    def generate_tfq(self, level="level1"):
        col = self._get_random_column()
        if not col:
            return {"type": "TFQ", "question": "Not enough data to generate question.", "answer": "N/A", "level": level.upper()}

        new_name = f"new_{col}"
        templates = [
            (f"True or False: The expression ρ({new_name} / {col})({self.table_name}) renames attribute {col} to {new_name}.", True),
            (f"True or False: The rename operation ρ({new_name} / {col}) changes the table name to {new_name}.", False),
            (f"True or False: The expression ρ({new_name} / {col}) modifies the values stored in the attribute.", False),
            (f"True or False: The rename operator ρ allows modifying both data and schema.", False),
            (f"True or False: Renaming an attribute with ρ changes the column name but not its data.", True),
            (f"True or False: The operator ρ is only used for renaming tables, not columns.", False),
            (f"True or False: ρ({new_name} / {col})({self.table_name}) results in the column {col} being replaced with {new_name}.", True)
        ]

        question, is_true = random.choice(templates)
        return {"type": "TFQ", "question": question, "answer": "True" if is_true else "False", "level": level.upper()}

    def generate_mcq(self, level="level1"):
        col = self._get_random_column()
        if not col:
            return {"type": "MCQ", "question": "Not enough data to generate question.", "options": {}, "answer": "N/A", "level": level.upper()}

        new_name = f"new_{col}"
        correct = f"ρ({new_name} / {col})({self.table_name})"
        options = [
            correct,
            f"π({new_name})({self.table_name})",
            f"σ({col} = {new_name})({self.table_name})",
            f"ρ({col} / {new_name})({self.table_name})",
            "None of the above."
        ]

        question_templates = [
            f"Which relational algebra expression correctly renames attribute {col} to {new_name}?",
            f"You want to rename column {col} to {new_name}. What’s the correct query?",
            f"Choose the valid expression to change the column name from {col} to {new_name}.",
            f"Select the correct relational algebra expression for renaming {col} to {new_name}."
        ]

        question = random.choice(question_templates)
        choices = random.sample(options, 4)
        if correct not in choices:
            choices[random.randint(0, 3)] = correct

        answer = f"({chr(choices.index(correct) + 97)})"

        return {
            "type": "MCQ",
            "question": question,
            "options": {chr(97 + i): opt for i, opt in enumerate(choices)},
            "answer": answer,
            "level": level.upper()
        }

    def generate_mtq(self, level="level1"):
        pairs = [
            ("ρ", "Rename relation or attribute"),
            ("σ", "Filter rows based on a condition"),
            ("π", "Select specific columns"),
            ("∪", "Union of two relations"),
            ("⨝", "Join two relations")
        ]
        selected = random.sample(pairs, 3 + (level == "level3"))
        ops = [p[0] for p in selected]
        meanings = [p[1] for p in selected]
        shuffled = meanings[:]
        random.shuffle(shuffled)

        formatted = [(op, f"({chr(97 + i)}) {desc}") for i, (op, desc) in enumerate(zip(ops, shuffled))]
        answer = ", ".join([f"{op} → ({chr(97 + shuffled.index(desc))})" for op, desc in zip(ops, meanings)])

        return {
            "type": "MTQ",
            "question": "Match the relational algebra operator to its correct purpose:",
            "pairs": formatted,
            "answer": answer,
            "level": level.upper()
        }

    def generate_ecq(self, level="level1"):
        col = self._get_random_column()
        if not col:
            return {"type": "ECQ", "question": "Not enough data to generate question.", "answer": "N/A", "level": level.upper()}

        new_name = f"new_{col}"
        templates = [
            (f"Complete the expression to rename attribute {col} to {new_name}: ρ(____ / {col})({self.table_name})", new_name),
            (f"Fill the blank to rename attribute {col}: ρ({new_name} / ____)({self.table_name})", col),
            (f"Complete the relational algebra statement to rename the table: ρ(____)({self.table_name})", f"new_{self.table_name}"),
            (f"You want to change the name of column {col} in {self.table_name}. What name completes this: ρ(new_name / ____)({self.table_name})?", col),
            (f"Insert the correct table name in: ρ(new_{self.table_name})(____)", self.table_name)
        ]

        question, answer = random.choice(templates)
        return {"type": "ECQ", "question": question, "answer": answer, "level": level.upper()}

    def generate_diq(self, level="level1"):
        col = self._get_random_column()
        if not col:
            return {"type": "DIQ", "question": "Not enough data to generate question.", "answer": "N/A", "tree": "", "level": level.upper()}

        new_name = f"new_{col}"
        templates = [
            (f"Given the relational algebra tree:\n  ρ({new_name} / {col})\n    |\n  {self.table_name}\nWhat does this operation do?", f"Renames attribute {col} to {new_name}"),
            (f"Identify the resulting schema attribute after applying ρ({new_name} / {col})({self.table_name}).", f"{new_name} replaces {col}"),
            (f"Examine this tree and state what changes: ρ({new_name} / {col})\n|\n{self.table_name}", f"{col} is renamed to {new_name}"),
            (f"What is the effect of this RA tree on the schema?\n  ρ({new_name} / {col})\n    |\n  {self.table_name}", f"Attribute {col} becomes {new_name}"),
            (f"Interpret the following RA tree:\n  ρ({new_name} / {col})\n    |\n  {self.table_name}\nWhat does the rename operator do here?", f"It changes the column name {col} to {new_name}"),
            (f"Analyze the query tree:\n  ρ({new_name} / {col})\n    |\n  {self.table_name}\nWhich column is being renamed and to what?", f"{col} is renamed to {new_name}"),
            (f"This operation:\n  ρ({new_name} / {col})\n    |\n  {self.table_name}\nrepresents what type of schema change?", f"Rename column {col} to {new_name}")
        ]

        question, answer = random.choice(templates)
        return {
            "type": "DIQ",
            "question": question,
            "tree": f"  ρ({new_name} / {col})\n    |\n  {self.table_name}",
            "answer": answer,
            "level": level.upper()
        }

    def generate_oeq(self, level="level1"):
        col = self._get_random_column()
        if not col:
            return {"type": "OEQ", "question": "Not enough data to generate question.", "answer": "N/A", "level": level.upper()}

        new_name = f"new_{col}"
        templates = [
            (f"Write a relational algebra expression to rename attribute {col} to {new_name} in relation {self.table_name}.", f"ρ({new_name} / {col})({self.table_name})"),
            (f"Write an expression to rename the relation {self.table_name} to new_{self.table_name}.", f"ρ(new_{self.table_name})({self.table_name})"),
            (f"How would you rename the column {col} in table {self.table_name}?", f"ρ({new_name} / {col})({self.table_name})"),
            (f"Write the RA expression for changing {col} to {new_name} in {self.table_name}.", f"ρ({new_name} / {col})({self.table_name})")
        ]

        question, answer = random.choice(templates)
        return {"type": "OEQ", "question": question, "answer": answer, "level": level.upper()}

    def generate_all_question_types(self, level="level1"):
        output = []
        for method_name in [
            "generate_bq", "generate_tfq", "generate_mcq",
            "generate_mtq", "generate_ecq", "generate_diq", "generate_oeq"
        ]:
            try:
                method = getattr(self, method_name)
                result = method(level=level)
                result["type"] = method_name.split("_")[1].upper()
                result["level"] = level.upper()
                output.append(result)
            except Exception as e:
                output.append({
                    "type": method_name.split("_")[1].upper(),
                    "error": str(e),
                    "level": level.upper()
                })
        return output

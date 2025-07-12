import random
from schemas.schema import get_schema_by_name

class JoinGenerator:
    def __init__(self, table_name=None, table_schema=None, schema=None, seed=None):
        self.table_name = table_name
        self.table_schema = table_schema
        self.schema = schema if schema else get_schema_by_name()
        self.foreign_keys = self._identify_foreign_keys()
        self.used_combinations = set()
        self.random_seed = seed
        if self.random_seed is not None:
            random.seed(self.random_seed)

    def _identify_foreign_keys(self):
        foreign_keys = {}
        for table_name, schema in self.schema.items():
            for column, details in schema.items():
                if isinstance(details, dict) and 'foreign_key' in details:
                    ref = details['foreign_key']
                    ref_table = ref.split(".")[0]
                    if table_name not in foreign_keys:
                        foreign_keys[table_name] = []
                    foreign_keys[table_name].append((column, ref))
            
            # Detect self-join candidates: multiple FKs to same table
            if table_name in foreign_keys:
                ref_tables = [ref.split(".")[0] for _, ref in foreign_keys[table_name]]
                if ref_tables.count(table_name) >= 2:
                    foreign_keys[table_name].append(("__self_join__", f"{table_name}.{table_name}"))

        return foreign_keys


    def _get_random_sample(self, table_name, column_name, num_values=1):
        sample_data = self.schema.get(table_name, {}).get("sample_data", [])
        column_values = list({row[column_name] for row in sample_data if column_name in row})
        if column_values:
            return random.sample(column_values, min(num_values, len(column_values)))
        else:
            return []

    def _generate_conditions(self, fk_column, sample_values):
        if len(sample_values) >= 2:
            condition1 = f"{fk_column} = '{sample_values[0]}'"
            condition2 = f"{fk_column} != '{sample_values[1]}'"
        elif len(sample_values) == 1:
            condition1 = f"{fk_column} = '{sample_values[0]}'"
            condition2 = f"{fk_column} != '{sample_values[0]}'"
        else:
            condition1 = f"{fk_column} IS NOT NULL"
            condition2 = f"{fk_column} IS NOT NULL"
        return condition1, condition2

    def _col_phrase(self, col):
        if col.endswith("_id"):
            return f"{col.replace('_', ' ').capitalize()} (ID)"
        elif col == "name":
            return "Name"
        else:
            return col.replace('_', ' ').capitalize()

    def generate_bq(self, join_type="inner", level="level1"):
        if not self.foreign_keys:
            raise ValueError("No foreign key relationships found in the schema.")

        templates = {
            "inner": {
                1: [
                    "Show all records where '{table1}' and '{table2}' have matching {col1_phrase}.",
                    "List the combined data from '{table1}' and '{table2}' where {col1_phrase} is the same in both tables.",
                    "Find all entries that appear in both '{table1}' and '{table2}' with the same {col1_phrase}.",
                    "Combine '{table1}' and '{table2}' to see only the rows where {col1_phrase} matches."
                ],
                2: [
                    "Find all rows where '{table1}' and '{table2}' match on {col1_phrase}, and only include those matches.",
                    "Combine '{table1}' and '{table2}' by matching {col1_phrase} values, and show only the matching records.",
                    "Show the data from '{table1}' and '{table2}' where {col1_phrase} is equal, and apply the filter {condition1}.",
                    "List the results of joining '{table1}' and '{table2}' on {col1_phrase} and filter by {condition1}."
                ],
                3: [
                    "Show the results of joining '{table1}' and '{table2}' where {col1_phrase} matches and also meets the condition: {condition1}.",
                    "List records from '{table1}' and '{table2}' where {col1_phrase} matches and also satisfy {condition1} and {condition2}.",
                    "Combine '{table1}' and '{table2}' on {col1_phrase}, but only include rows that meet both {condition1} and {condition2}.",
                    "Display joined data from '{table1}' and '{table2}' where {col1_phrase} matches and extra filters apply."
                ]
            },
            "left_outer": {
                1: [
                    "Show all records from '{table1}', and add matching data from '{table2}' where {col1_phrase} is the same. If there is no match, keep the '{table1}' data.",
                    "List every row from '{table1}' and fill in data from '{table2}' where {col1_phrase} matches. If not, leave those fields empty.",
                    "Display all entries from '{table1}', adding info from '{table2}' when {col1_phrase} matches.",
                    "For each row in '{table1}', attach matching '{table2}' data on {col1_phrase}, or leave blank if no match."
                ],
                2: [
                    "Show all rows from '{table1}' and matching ones from '{table2}' where {col1_phrase} matches and also meets {condition1}.",
                    "List every '{table1}' record, adding '{table2}' data if {col1_phrase} matches and {condition1} is true.",
                    "Display all '{table1}' rows, with '{table2}' info if {col1_phrase} matches and {condition1} applies.",
                    "For each '{table1}' row, include '{table2}' data if {col1_phrase} matches and {condition1} is satisfied."
                ],
                3: [
                    "Show all '{table1}' rows with any matching '{table2}' data, but only if they meet {condition1} and {condition2}.",
                    "List every '{table1}' record, including '{table2}' info if {col1_phrase} matches and both {condition1} and {condition2} are true.",
                    "Display all '{table1}' entries, attaching '{table2}' data where {col1_phrase} matches and both filters apply.",
                    "For each '{table1}' row, add '{table2}' info if {col1_phrase} matches and both {condition1} and {condition2} are met."
                ]
            },
            "right_outer": {
                1: [
                    "Show all records from '{table2}', and add matching data from '{table1}' where {col1_phrase} is the same. If there is no match, keep the '{table2}' data.",
                    "List every row from '{table2}' and fill in data from '{table1}' where {col1_phrase} matches. If not, leave those fields empty.",
                    "Display all entries from '{table2}', adding info from '{table1}' when {col1_phrase} matches.",
                    "For each row in '{table2}', attach matching '{table1}' data on {col1_phrase}, or leave blank if no match."
                ],
                2: [
                    "Show all rows from '{table2}' and matching ones from '{table1}' where {col1_phrase} matches and also meets {condition1}.",
                    "List every '{table2}' record, adding '{table1}' data if {col1_phrase} matches and {condition1} is true.",
                    "Display all '{table2}' rows, with '{table1}' info if {col1_phrase} matches and {condition1} applies.",
                    "For each '{table2}' row, include '{table1}' data if {col1_phrase} matches and {condition1} is satisfied."
                ],
                3: [
                    "Show all '{table2}' rows with any matching '{table1}' data, but only if they meet {condition1} and {condition2}.",
                    "List every '{table2}' record, including '{table1}' info if {col1_phrase} matches and both {condition1} and {condition2} are true.",
                    "Display all '{table2}' entries, attaching '{table1}' data where {col1_phrase} matches and both filters apply.",
                    "For each '{table2}' row, add '{table1}' info if {col1_phrase} matches and both {condition1} and {condition2} are met."
                ]
            },
            "full_outer": {
                1: [
                    "Show all records from both '{table1}' and '{table2}', matching them where {col1_phrase} is the same. If there is no match, keep the data from both tables.",
                    "List every row from '{table1}' and '{table2}', combining them where {col1_phrase} matches, and keeping all other rows as well.",
                    "Display all data from both '{table1}' and '{table2}', joining where {col1_phrase} matches and keeping unmatched rows too.",
                    "Combine '{table1}' and '{table2}' so that all rows from both tables appear, matching on {col1_phrase} where possible."
                ],
                2: [
                    "Show all rows from both tables, matching on {col1_phrase} and also meeting {condition1}.",
                    "List every record from '{table1}' and '{table2}', combining them where {col1_phrase} matches and {condition1} is true.",
                    "Display all rows from both tables, joining on {col1_phrase} and applying filter {condition1}.",
                    "Combine '{table1}' and '{table2}' with a full outer join on {col1_phrase}, keeping all rows and filtering by {condition1}."
                ],
                3: [
                    "Show all records from both tables, matching on {col1_phrase} and only if {condition1} and {condition2} are true.",
                    "List every row from '{table1}' and '{table2}', combining them where {col1_phrase} matches and both {condition1} and {condition2} are true.",
                    "Display all data from both tables, joining on {col1_phrase} and applying both filters.",
                    "Combine '{table1}' and '{table2}' with a full outer join on {col1_phrase}, keeping all rows and filtering by both {condition1} and {condition2}."
                ]
            },
            "equijoin": {
                1: [
                    "Combine '{table1}' and '{table2}' where {col1_phrase} in both tables has the same value.",
                    "Show all records where '{table1}' and '{table2}' have equal values in {col1_phrase}.",
                    "Join '{table1}' and '{table2}' by matching rows where {col1_phrase} is the same.",
                    "Display only the rows from '{table1}' and '{table2}' where {col1_phrase} matches exactly."
                ],
                2: [
                    "Find all rows where '{table1}' and '{table2}' have the same value in {col1_phrase}, and only include those matches.",
                    "Combine '{table1}' and '{table2}' by matching {col1_phrase} values, and show only the matching records.",
                    "Show the data from '{table1}' and '{table2}' where {col1_phrase} is equal, and apply the filter {condition1}.",
                    "List the results of joining '{table1}' and '{table2}' on {col1_phrase} and filter by {condition1}."
                ],
                3: [
                    "Show the results of joining '{table1}' and '{table2}' where {col1_phrase} matches and also meets the condition: {condition1}.",
                    "List records from '{table1}' and '{table2}' where {col1_phrase} matches and also satisfy {condition1} and {condition2}.",
                    "Combine '{table1}' and '{table2}' on {col1_phrase}, but only include rows that meet both {condition1} and {condition2}.",
                    "Display joined data from '{table1}' and '{table2}' where {col1_phrase} matches and extra filters apply."
                ]
            },
            "natural": {
                1: [
                    "Combine '{table1}' and '{table2}' by matching all columns with the same name.",
                    "Show all records where '{table1}' and '{table2}' have the same values in columns with matching names.",
                    "Join '{table1}' and '{table2}' using all shared column names as the join condition.",
                    "Display combined data from '{table1}' and '{table2}' where columns with the same name match."
                ],
                2: [
                    "Show all data from '{table1}' and '{table2}' where columns with the same name match.",
                    "Combine '{table1}' and '{table2}' using all shared column names as the join condition.",
                    "Display all rows from '{table1}' and '{table2}' where columns with matching names have the same value.",
                    "Join '{table1}' and '{table2}' naturally, matching on all columns with the same name."
                ],
                3: [
                    "Combine '{table1}' and '{table2}' by matching all columns with the same name, but only if {condition1} is also true.",
                    "Show all records from '{table1}' and '{table2}' where columns match by name and {condition1} is satisfied.",
                    "Join '{table1}' and '{table2}' naturally, but only include rows where {condition1} applies.",
                    "Display combined data from '{table1}' and '{table2}' where columns match by name and filter by {condition1}."
                ]
            },
            "self": {
                1: [
                    "Combine '{table1}' with itself, matching rows where {col1_phrase} equals {col2_phrase}.",
                    "Show pairs of rows from '{table1}' where {col1_phrase} is the same in both.",
                    "Join '{table1}' to itself to find rows with the same value in {col1_phrase}.",
                    "Display all pairs of '{table1}' rows where {col1_phrase} matches."
                ],
                2: [
                    "Combine '{table1}' with itself where {col1_phrase} equals {col2_phrase} and also meets {condition1}.",
                    "Show pairs from '{table1}' where {col1_phrase} matches and {condition1} is true.",
                    "Join '{table1}' to itself on {col1_phrase}, but only include pairs where {condition1} applies.",
                    "Display all pairs of '{table1}' rows where {col1_phrase} matches and {condition1} is satisfied."
                ],
                3: [
                    "Combine '{table1}' with itself where {col1_phrase} equals {col2_phrase} and both {condition1} and {condition2} are true.",
                    "Show pairs from '{table1}' where {col1_phrase} matches and both {condition1} and {condition2} are satisfied.",
                    "Join '{table1}' to itself on {col1_phrase}, but only include pairs where both {condition1} and {condition2} apply.",
                    "Display all pairs of '{table1}' rows where {col1_phrase} matches and both filters are met."
                ]
            }
        }

        level_num = {"level1": 1, "level2": 2, "level3": 3}.get(level.lower(), 1)
        valid_questions = []

        for table1_name, foreign_keys in self.foreign_keys.items():
            for fk_column, ref in foreign_keys:
                ref_table_name, ref_column = ref.split('.')
                sample_values = self._get_random_sample(ref_table_name, ref_column, num_values=2)
                condition1, condition2 = self._generate_conditions(fk_column, sample_values)
                col1_phrase = self._col_phrase(fk_column)
                col2_phrase = self._col_phrase(ref_column)

                if join_type not in templates or level_num not in templates[join_type]:
                    continue

                template = random.choice(templates[join_type][level_num])
                question = template.format(
                    table1=table1_name,
                    table2=ref_table_name,
                    col1=fk_column,
                    col2=ref_column,
                    col1_phrase=col1_phrase,
                    col2_phrase=col2_phrase,
                    condition1=condition1,
                    condition2=condition2
                )

                # Construct query based on join type
                if join_type == "inner" or join_type == "equijoin":
                    query = (
                        f"({table1_name} ⨝ {fk_column} = {ref_table_name}.{fk_column})"
                        if level_num in [1, 2] else
                        f"σ({condition1} AND {condition2})({table1_name} ⨝ {fk_column} = {ref_table_name}.{fk_column})"
                    )
                elif join_type == "left_outer":
                    symbol = "⟕"
                    query = (
                        f"({table1_name} {symbol} {fk_column} = {ref_table_name}.{fk_column})"
                        if level_num == 1 else
                        f"σ({condition1})({table1_name} {symbol} {fk_column} = {ref_table_name}.{fk_column})"
                        if level_num == 2 else
                        f"σ({condition1} AND {condition2})({table1_name} {symbol} {fk_column} = {ref_table_name}.{fk_column})"
                    )
                elif join_type == "right_outer":
                    symbol = "⟖"
                    query = (
                        f"({table1_name} {symbol} {fk_column} = {ref_table_name}.{fk_column})"
                        if level_num == 1 else
                        f"σ({condition1})({table1_name} {symbol} {fk_column} = {ref_table_name}.{fk_column})"
                        if level_num == 2 else
                        f"σ({condition1} AND {condition2})({table1_name} {symbol} {fk_column} = {ref_table_name}.{fk_column})"
                    )
                elif join_type == "full_outer":
                    symbol = "⟗"
                    query = (
                        f"({table1_name} {symbol} {fk_column} = {ref_table_name}.{fk_column})"
                        if level_num == 1 else
                        f"σ({condition1})({table1_name} {symbol} {fk_column} = {ref_table_name}.{fk_column})"
                        if level_num == 2 else
                        f"σ({condition1} AND {condition2})({table1_name} {symbol} {fk_column} = {ref_table_name}.{fk_column})"
                    )
                elif join_type == "natural":
                    query = (
                        f"({table1_name} ⨝ {ref_table_name})"
                        if level_num in [1, 2] else
                        f"σ({condition1})({table1_name} ⨝ {ref_table_name})"
                    )
                elif join_type == "self":
                    query = (
                        f"({table1_name} ⨝ {fk_column} = {fk_column})"
                        if level_num == 1 else
                        f"σ({condition1})({table1_name} ⨝ {fk_column} = {fk_column})"
                        if level_num == 2 else
                        f"σ({condition1} AND {condition2})({table1_name} ⨝ {fk_column} = {fk_column})"
                    )
                else:
                    continue

                valid_questions.append({
                    "question": question,
                    "answer": query
                })

        return random.choice(valid_questions) if valid_questions else None

    def generate_mcq(self, join_type="inner", level="level1"):
        join_symbols = {
            "inner": "⨝",
            "left_outer": "⟕",
            "right_outer": "⟖",
            "full_outer": "⟗",
            "natural": "⨝",
            "equijoin": "⨝",
            "self": "⨝"
        }

        if join_type not in join_symbols or not self.foreign_keys:
            return None

        fk_pairs = []
        for table1, keys in self.foreign_keys.items():
            for fk_column, ref in keys:
                ref_table = ref.split('.')[0]
                fk_pairs.append((table1, ref_table, fk_column))

        if not fk_pairs:
            return None

        if join_type == "self":
            table1, table2, fk_column = random.choice(fk_pairs)
            table2 = table1  # self join
        else:
            table1, table2, fk_column = random.choice(fk_pairs)

        condition = f"{table1}.{fk_column} = {table2}.{fk_column}"
        symbol = join_symbols[join_type]

        # Templates by level for MCQ
        templates = {
            "level1": {  # Easy - basic understanding
                "inner": [
                    f"What relational algebra query retrieves matching rows from '{table1}' and '{table2}' using INNER JOIN?",
                    f"Select the expression showing intersecting rows between '{table1}' and '{table2}' on {fk_column}."
                ],
                "left_outer": [
                    f"Which query retrieves all rows from '{table1}' and matching ones from '{table2}', filling NULLs if no match?",
                    f"Choose the correct LEFT OUTER JOIN query for '{table1}' and '{table2}'."
                ],
                "right_outer": [
                    f"Which query keeps all rows from '{table2}' and matches from '{table1}', inserting NULLs if needed?",
                    f"Select the RIGHT OUTER JOIN expression on '{table1}' and '{table2}'."
                ],
                "full_outer": [
                    f"Which join returns all rows from both '{table1}' and '{table2}', matched or not?",
                    f"Choose the FULL OUTER JOIN query between '{table1}' and '{table2}'."
                ],
                "natural": [
                    f"Which query performs a NATURAL JOIN on '{table1}' and '{table2}' using common attributes?",
                    f"Select the NATURAL JOIN expression for '{table1}' and '{table2}'."
                ],
                "equijoin": [
                    f"Which query joins '{table1}' and '{table2}' using equality on {fk_column}?",
                    f"Choose the EQUIJOIN relational algebra query between '{table1}' and '{table2}'."
                ],
                "self": [
                    f"Which query performs a self-join on '{table1}' using {fk_column}?",
                    f"Select the relational algebra expression for self-join on '{table1}'."
                ],
            },
            "level2": {  # Medium - more precise language, slightly more complex
                "inner": [
                    f"In relational algebra, which query retrieves only rows with matching values from '{table1}' and '{table2}' on {fk_column} using INNER JOIN?",
                    f"Identify the correct INNER JOIN expression filtering rows on equality condition {condition}."
                ],
                "left_outer": [
                    f"Choose the query that returns all rows from '{table1}' along with matched rows from '{table2}', placing NULLs where no match is found.",
                    f"Which relational algebra operation corresponds to LEFT OUTER JOIN on '{table1}' and '{table2}' with condition {condition}?"
                ],
                "right_outer": [
                    f"Identify the expression that returns all rows from '{table2}' and matching rows from '{table1}', with NULLs for unmatched rows.",
                    f"Which relational algebra operation represents RIGHT OUTER JOIN between '{table1}' and '{table2}' on {fk_column}?"
                ],
                "full_outer": [
                    f"Select the relational algebra expression representing FULL OUTER JOIN between '{table1}' and '{table2}' with condition {condition}.",
                    f"Which join operation keeps all tuples from both relations, matched or not?"
                ],
                "natural": [
                    f"Which query automatically joins '{table1}' and '{table2}' on all common attribute names without specifying join conditions?",
                    f"Select the correct NATURAL JOIN expression for '{table1}' and '{table2}'."
                ],
                "equijoin": [
                    f"Choose the relational algebra query for EQUIJOIN between '{table1}' and '{table2}' using equality on {fk_column}.",
                    f"Which expression represents an equijoin predicate {condition} between '{table1}' and '{table2}'?"
                ],
                "self": [
                    f"Which query correctly represents a self-join on '{table1}' with the equality condition {condition}?",
                    f"Identify the relational algebra expression for self join on '{table1}' using {fk_column}."
                ],
            },
            "level3": {  # Hard - more technical, with join condition and symbols
                "inner": [
                    f"Given relations '{table1}' and '{table2}', which relational algebra query with condition {condition} represents an INNER JOIN?",
                    f"Select the expression that uses the symbol '{symbol}' for INNER JOIN on attribute {fk_column}."
                ],
                "left_outer": [
                    f"Identify the relational algebra expression using '{symbol}' that returns all tuples from '{table1}' with matching '{table2}' tuples or NULLs.",
                    f"Which query correctly uses the LEFT OUTER JOIN operator '{symbol}' between '{table1}' and '{table2}' on {fk_column}?"
                ],
                "right_outer": [
                    f"Select the relational algebra operation using '{symbol}' representing RIGHT OUTER JOIN on '{table1}' and '{table2}'.",
                    f"Choose the query keeping all rows from '{table2}' while matching '{table1}', using the symbol '{symbol}'."
                ],
                "full_outer": [
                    f"Which relational algebra expression using '{symbol}' keeps unmatched rows from both '{table1}' and '{table2}'?",
                    f"Select the FULL OUTER JOIN query on '{table1}' and '{table2}' represented by '{symbol}'."
                ],
                "natural": [
                    f"Choose the expression representing NATURAL JOIN '{table1} ⨝ {table2}' which joins on all common attributes implicitly.",
                    f"Identify the natural join query that merges tuples from '{table1}' and '{table2}' where attribute names match."
                ],
                "equijoin": [
                    f"Select the relational algebra query with explicit join condition {condition} representing an EQUIJOIN.",
                    f"Which query uses '{symbol}' and σ to perform an equijoin on '{table1}' and '{table2}'?"
                ],
                "self": [
                    f"Identify the self-join relational algebra query using '{symbol}' with condition {condition} on '{table1}'.",
                    f"Which expression correctly represents a self join on '{table1}' using equality on {fk_column}?"
                ],
            }
        }

        # Correct answer construction (same as before)
        if join_type == "natural":
            correct = f"{table1} ⨝ {table2}"
        elif join_type == "self":
            correct = f"{table1} {symbol} {condition}"
        else:
            correct = f"{table1} {symbol} {condition}"

        wrong1 = f"{table2} {symbol} {condition}"
        wrong2 = f"σ({condition})({table1})"
        wrong3 = f"π({fk_column})({table2})"

        options = [correct, wrong1, wrong2, wrong3]
        random.shuffle(options)
        answer = chr(options.index(correct) + ord('a'))

        # Pick a random template based on level and join_type
        selected_template = random.choice(templates[level][join_type])

        return {
            "type": "MCQ",
            "join_type": join_type.upper(),
            "level": level.upper(),
            "question": selected_template,
            "options": {chr(i + 97): opt for i, opt in enumerate(options)},
            "answer": f"({answer})"
        }


    def generate_tfq(self, join_type="inner", level="level1"):
        join_symbols = {
            "inner": "⨝",
            "left_outer": "⟕",
            "right_outer": "⟖",
            "full_outer": "⟗",
            "natural": "⨝",
            "equijoin": "⨝",
            "self": "⨝"
        }

        if join_type not in join_symbols or not self.foreign_keys:
            return None

        fk_pairs = []
        for table1, keys in self.foreign_keys.items():
            for fk_column, ref in keys:
                ref_table = ref.split('.')[0]
                fk_pairs.append((table1, ref_table, fk_column))

        if not fk_pairs:
            return None

        table1, table2, fk_column = random.choice(fk_pairs)
        if join_type == "self":
            table2 = table1

        condition = f"{table1}.{fk_column} = {table2}.{fk_column}"
        symbol = join_symbols[join_type]

        # Define templates for each difficulty level
        true_templates = {
            "level1": {
                "inner": [
                    f"The inner join retrieves rows from '{table1}' and '{table2}' where {condition}.",
                    f"{table1} {symbol} {condition} gives only matching rows from both tables.",
                    f"An INNER JOIN combines records from '{table1}' and '{table2}' where values match on {fk_column}."
                ],
                "left_outer": [
                    f"{table1} ⟕ {table2} returns all rows from '{table1}' and matching ones from '{table2}'.",
                    f"In a LEFT OUTER JOIN, unmatched rows from '{table1}' are preserved with NULLs for '{table2}'.",
                    f"{table1} ⟕ {table2} includes unmatched rows from '{table1}'."
                ],
                "right_outer": [
                    f"{table1} ⟖ {table2} includes all rows from '{table2}' and matched ones from '{table1}'.",
                    f"RIGHT OUTER JOIN preserves unmatched rows from '{table2}' and fills NULLs for '{table1}'.",
                    f"{table1} ⟖ {table2} is used to keep all entries from '{table2}'."
                ],
                "full_outer": [
                    f"FULL OUTER JOIN includes unmatched rows from both '{table1}' and '{table2}'.",
                    f"{table1} ⟗ {table2} gives a complete join keeping all rows from both tables.",
                    f"In FULL OUTER JOIN, NULLs fill missing matches from both sides."
                ],
                "natural": [
                    f"{table1} ⨝ {table2} represents a NATURAL JOIN using common attributes.",
                    f"A NATURAL JOIN automatically joins on all common attribute names.",
                    f"{table1} ⨝ {table2} will use implicit equality on shared column names."
                ],
                "equijoin": [
                    f"{table1} ⨝ {condition} is an example of an EQUIJOIN using equality.",
                    f"An EQUIJOIN explicitly defines the join condition like {condition}.",
                    f"Equijoins combine tables using an explicit = condition."
                ],
                "self": [
                    f"A self join involves joining '{table1}' with itself using {condition}.",
                    f"{table1} ⨝ {condition} performs a self join to compare rows within the same table.",
                    f"Self joins use aliases or conditions to join a table with itself."
                ]
            },
            "level2": {
                "inner": [
                    f"INNER JOIN between '{table1}' and '{table2}' returns rows only where {condition} holds.",
                    f"Using {table1} ⨝ {table2}, only matching rows on {fk_column} are included.",
                    f"The join condition {condition} ensures rows from both tables match exactly in INNER JOIN."
                ],
                "left_outer": [
                    f"LEFT OUTER JOIN keeps all rows from '{table1}' and adds NULLs for non-matching '{table2}' rows.",
                    f"In {table1} ⟕ {table2}, unmatched '{table1}' rows appear with NULLs for '{table2}'.",
                    f"LEFT OUTER JOIN guarantees preservation of all '{table1}' rows regardless of matches."
                ],
                "right_outer": [
                    f"RIGHT OUTER JOIN preserves every row of '{table2}' and matches from '{table1}'.",
                    f"{table1} ⟖ {table2} includes unmatched '{table2}' rows with NULLs in '{table1}'.",
                    f"RIGHT OUTER JOIN ensures full '{table2}' row inclusion regardless of match."
                ],
                "full_outer": [
                    f"FULL OUTER JOIN retains all rows from '{table1}' and '{table2}', filling NULLs when unmatched.",
                    f"In {table1} ⟗ {table2}, unmatched rows from both sides appear with NULL placeholders.",
                    f"FULL OUTER JOIN provides a comprehensive union of both relations with NULL padding."
                ],
                "natural": [
                    f"NATURAL JOIN between '{table1}' and '{table2}' matches all attributes with identical names.",
                    f"{table1} ⨝ {table2} automatically matches columns with the same name without explicit condition.",
                    f"Natural join uses implicit equality on all common attributes between '{table1}' and '{table2}'."
                ],
                "equijoin": [
                    f"EQUIJOIN specifies equality condition {condition} explicitly between two relations.",
                    f"{table1} ⨝ {table2} with condition {condition} is a classic equijoin example.",
                    f"Equijoins join tables based strictly on an equality predicate, such as {condition}."
                ],
                "self": [
                    f"Self join matches rows within '{table1}' on condition {condition} using table aliases.",
                    f"A self join duplicates the table and joins on {fk_column} equality.",
                    f"Self join is used to compare rows in '{table1}' meeting {condition}."
                ]
            },
            "level3": {
                "inner": [
                    f"An INNER JOIN operation between '{table1}' and '{table2}' uses predicate {condition} to combine only matching tuples, excluding non-matching ones.",
                    f"Using relational algebra symbol {symbol} and condition {condition}, INNER JOIN produces the intersection of matching tuples between '{table1}' and '{table2}'.",
                    f"INNER JOIN filters the Cartesian product of '{table1}' and '{table2}' using condition {condition} to return matching pairs."
                ],
                "left_outer": [
                    f"LEFT OUTER JOIN {table1} {symbol} {table2} retains all tuples from '{table1}', padding unmatched tuples from '{table2}' with NULLs according to condition {condition}.",
                    f"The LEFT OUTER JOIN extends INNER JOIN by including unmatched rows from the left relation '{table1}' filled with NULLs for '{table2}'.",
                    f"In relational algebra, LEFT OUTER JOIN returns all '{table1}' tuples and matches from '{table2}', with NULLs for unmatched '{table2}' rows per {condition}."
                ],
                "right_outer": [
                    f"RIGHT OUTER JOIN includes all tuples from the right relation '{table2}' and matches from '{table1}', padding unmatched '{table1}' tuples with NULLs using condition {condition}.",
                    f"In {table1} {symbol} {table2}, the RIGHT OUTER JOIN returns every '{table2}' tuple alongside matching '{table1}' tuples.",
                    f"RIGHT OUTER JOIN extends the inner join by including all right relation tuples and NULLs for unmatched left relation tuples."
                ],
                "full_outer": [
                    f"FULL OUTER JOIN combines all tuples from '{table1}' and '{table2}', filling NULLs for unmatched tuples on either side based on {condition}.",
                    f"{table1} {symbol} {table2} in FULL OUTER JOIN returns a union of both relations including all unmatched rows padded with NULLs.",
                    f"The FULL OUTER JOIN operation preserves unmatched rows from both '{table1}' and '{table2}' and joins on condition {condition}."
                ],
                "natural": [
                    f"NATURAL JOIN eliminates duplicate columns by joining '{table1}' and '{table2}' on all common attributes implicitly.",
                    f"In relational algebra, NATURAL JOIN {table1} ⨝ {table2} merges relations based on all shared attribute names without explicit predicates.",
                    f"Natural join automatically creates equality conditions on all attributes with the same names between '{table1}' and '{table2}'."
                ],
                "equijoin": [
                    f"EQUIJOIN explicitly specifies an equality predicate {condition} and returns combined tuples satisfying this condition between '{table1}' and '{table2}'.",
                    f"Relational algebra equijoin {table1} ⨝_{{{condition}}} {table2} filters the Cartesian product of '{table1}' and '{table2}' on {condition}.",
                    f"EQUIJOIN is a form of theta join where the predicate is equality on attributes, such as {condition}."
                ],
                "self": [
                    f"Self join {table1} ⨝_{{{condition}}} {table1} creates pairs of rows from the same table '{table1}' that satisfy the condition {condition}.",
                    f"In relational algebra, self join involves joining a relation with itself using a condition like {condition} to compare tuples.",
                    f"Self join typically requires renaming attributes or aliases to distinguish between two copies of '{table1}' before joining."
                ]
            }
        }

        false_templates = {
            "level1": {
                "inner": [
                    f"An inner join keeps all rows from both '{table1}' and '{table2}' regardless of match.",
                    f"INNER JOIN inserts NULLs for unmatched rows from '{table1}'.",
                    f"{table1} ⨝ {condition} will include unmatched data from '{table2}'."
                ],
                "left_outer": [
                    f"LEFT OUTER JOIN only returns rows where {condition} holds true.",
                    f"{table1} ⟕ {table2} excludes rows from '{table1}' that have no match in '{table2}'.",
                    f"All unmatched rows from '{table2}' are preserved in a LEFT OUTER JOIN."
                ],
                "right_outer": [
                    f"RIGHT OUTER JOIN includes only matched rows from '{table2}'.",
                    f"In a RIGHT OUTER JOIN, unmatched rows from '{table1}' are preserved.",
                    f"{table1} ⟖ {table2} drops unmatched rows from '{table2}'."
                ],
                "full_outer": [
                    f"A FULL OUTER JOIN is identical to an INNER JOIN.",
                    f"{table1} ⟗ {table2} removes all unmatched rows.",
                    f"FULL OUTER JOIN cannot represent NULLs."
                ],
                "natural": [
                    f"A NATURAL JOIN allows custom join conditions using != operators.",
                    f"{table1} ⨝ {table2} always requires manually specifying join conditions.",
                    f"NATURAL JOIN ignores common column names while joining."
                ],
                "equijoin": [
                    f"Equijoins automatically use all common columns like NATURAL JOINs.",
                    f"{table1} ⨝ {condition} includes NULLs for unmatched values.",
                    f"EQUIJOIN does not allow specifying the join condition."
                ],
                "self": [
                    f"A self join combines '{table1}' with a completely different table.",
                    f"Self joins require distinct tables like '{table1}' and '{table2}'.",
                    f"{table1} ⨝ {condition} is a CROSS JOIN, not a self join."
                ]
            },
            "level2": {
                "inner": [
                    f"INNER JOIN returns unmatched rows padded with NULLs from both relations.",
                    f"All rows from '{table1}' and '{table2}' are included in INNER JOIN regardless of condition {condition}.",
                    f"INNER JOIN is identical to CROSS JOIN without any filtering."
                ],
                "left_outer": [
                    f"LEFT OUTER JOIN drops unmatched rows from '{table1}'.",
                    f"{table1} ⟕ {table2} excludes NULL values for unmatched rows.",
                    f"LEFT OUTER JOIN only returns rows matching the join condition."
                ],
                "right_outer": [
                    f"RIGHT OUTER JOIN excludes unmatched rows from '{table2}'.",
                    f"RIGHT OUTER JOIN removes NULLs from unmatched tuples.",
                    f"{table1} ⟖ {table2} returns only matched rows."
                ],
                "full_outer": [
                    f"FULL OUTER JOIN excludes unmatched rows from both tables.",
                    f"FULL OUTER JOIN is the same as INNER JOIN.",
                    f"NULL values are not used in FULL OUTER JOIN."
                ],
                "natural": [
                    f"NATURAL JOIN requires explicit join condition with != operator.",
                    f"NATURAL JOIN ignores common attribute names.",
                    f"{table1} ⨝ {table2} cannot be used without specifying conditions."
                ],
                "equijoin": [
                    f"EQUIJOIN does not use equality conditions.",
                    f"Equijoins include unmatched rows padded with NULLs.",
                    f"EQUIJOIN is a type of CROSS JOIN without filtering."
                ],
                "self": [
                    f"Self joins require joining two different tables.",
                    f"Self join is the same as CROSS JOIN between two tables.",
                    f"Self join does not use equality conditions."
                ]
            },
            "level3": {
                "inner": [
                    f"INNER JOIN includes all possible tuple pairs from '{table1}' and '{table2}' regardless of join condition.",
                    f"Using {symbol}, INNER JOIN returns unmatched tuples padded with NULLs.",
                    f"INNER JOIN returns the full Cartesian product of the two relations."
                ],
                "left_outer": [
                    f"LEFT OUTER JOIN removes unmatched tuples from the left relation.",
                    f"LEFT OUTER JOIN pads unmatched tuples from the right relation with actual values, not NULLs.",
                    f"LEFT OUTER JOIN only includes matched tuples."
                ],
                "right_outer": [
                    f"RIGHT OUTER JOIN excludes unmatched tuples from the right relation.",
                    f"RIGHT OUTER JOIN pads unmatched tuples from the left relation with actual values, not NULLs.",
                    f"RIGHT OUTER JOIN behaves like INNER JOIN."
                ],
                "full_outer": [
                    f"FULL OUTER JOIN excludes tuples without matches from either relation.",
                    f"FULL OUTER JOIN is equivalent to INNER JOIN.",
                    f"FULL OUTER JOIN never produces NULLs."
                ],
                "natural": [
                    f"NATURAL JOIN duplicates common columns instead of merging them.",
                    f"NATURAL JOIN requires explicit predicates for each common attribute.",
                    f"NATURAL JOIN cannot be used without explicit renaming."
                ],
                "equijoin": [
                    f"EQUIJOIN cannot be defined by an equality predicate.",
                    f"EQUIJOIN includes tuples that don't satisfy the equality condition.",
                    f"EQUIJOIN behaves like FULL OUTER JOIN."
                ],
                "self": [
                    f"Self join cannot be performed in relational algebra.",
                    f"Self join always returns the Cartesian product of the table with itself.",
                    f"Self join does not require aliasing in relational algebra."
                ]
            }
        }

        true_statements = true_templates.get(level, {}).get(join_type, [])
        false_statements = false_templates.get(level, {}).get(join_type, [])

        if not true_statements or not false_statements:
            return None

        is_true = random.choice([True, False])
        if is_true:
            question = random.choice(true_statements)
            answer = "(a) True"
        else:
            question = random.choice(false_statements)
            answer = "(b) False"

        return {
            "type": "TFQ",
            "join_type": join_type.upper(),
            "level": level.upper(),
            "question": question,
            "options": {
                "a": "True",
                "b": "False"
            },
            "answer": answer
        }

    def generate_diq(self, join_type="inner", level="level1"):
        join_symbols = {
            "inner": "⨝",
            "left_outer": "⟕",
            "right_outer": "⟖",
            "full_outer": "⟗",
            "natural": "⨝",
            "equijoin": "⨝",
            "self": "⨝"
        }

        level = level.lower()
        join_type = join_type.lower()
        if join_type not in join_symbols or not self.foreign_keys:
            return None

        fk_pairs = []
        for table1, keys in self.foreign_keys.items():
            for fk_column, ref in keys:
                ref_table = ref.split('.')[0]
                fk_pairs.append((table1, ref_table, fk_column))

        if not fk_pairs:
            return None

        table1, table2, fk_column = random.choice(fk_pairs)
        if join_type == "self":
            table2 = table1

        condition = f"{table1}.{fk_column} = {table2}.{fk_column}"
        symbol = join_symbols[join_type]

        # Relational Algebra expression
        if join_type == "equijoin":
            ra_expression = f"{table1} ⨝ ({condition}) {table2}"
        elif join_type == "self":
            ra_expression = f"{table1} ⨝ {table1}"
        elif join_type == "natural":
            ra_expression = f"{table1} ⨝ {table2}"
        else:
            ra_expression = f"{table1} {symbol} {table2}"

        # Explanation for each join type
        explanation_map = {
            "inner": (
                "Returns only the rows from both tables where the join condition holds true. "
                "Rows without a match in either table are excluded."
            ),
            "left_outer": (
                f"Returns all rows from the left table ('{table1}'), and matched rows from the right table ('{table2}'). "
                f"Unmatched rows from the left table appear with NULLs for right table attributes."
            ),
            "right_outer": (
                f"Returns all rows from the right table ('{table2}'), and matched rows from the left table ('{table1}'). "
                f"Unmatched rows from the right table appear with NULLs for left table attributes."
            ),
            "full_outer": (
                "Returns all rows from both tables. "
                "Rows with no matching pair in the opposite table are filled with NULLs."
            ),
            "natural": (
                f"Performs a join based on all columns with the same name between '{table1}' and '{table2}', "
                "eliminating duplicates for the matched columns."
            ),
            "equijoin": (
                f"Combines rows from '{table1}' and '{table2}' where the values of {fk_column} are equal. "
                "Requires an explicit equality condition."
            ),
            "self": (
                f"Joins '{table1}' with itself, comparing rows within the same table. "
                "Useful for hierarchical or comparative relationships."
            )
        }

        explanation = explanation_map.get(join_type, "No explanation available.")

        # Final answer guide
        answer_guide = (
            f"Relational Algebra Expression:\n  {ra_expression}\n"
            f"Join Condition:\n  {condition if join_type not in ['natural', 'self'] else 'Implicit (natural/self join)'}\n\n"
            f"Explanation:\n{explanation}"
        )

        # DIQ-style question prompt
        question = (
            f"Given the relational algebra expression `{ra_expression}`, describe and interpret what this operation does. "
            f"What type of join is being performed and how does it affect the result set?"
        )

        return {
            "type": "DIQ",
            "join_type": join_type.upper(),
            "level": level.upper(),
            "question": question,
            "expression": ra_expression,
            "join_condition": condition,
            "answer_guide": answer_guide,
            "answer": answer_guide,
            "tree": f"{symbol}|{table1}|{table2}",  # For line-by-line or mermaid parsing
            "table1": table1,
            "table2": table2,
            "symbol": symbol
        }


    def generate_mtq(self, join_type="inner", level="level1"):
        join_symbols = {
            "inner": "⨝",
            "left_outer": "⟕",
            "right_outer": "⟖",
            "full_outer": "⟗",
            "natural": "⨝",
            "equijoin": "⨝",
            "self": "⨝"
        }

        level = level.lower()
        if join_type not in join_symbols or not self.foreign_keys:
            return None

        fk_pairs = []
        for table1, keys in self.foreign_keys.items():
            for fk_column, ref in keys:
                ref_table = ref.split('.')[0]
                fk_pairs.append((table1, ref_table, fk_column))

        if not fk_pairs:
            return None

        table1, table2, fk_column = random.choice(fk_pairs)
        if join_type == "self":
            table2 = table1

        condition = f"{table1}.{fk_column} = {table2}.{fk_column}"
        symbol = join_symbols[join_type]

        ra_expression = ""
        if join_type == "equijoin":
            ra_expression = f"{table1} ⨝ ({condition}) {table2}"
        elif join_type == "self":
            ra_expression = f"{table1} ⨝ {table1}"
        else:
            ra_expression = f"{table1} {symbol} {table2}"

        # Define match pairs by level
        match_sets = {
            "level1": {
                "prompt": f"Match the join types with their correct meaning for tables '{table1}' and '{table2}':",
                "pairs": {
                    "INNER JOIN": "Returns rows with matching keys in both tables",
                    "LEFT OUTER JOIN": "Returns all rows from left table and matching rows from right table",
                    "RIGHT OUTER JOIN": "Returns all rows from right table and matching rows from left table",
                    "FULL OUTER JOIN": "Returns all rows when there is a match in one of the tables"
                }
            },
            "level2": {
                "prompt": f"Match join types to relational algebra symbols for joining '{table1}' and '{table2}':",
                "pairs": {
                    "INNER JOIN": "⨝",
                    "LEFT OUTER JOIN": "⟕",
                    "RIGHT OUTER JOIN": "⟖",
                    "FULL OUTER JOIN": "⟗"
                }
            },
            "level3": {
                "prompt": f"Match join types with correct relational algebra expressions for '{table1}' and '{table2}' using key '{fk_column}':",
                "pairs": {
                    "INNER JOIN": f"{table1} ⨝ {table2}",
                    "EQUIJOIN": f"{table1} ⨝ ({condition}) {table2}",
                    "SELF JOIN": f"{table1} ⨝ {table1}",
                    "NATURAL JOIN": f"{table1} ⨝ {table2}"
                }
            }
        }

        match_info = match_sets.get(level)
        if not match_info:
            return None

        left_items = list(match_info["pairs"].keys())
        right_items = list(match_info["pairs"].values())
        random.shuffle(left_items)
        random.shuffle(right_items)

        # For display compatibility, also provide pairs and answer_pairs
        pairs = list(zip(left_items, right_items))
        answer_pairs = list(match_info["pairs"].items())

        return {
            "type": "MTQ",
            "join_type": join_type.upper(),
            "level": level.upper(),
            "question": match_info["prompt"],
            "left_items": left_items,
            "right_items": right_items,
            "answer_key": match_info["pairs"],
            "pairs": pairs,
            "answer_pairs": answer_pairs,
            'answer': {left: right for left, right in answer_pairs}
        }

    def generate_ecq(self, join_type="inner", level="level1"):
        join_symbols = {
            "inner": "⨝",
            "left_outer": "⟕",
            "right_outer": "⟖",
            "full_outer": "⟗",
            "natural": "⨝",
            "equijoin": "⨝",
            "self": "⨝"
        }

        level = level.lower()
        join_type = join_type.lower()
        if join_type not in join_symbols or not self.foreign_keys:
            return None

        fk_pairs = []
        for table1, keys in self.foreign_keys.items():
            for fk_column, ref in keys:
                ref_table = ref.split('.')[0]
                fk_pairs.append((table1, ref_table, fk_column))

        if not fk_pairs:
            return None

        table1, table2, fk_column = random.choice(fk_pairs)
        if join_type == "self":
            table2 = table1

        condition = f"{table1}.{fk_column} = {table2}.{fk_column}"
        symbol = join_symbols[join_type]

        # Build relational algebra expression
        if join_type == "natural":
            expression = f"{table1} ⨝ {table2}"
        elif join_type == "equijoin":
            expression = f"{table1} ⨝ ({condition}) {table2}"
        elif join_type == "self":
            expression = f"{table1} ⨝ {table1}"
        else:
            expression = f"{table1} {symbol} {table2}"

        templates = {
            "level1": [
                f"What does the relational algebra expression `{expression}` represent?",
                f"Explain what operation is being performed in `{expression}`.",
                f"Describe the result of executing `{expression}` in a database system."
            ],
            "level2": [
                f"The expression `{expression}` is used in a query plan. What kind of join is being performed and what rows are expected in the result?",
                f"Given the join condition in `{expression}`, explain how it filters and combines rows.",
                f"What would be the result of executing `{expression}` with partial matches in the referenced column?"
            ],
            "level3": [
                f"Consider `{expression}` as part of a complex query. Describe the intermediate result and how it integrates with other relational operations.",
                f"In `{expression}`, how would changing the join type affect the result set when some rows are unmatched?",
                f"Explain the semantics of `{expression}` in terms of relational set theory and tuple compatibility."
            ]
        }

        question = random.choice(templates[level])
        # Use plain text for explanation for safer display
        explanation_map = {
            "inner": f"This expression performs an inner join, returning only rows where {table1}.{fk_column} matches {table2}.{fk_column}.",
            "left_outer": f"This is a left outer join, returning all rows from {table1} and matched rows from {table2}. Unmatched rows in {table2} result in NULLs.",
            "right_outer": f"This is a right outer join, returning all rows from {table2} and matched rows from {table1}.",
            "full_outer": f"This is a full outer join, including all rows from both {table1} and {table2}, with NULLs where there are no matches.",
            "natural": f"A natural join on {table1} and {table2} joins based on columns with the same name, eliminating duplicate attributes.",
            "equijoin": f"An equijoin joins {table1} and {table2} based on equality of {fk_column}.",
            "self": f"A self join of {table1} combines the table with itself to compare rows within the same relation."
        }

        answer = explanation_map.get(join_type, "No explanation available.")

        return {
            "type": "ECQ",
            "join_type": join_type.upper(),
            "level": level.upper(),
            "question": question,
            "expression": expression,
            "answer": answer
        }


    def generate_oeq(self, join_type="inner", level="level1"):
        # Mapping join types to symbols used in RA
        join_symbols = {
            "inner": "⨝",
            "left_outer": "⟕",
            "right_outer": "⟖",
            "full_outer": "⟗",
            "natural": "⨝",
            "equijoin": "⨝",
            "self": "⨝"
        }

        join_type = join_type.lower()
        level = level.lower()

        # Validate join_type and presence of foreign keys
        if join_type not in join_symbols or not self.foreign_keys:
            return None

        # Collect all foreign key relations (table1, table2, fk_column)
        fk_pairs = []
        for table1, keys in self.foreign_keys.items():
            for fk_column, ref in keys:
                ref_table = ref.split('.')[0]
                fk_pairs.append((table1, ref_table, fk_column))

        if not fk_pairs:
            return None

        # Choose a random FK relation
        table1, table2, fk_column = random.choice(fk_pairs)

        # For self join, table2 = table1
        if join_type == "self":
            table2 = table1

        # Construct join condition
        condition = f"{table1}.{fk_column} = {table2}.{fk_column}"
        symbol = join_symbols[join_type]

        # Construct RA expressions depending on join_type
        if join_type == "natural":
            expression_simple = f"{table1} ⨝ {table2}"
            expression_explicit = expression_simple  # natural join no explicit condition
        elif join_type in ["equijoin", "inner"]:
            expression_simple = f"{table1} ⨝ {table2}"
            expression_explicit = f"{table1} ⨝ ({condition}) {table2}"
        elif join_type == "self":
            expression_simple = f"{table1} ⨝ {table1}"
            expression_explicit = expression_simple
        else:
            # outer joins: left_outer, right_outer, full_outer
            expression_simple = f"{table1} {symbol} {table2}"
            expression_explicit = expression_simple

        # Question templates by join_type and difficulty level
        base_templates = {
            "inner": {
                "level1": [
                    f"Write a relational algebra expression to join '{table1}' and '{table2}' on matching '{fk_column}'.",
                    f"How would you combine rows from '{table1}' and '{table2}' where '{fk_column}' matches?",
                    f"Explain how to retrieve records by joining '{table1}' and '{table2}' using an inner join."
                ],
                "level2": [
                    f"Formulate a relational algebra query performing an inner join between '{table1}' and '{table2}' on '{fk_column}'.",
                    f"Describe the expression to join '{table1}' and '{table2}' filtering only matched tuples based on '{fk_column}'.",
                    f"How do you write an inner join in relational algebra between '{table1}' and '{table2}'?"
                ],
                "level3": [
                    f"Write and explain a relational algebra inner join between '{table1}' and '{table2}' including only matching tuples on '{fk_column}'.",
                    f"How does an inner join between '{table1}' and '{table2}' affect the result when joining on '{fk_column}'?",
                    f"Compose a relational algebra expression for an inner join on '{fk_column}' between '{table1}' and '{table2}'."
                ],
            },
            "left_outer": {
                "level1": [
                    f"Write a relational algebra expression to perform a left outer join of '{table1}' with '{table2}'.",
                    f"How do you include all rows from '{table1}' and matching rows from '{table2}' in a join?",
                    f"Explain a left outer join between '{table1}' and '{table2}'."
                ],
                "level2": [
                    f"Formulate a relational algebra query for a left outer join between '{table1}' and '{table2}'.",
                    f"Describe how to get all rows from '{table1}' with matching rows from '{table2}', including NULLs where no match exists.",
                    f"Write a left outer join relational algebra expression for '{table1}' and '{table2}'."
                ],
                "level3": [
                    f"Explain and write the relational algebra expression for a left outer join on '{table1}' and '{table2}'.",
                    f"How does a left outer join differ from an inner join between '{table1}' and '{table2}'?",
                    f"Compose a complex relational algebra query performing a left outer join between '{table1}' and '{table2}'."
                ],
            },
            "right_outer": {
                "level1": [
                    f"Write a relational algebra expression for a right outer join between '{table1}' and '{table2}'.",
                    f"How do you get all rows from '{table2}' with matching rows from '{table1}'?",
                    f"Explain a right outer join between '{table1}' and '{table2}'."
                ],
                "level2": [
                    f"Formulate a relational algebra query for a right outer join between '{table1}' and '{table2}'.",
                    f"Describe how to get all rows from '{table2}' including matching rows from '{table1}', with NULLs for non-matches.",
                    f"Write the right outer join expression in relational algebra for '{table1}' and '{table2}'."
                ],
                "level3": [
                    f"Explain the effects of a right outer join between '{table1}' and '{table2}', and write its relational algebra expression.",
                    f"How does a right outer join differ from an inner join between '{table1}' and '{table2}'?",
                    f"Compose a detailed relational algebra expression for a right outer join between '{table1}' and '{table2}'."
                ],
            },
            "full_outer": {
                "level1": [
                    f"Write a relational algebra expression for a full outer join between '{table1}' and '{table2}'.",
                    f"How do you combine all rows from both '{table1}' and '{table2}', including unmatched rows?",
                    f"Explain a full outer join between '{table1}' and '{table2}'."
                ],
                "level2": [
                    f"Formulate a relational algebra query for a full outer join between '{table1}' and '{table2}'.",
                    f"Describe how to retrieve all rows from '{table1}' and '{table2}', filling NULLs for unmatched rows.",
                    f"Write the full outer join expression in relational algebra for '{table1}' and '{table2}'."
                ],
                "level3": [
                    f"Explain and write a relational algebra query performing a full outer join between '{table1}' and '{table2}'.",
                    f"How does a full outer join handle unmatched rows differently from inner or outer joins?",
                    f"Compose a complex relational algebra expression for a full outer join between '{table1}' and '{table2}'."
                ],
            },
            "natural": {
                "level1": [
                    f"Write a natural join expression between '{table1}' and '{table2}' in relational algebra.",
                    f"How do you join '{table1}' and '{table2}' on all common attributes?",
                    f"Explain the natural join between '{table1}' and '{table2}'."
                ],
                "level2": [
                    f"Formulate a relational algebra query for a natural join between '{table1}' and '{table2}'.",
                    f"Describe how natural join works on '{table1}' and '{table2}' in relational algebra.",
                    f"Write the relational algebra expression for a natural join between '{table1}' and '{table2}'."
                ],
                "level3": [
                    f"Explain the working of natural join between '{table1}' and '{table2}' and write its relational algebra expression.",
                    f"How does natural join differ from equijoin in relational algebra between '{table1}' and '{table2}'?",
                    f"Compose a detailed relational algebra query for a natural join between '{table1}' and '{table2}'."
                ],
            },
            "equijoin": {
                "level1": [
                    f"Write an equijoin relational algebra expression between '{table1}' and '{table2}' on '{fk_column}'.",
                    f"How do you join '{table1}' and '{table2}' where '{fk_column}' matches in both tables?",
                    f"Explain equijoin between '{table1}' and '{table2}'."
                ],
                "level2": [
                    f"Formulate an equijoin query in relational algebra between '{table1}' and '{table2}'.",
                    f"Describe how to join '{table1}' and '{table2}' using equijoin on '{fk_column}'.",
                    f"Write the relational algebra expression for equijoin between '{table1}' and '{table2}'."
                ],
                "level3": [
                    f"Explain equijoin semantics and write a relational algebra expression for equijoin between '{table1}' and '{table2}'.",
                    f"How does equijoin differ from natural join in relational algebra between '{table1}' and '{table2}'?",
                    f"Compose a detailed relational algebra equijoin query for '{table1}' and '{table2}'."
                ],
            },
            "self": {
                "level1": [
                    f"Write a relational algebra expression for a self join on '{table1}'.",
                    f"Explain how a self join is performed on '{table1}'.",
                    f"How do you join a table to itself in relational algebra?"
                ],
                "level2": [
                    f"Formulate a relational algebra query performing a self join on '{table1}'.",
                    f"Describe the use of self join in relational algebra for '{table1}'.",
                    f"Write an expression to perform a self join on '{table1}'."
                ],
                "level3": [
                    f"Explain the concept of self join and write a relational algebra expression performing a self join on '{table1}'.",
                    f"How can self join be used to compare rows within '{table1}'?",
                    f"Compose a complex relational algebra expression for a self join on '{table1}'."
                ],
            },
        }

        # Select templates for the given join_type and level
        templates = base_templates.get(join_type, {}).get(level, [])
        if not templates:
            # fallback generic template if none found
            templates = [f"Write a relational algebra expression for a {join_type} join between '{table1}' and '{table2}'."]

        question = random.choice(templates)

        # Compose answer string
        if expression_simple != expression_explicit:
            answer = f"Simplified: {expression_simple}\nExplicit: {expression_explicit}"
        else:
            answer = expression_simple

        return {
            "type": "OEQ",
            "join_type": join_type.upper(),
            "level": level.upper(),
            "question": question,
            "answer": answer,
            "expected_keywords": [join_type, table1, table2, fk_column]
        }


    def generate_all_question_types(self, level="level1", join_type=None):
        output = []
        try:
            bq = self.generate_bq(level=level, join_type=join_type)
            output.append({**bq, "type": "BQ"})
        except Exception as e:
            output.append({"type": "BQ", "error": str(e), "level": level})

        for func_name in ["generate_tfq", "generate_mcq", "generate_mtq", "generate_ecq", "generate_diq", "generate_oeq"]:
            try:
                method = getattr(self, func_name)
                result = method(level=level, join_type=join_type)
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
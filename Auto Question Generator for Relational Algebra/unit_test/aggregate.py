import random

class AggregateGenerator:
    def __init__(self, table_name, table_schema):
        self.table_name = table_name
        self.schema = table_schema
        self.columns = [col for col, info in table_schema.items() if isinstance(info, dict) and 'type' in info]
        self.sample_data = table_schema.get("sample_data", [])
        self.aggregates = ["MAX", "MIN", "SUM", "AVG", "COUNT"]

    def generate_filters(self):
        filters = []
        if not self.sample_data:
            return filters

        for column in self.columns:
            col_type = self.schema[column].get("type", "string")
            sample_values = [row[column] for row in self.sample_data if column in row]

            if col_type in ("int", "float"):
                if sample_values:
                    value = random.choice(sample_values)
                    filters.append(f"{column} > {value}")
                    filters.append(f"{column} < {value}")
            elif col_type == "string":
                if sample_values:
                    value = random.choice(sample_values)
                    filters.append(f"{column} = '{value}'")
                    filters.append(f"{column} != '{value}'")
        return filters

    def _random_column(self):
        return random.choice(self.columns)
    
    def _random_aggregate(self):
        return random.choice(self.aggregates)
    
    def _resolve_agg_type(self, agg_type):
        if agg_type and agg_type.upper() in self.aggregates:
            return agg_type.upper()
        return None


    def generate_bq(self, level="level1", agg_type=None):
        if not self.columns:
            return None

        level = (level or "level1").lower()
        if level not in ["level1", "level2", "level3"]:
            level = "level1"

        col = self._random_column()
        agg = agg_type.upper() if agg_type and agg_type.upper() in self.aggregates else self._random_aggregate()

        bq_templates = {
    "SUM": {
        "level1": [
            f"What is the total value of '{col}' in the '{self.table_name}' table?",
            f"How much do all the '{col}' values add up to in '{self.table_name}'?",
            f"If you want to know the total '{col}' for all records, how would you get it?",
            f"How can you find the sum of '{col}' for everyone in '{self.table_name}'?",
            f"Suppose you need the total '{col}' for your business report. How do you get it?"
        ],
        "level2": [
            f"What is the total '{col}' for records that meet certain conditions in '{self.table_name}'?",
            f"How do you calculate the sum of '{col}' only for filtered data in '{self.table_name}'?",
            f"Suppose you want the total '{col}' for specific entries. How would you do it?",
            f"How can you find the sum of '{col}' for rows that match a filter?",
            f"Find the total '{col}' for records that satisfy a given rule."
        ],
        "level3": [
            f"How do you find the total '{col}' for each group in '{self.table_name}'?",
            f"Suppose you want to see the sum of '{col}' for every category. How would you do it?",
            f"How can you calculate the total '{col}' for each type or group in the data?",
            f"Show how to get the sum of '{col}' for each group in '{self.table_name}'.",
            f"How do you summarize '{col}' totals by group?"
        ]
    },
    "AVG": {
        "level1": [
            f"What is the average value of '{col}' in the '{self.table_name}' table?",
            f"How do you find the average (mean) of all '{col}' values in '{self.table_name}'?",
            f"Suppose you want to know the average '{col}' for all records. How would you get it?",
            f"How can you calculate the average of '{col}' in '{self.table_name}'?",
            f"What is the typical (average) value for '{col}' in this table?"
        ],
        "level2": [
            f"How do you find the average '{col}' for records that meet a certain condition?",
            f"Suppose you only want the average '{col}' for filtered data. How would you do it?",
            f"How can you get the mean of '{col}' for specific entries in '{self.table_name}'?",
            f"Find the average '{col}' for rows that match a filter.",
            f"How do you calculate the average '{col}' for selected records?"
        ],
        "level3": [
            f"How do you find the average '{col}' for each group in '{self.table_name}'?",
            f"Suppose you want to see the average '{col}' for every category. How would you do it?",
            f"How can you calculate the average '{col}' for each type or group in the data?",
            f"Show how to get the average '{col}' for each group in '{self.table_name}'.",
            f"How do you summarize '{col}' averages by group?"
        ]
    },
    "MIN": {
        "level1": [
            f"What is the smallest value of '{col}' in the '{self.table_name}' table?",
            f"How do you find the minimum '{col}' in '{self.table_name}'?",
            f"Suppose you want to know the lowest '{col}' for all records. How would you get it?",
            f"How can you find the least '{col}' in '{self.table_name}'?",
            f"What is the minimum value for '{col}' in this table?"
        ],
        "level2": [
            f"How do you find the minimum '{col}' for records that meet a certain condition?",
            f"Suppose you only want the lowest '{col}' for filtered data. How would you do it?",
            f"How can you get the minimum '{col}' for specific entries in '{self.table_name}'?",
            f"Find the smallest '{col}' for rows that match a filter.",
            f"How do you calculate the minimum '{col}' for selected records?"
        ],
        "level3": [
            f"How do you find the minimum '{col}' for each group in '{self.table_name}'?",
            f"Suppose you want to see the lowest '{col}' for every category. How would you do it?",
            f"How can you calculate the minimum '{col}' for each type or group in the data?",
            f"Show how to get the minimum '{col}' for each group in '{self.table_name}'.",
            f"How do you summarize '{col}' minimums by group?"
        ]
    },
    "MAX": {
        "level1": [
            f"What is the largest value of '{col}' in the '{self.table_name}' table?",
            f"How do you find the maximum '{col}' in '{self.table_name}'?",
            f"Suppose you want to know the highest '{col}' for all records. How would you get it?",
            f"How can you find the greatest '{col}' in '{self.table_name}'?",
            f"What is the maximum value for '{col}' in this table?"
        ],
        "level2": [
            f"How do you find the maximum '{col}' for records that meet a certain condition?",
            f"Suppose you only want the highest '{col}' for filtered data. How would you do it?",
            f"How can you get the maximum '{col}' for specific entries in '{self.table_name}'?",
            f"Find the largest '{col}' for rows that match a filter.",
            f"How do you calculate the maximum '{col}' for selected records?"
        ],
        "level3": [
            f"How do you find the maximum '{col}' for each group in '{self.table_name}'?",
            f"Suppose you want to see the highest '{col}' for every category. How would you do it?",
            f"How can you calculate the maximum '{col}' for each type or group in the data?",
            f"Show how to get the maximum '{col}' for each group in '{self.table_name}'.",
            f"How do you summarize '{col}' maximums by group?"
        ]
    },
    "COUNT": {
        "level1": [
            f"How many records are there in the '{self.table_name}' table?",
            f"How do you count all the rows in '{self.table_name}'?",
            f"Suppose you want to know the total number of entries. How would you get it?",
            f"How can you find out how many records are in '{self.table_name}'?",
            f"What is the total count of rows in this table?"
        ],
        "level2": [
            f"How do you count records that meet a certain condition in '{self.table_name}'?",
            f"Suppose you only want to count filtered data. How would you do it?",
            f"How can you get the count for specific entries in '{self.table_name}'?",
            f"Find the number of rows that match a filter.",
            f"How do you calculate the count for selected records?"
        ],
        "level3": [
            f"How do you count the number of records for each group in '{self.table_name}'?",
            f"Suppose you want to see the count for every category. How would you do it?",
            f"How can you calculate the count for each type or group in the data?",
            f"Show how to get the count for each group in '{self.table_name}'.",
            f"How do you summarize record counts by group?"
        ]
    }
}

        # Build expression
        if level == "level1":
            if agg == "COUNT":
                query = f"γ count(*)({self.table_name})"
            else:
                query = f"γ {agg.lower()}({col})({self.table_name})"

        elif level == "level2":
            filters = self.generate_filters()
            if len(filters) < 2:
                return None
            filter_expr = random.choice(filters)
            if agg == "COUNT":
                query = f"γ count(*) (σ({filter_expr})({self.table_name}))"
            else:
                query = f"γ {agg.lower()}({col})(σ({filter_expr})({self.table_name}))"

        elif level == "level3":
            group_col = random.choice([c for c in self.columns if c != col])
            if agg == "COUNT":
                query = f"γ {group_col}, count(*)({self.table_name})"
            else:
                query = f"γ {group_col}, {agg.lower()}({col})({self.table_name})"

        else:
            return None

        question = random.choice(bq_templates.get(agg, {}).get(level, [
            f"Write a relational algebra expression using {agg.lower()} for column '{col}'."
        ]))

        return {
            "type": "BQ",
            "level": level.upper(),
            "question": question,
            "answer": query
        }


    def generate_mcq(self, level="level1", agg_type=None):
        if not self.columns:
            return None

        level = (level or "level1").lower()
        if level not in ["level1", "level2", "level3"]:
            level = "level1"

        col = self._random_column()
        agg = agg_type.upper() if agg_type and agg_type.upper() in self.aggregates else random.choice(self.aggregates)

        correct = f"γ {agg.lower()}({col})({self.table_name})"
        wrong = [
            f"π ({agg.lower()}({col})) ({self.table_name})",
            f"σ ({agg.lower()}({col})) ({self.table_name})",
            f"γ {agg.upper()} ({self.table_name})"
        ]
        options = [correct] + random.sample(wrong, 3)
        random.shuffle(options)
        answer = chr(options.index(correct) + ord('a'))

        level_templates = {
            "SUM": {
                "level1": [
                    f"Which query calculates the sum of all '{col}' values in '{self.table_name}'?",
                    f"How would you express the total amount of '{col}' in relational algebra?",
                    f"Find the relational algebra expression that computes sum of '{col}'.",
                    f"What operation gives the total sum for '{col}' in '{self.table_name}'?",
                    f"Select the correct expression to determine total '{col}' values."
                ],
                "level2": [
                    f"Choose the correct aggregate function to sum values of '{col}' with conditions.",
                    f"Identify how to calculate the sum of '{col}' with filters applied.",
                    f"What expression returns sum('{col}') from '{self.table_name}' where conditions apply?"
                ],
                "level3": [
                    f"In relational algebra, how is the SUM aggregate applied to '{col}'?",
                    f"Formally derive the expression that calculates sum of '{col}'.",
                    f"From the relation '{self.table_name}', what gives the grouped sum of '{col}'?"
                ]
            },
            "AVG": {
                "level1": [
                    f"Which query calculates the average of column '{col}'?",
                    f"How do you compute the mean of '{col}' in relational algebra?",
                    f"Choose the expression that represents avg('{col}') in '{self.table_name}'."
                ],
                "level2": [
                    f"Identify the expression that finds average of '{col}' with filtering conditions.",
                    f"Which algebra computes average of '{col}' for filtered rows in '{self.table_name}'?"
                ],
                "level3": [
                    f"Which grouped query returns the average of '{col}' for each group in '{self.table_name}'?",
                    f"What formal expression gives avg('{col}') grouped by another column?"
                ]
            },
            "MIN": {
                "level1": [
                    f"What query retrieves the minimum value in '{col}'?",
                    f"Which relational algebra gives the smallest '{col}' value?",
                    f"Select the expression to compute the min of '{col}'."
                ],
                "level2": [
                    f"Which expression filters and finds the minimum of '{col}'?",
                    f"How is min('{col}') derived when conditions apply?"
                ],
                "level3": [
                    f"What relational algebra groups and computes minimum of '{col}'?",
                    f"Find expression computing grouped minimum of '{col}' in '{self.table_name}'."
                ]
            },
            "MAX": {
                "level1": [
                    f"What expression gives the maximum value of '{col}'?",
                    f"Which query computes the largest value in '{col}'?",
                    f"Choose the query that evaluates max of '{col}'."
                ],
                "level2": [
                    f"Identify how to find the max('{col}') after applying filters.",
                    f"How is the maximum of '{col}' computed with selection?"
                ],
                "level3": [
                    f"How do you group and find max('{col}') per group?",
                    f"What is the grouped max operation in relational algebra for '{col}'?"
                ]
            },
            "COUNT": {
                "level1": [
                    f"Which expression counts rows in '{self.table_name}'?",
                    f"What is the query to count entries of column '{col}'?",
                    f"Select the relational algebra operation that counts rows."
                ],
                "level2": [
                    f"How do you count rows satisfying a condition in '{self.table_name}'?",
                    f"What query counts distinct values in '{col}' with filters?"
                ],
                "level3": [
                    f"What expression returns count grouped by another column?",
                    f"Which query counts entries per group in relational algebra?"
                ]
            }
        }

        question_bank = level_templates.get(agg, {}).get(level, [
            f"Which relational algebra expression computes the {agg.lower()} of '{col}'?"
        ])

        question = random.choice(question_bank)

        return {
            "type": "MCQ",
            "level": level.upper(),
            "question": question,
            "options": {chr(i + 97): opt for i, opt in enumerate(options)},
            "answer": f"({answer})"
        }

    def generate_tfq(self, level="level1", agg_type=None):
        if not self.columns:
            return None

        level = (level or "level1").lower()
        if level not in ["level1", "level2", "level3"]:
            level = "level1"

        col = self._random_column()
        agg = agg_type.upper() if agg_type and agg_type.upper() in self.aggregates else self._random_aggregate()

        correct_expr = f"γ {agg.lower()}({col})({self.table_name})"
        incorrect_expr = f"σ {agg.lower()}({col})({self.table_name})"
        is_true = random.choice([True, False])
        expression = correct_expr if is_true else incorrect_expr

        tfq_templates = {
            "SUM": {
                "level1": [
                    f"{expression} returns the sum of '{col}' in '{self.table_name}'.",
                    f"Is the total value of '{col}' calculated by: {expression}?"
                ],
                "level2": [
                    f"Does {expression} correctly compute the summation of values in '{col}'?",
                    f"Evaluate the correctness of this sum operation: {expression}."
                ],
                "level3": [
                    f"True or False: {expression} represents a valid sum aggregation over column '{col}'.",
                    f"Determine the validity of this SUM query: {expression}."
                ]
            },
            "AVG": {
                "level1": [
                    f"{expression} computes the average of values in '{col}' column.",
                    f"Is this a correct query to find the mean of '{col}': {expression}?"
                ],
                "level2": [
                    f"Check if {expression} properly derives the average of '{col}' in relational algebra.",
                    f"Evaluate: {expression} performs the average aggregate function."
                ],
                "level3": [
                    f"True or False: The expression {expression} correctly computes the average value for '{col}'.",
                    f"Verify whether {expression} defines an accurate AVG operation on column '{col}'."
                ]
            },
            "MIN": {
                "level1": [
                    f"{expression} gives the minimum value of '{col}'.",
                    f"Does the query {expression} find the smallest value in column '{col}'?"
                ],
                "level2": [
                    f"Is the following expression correct for computing min('{col}'): {expression}?",
                    f"Check whether {expression} yields the lowest value of '{col}'."
                ],
                "level3": [
                    f"True or False: {expression} computes the minimum of column '{col}' from '{self.table_name}'.",
                    f"Validate if {expression} is a valid minimum aggregation query."
                ]
            },
            "MAX": {
                "level1": [
                    f"{expression} returns the highest value of '{col}' in the relation.",
                    f"Does {expression} represent a correct max operation on '{col}'?"
                ],
                "level2": [
                    f"Evaluate the max operation correctness for {expression} on '{col}'.",
                    f"Check if {expression} computes the maximum for column '{col}'."
                ],
                "level3": [
                    f"True or False: The expression {expression} is valid for finding maximum in column '{col}'.",
                    f"Determine the correctness of this MAX operation: {expression}."
                ]
            },
            "COUNT": {
                "level1": [
                    f"{expression} returns the number of entries in '{self.table_name}'.",
                    f"Does this expression count the tuples in the table: {expression}?"
                ],
                "level2": [
                    f"Evaluate if {expression} accurately counts entries in '{self.table_name}'.",
                    f"Is {expression} the correct way to count rows in relational algebra?"
                ],
                "level3": [
                    f"True or False: {expression} performs a valid COUNT aggregate over the dataset.",
                    f"Check if {expression} logically implements a count operation."
                ]
            }
        }

        question_bank = tfq_templates.get(agg, {}).get(level, [
            f"Does {expression} compute the {agg.lower()} of '{col}'?"
        ])

        question = random.choice(question_bank)

        return {
            "type": "TFQ",
            "level": level.upper(),
            "question": question,
            "answer": "True" if is_true else "False"
        }

    def generate_oeq(self, level="level1", agg_type=None):
        if not self.columns:
            return None

        level = (level or "level1").lower()
        if level not in ["level1", "level2", "level3"]:
            level = "level1"

        col = self._random_column()
        agg = agg_type.upper() if agg_type and agg_type.upper() in self.aggregates else self._random_aggregate()

        oeq_templates = {
            "SUM": {
                "level1": [
                    f"Write a relational algebra expression to compute the sum of '{col}' in table '{self.table_name}'.",
                    f"Construct a query to find the total value of column '{col}'.",
                    f"How can you calculate the total sum for '{col}' using relational algebra?"
                ],
                "level2": [
                    f"Devise a relational algebra expression that returns the sum of '{col}' with appropriate filters.",
                    f"Write a query to calculate the aggregate sum on column '{col}' from relation '{self.table_name}'."
                ],
                "level3": [
                    f"Formally construct an expression in relational algebra that calculates the grouped sum of '{col}'.",
                    f"Derive the relational algebra formula for summing column '{col}' grouped by another attribute."
                ]
            },
            "AVG": {
                "level1": [
                    f"Write the relational algebra expression to compute the average of '{col}' from '{self.table_name}'.",
                    f"How do you find the average value of '{col}' in relational algebra?"
                ],
                "level2": [
                    f"Compose a relational algebra query to calculate the mean of column '{col}' with a filter condition.",
                    f"Create an expression that computes the average of '{col}' using relational algebra."
                ],
                "level3": [
                    f"Formulate a grouped relational algebra query to evaluate average of '{col}' per group.",
                    f"Construct a complex relational algebra expression to find the average of '{col}' per combination of values."
                ]
            },
            "MIN": {
                "level1": [
                    f"Provide a relational algebra expression to get the minimum value in column '{col}'.",
                    f"Write the expression that computes the lowest value of '{col}' in '{self.table_name}'."
                ],
                "level2": [
                    f"Compose a query that returns the minimum of '{col}' with conditions applied.",
                    f"Devise a relational algebra formula to filter and compute min of '{col}'."
                ],
                "level3": [
                    f"Write a grouped query in relational algebra to retrieve min of '{col}'.",
                    f"How do you calculate minimum values of '{col}' grouped by another field in relational algebra?"
                ]
            },
            "MAX": {
                "level1": [
                    f"Construct a relational algebra expression to compute the maximum value of '{col}' from '{self.table_name}'.",
                    f"How is the max of column '{col}' expressed in relational algebra?"
                ],
                "level2": [
                    f"Write a filtered expression in relational algebra to find max of '{col}'.",
                    f"Compose a query for retrieving the maximum value from '{col}' under selection conditions."
                ],
                "level3": [
                    f"Design a grouped query to find the maximum of '{col}' across combinations in '{self.table_name}'.",
                    f"Formulate the relational algebra operation to compute groupwise max of '{col}'."
                ]
            },
            "COUNT": {
                "level1": [
                    f"Write the relational algebra expression to count rows in '{self.table_name}'.",
                    f"How would you represent a row count in relational algebra?"
                ],
                "level2": [
                    f"Devise a query in relational algebra to count rows satisfying a condition.",
                    f"Create a relational algebra expression that counts distinct values of column '{col}'."
                ],
                "level3": [
                    f"Formulate a relational algebra query to compute count grouped by another column.",
                    f"Write a grouped count query in relational algebra for column '{col}'."
                ]
            }
        }

        question_bank = oeq_templates.get(agg, {}).get(level, [
            f"Write the relational algebra expression to compute the {agg.lower()} of '{col}' in the table '{self.table_name}'."
        ])

        question = random.choice(question_bank)
        answer = f"γ {agg.lower()}({col})({self.table_name})"

        return {
            "type": "OEQ",
            "level": level.upper(),
            "question": question,
            "answer": answer
        }

    def generate_mtq(self, level="level1", agg_type=None):
        if not self.columns:
            return None

        level = (level or "level1").lower()
        if level not in ["level1", "level2", "level3"]:
            level = "level1"

        agg = agg_type.upper() if agg_type and agg_type.upper() in self.aggregates else self._random_aggregate()

        mtq_templates = {
            "SUM": {
                "level1": ["Match each SUM expression with its correct interpretation:"],
                "level2": ["Match each SUM expression to its filtered real-world meaning:"],
                "level3": ["Match each grouped SUM expression to its contextual description:"]
            },
            "AVG": {
                "level1": ["Match each AVG expression with its real-world equivalent:"],
                "level2": ["Identify AVG expressions and their filtered data meaning:"],
                "level3": ["Associate grouped AVG expressions with their respective scenarios:"]
            },
            "MIN": {
                "level1": ["Relate each MIN expression to what it returns:"],
                "level2": ["Link each MIN expression with a filtered condition meaning:"],
                "level3": ["Match grouped MIN expressions to their descriptions:"]
            },
            "MAX": {
                "level1": ["Match MAX queries with what they compute:"],
                "level2": ["Identify MAX expressions under filtering context:"],
                "level3": ["Group each MAX query with its real-world grouped usage:"]
            },
            "COUNT": {
                "level1": ["Match each COUNT query with what it counts:"],
                "level2": ["Connect COUNT expressions with filtered conditions:"],
                "level3": ["Match COUNT queries with grouped counting use cases:"]
            }
        }

        descriptions_by_agg = {
            "SUM": ["Total revenue", "Sum of salaries", "Total score", "Aggregate expenditure", "Sum of distances"],
            "AVG": ["Average salary", "Mean temperature", "Average marks", "Mean sales", "Average working hours"],
            "MIN": ["Lowest price", "Minimum score", "Smallest age", "Least salary", "Minimum units sold"],
            "MAX": ["Highest value", "Maximum height", "Max experience", "Greatest profit", "Top score"],
            "COUNT": ["Number of employees", "Count of entries", "Total number of orders", "Number of students", "Total records"]
        }

        col_set = set()
        pairs = []
        while len(pairs) < 3:
            col = self._random_column()
            if col in col_set:
                continue
            expr = f"γ {agg.lower()}({col})({self.table_name})"
            col_set.add(col)
            pairs.append((expr, col))

        descs = descriptions_by_agg[agg][:len(pairs)]
        labeled_descs = [(pairs[i][0], f"({chr(97+i)}) {descs[i]}") for i in range(len(pairs))]
        answer = ", ".join([f"{expr} → ({chr(97+i)})" for i, (expr, _) in enumerate(pairs)])
        question_text = random.choice(mtq_templates[agg].get(level, mtq_templates[agg]["level1"]))

        return {
            "type": "MTQ",
            "level": level.upper(),
            "question": question_text,
            "pairs": labeled_descs,
            "answer": answer
        }

    def generate_diq(self, level="level1", agg_type=None):
        if not self.columns:
            return None

        level = (level or "level1").lower()
        if level not in ["level1", "level2", "level3"]:
            level = "level1"

        col = self._random_column()
        agg = agg_type.upper() if agg_type and agg_type.upper() in self.aggregates else self._random_aggregate()

        tree = (
            f"      γ {agg.lower()}({col})\n"
            f"         |\n"
            f"     {self.table_name}"
        )

        templates_by_op = {
            "SUM": {
                "level1": [
                    "What does this tree compute in terms of total value?",
                    "Interpret the relational algebra tree to find the total sum computed.",
                    "What is the meaning of this tree in context of summing data?",
                    "What total does this tree compute from the relation?",
                    "How does this tree summarize values using summation?"
                ],
                "level2": [
                    "Explain how this tree summarizes the data using SUM.",
                    "Describe what the tree computes using a SUM operation.",
                    "What attribute is being summed up in the algebra tree?",
                    "Analyze the summation logic represented in the tree."
                ],
                "level3": [
                    "Describe in detail how this tree performs summation in relational algebra.",
                    "Provide a comprehensive explanation of the sum operation in the given algebra tree.",
                    "Discuss how the SUM operation is used in this hierarchical tree structure.",
                    "Explain how SUM is executed in layered relational algebra trees."
                ]
            },
            "AVG": {
                "level1": [
                    "What does this tree return in terms of average?",
                    "Interpret this algebra tree: What average is it computing?",
                    "How is average derived from this tree?",
                    "Which attribute's average is being calculated here?",
                    "What mean value is being computed by the tree?"
                ],
                "level2": [
                    "Analyze this tree in terms of calculating average.",
                    "What attribute's average is being derived from this tree?",
                    "Which column is targeted for average computation?",
                    "Describe the logic of averaging in this tree structure."
                ],
                "level3": [
                    "Describe the process and result of this average operation shown in the tree.",
                    "How does this relational algebra tree implement average aggregation?",
                    "Explain how the average function is constructed in the tree form.",
                    "Discuss the relational reasoning behind average in this tree."
                ]
            },
            "MIN": {
                "level1": [
                    "What minimum value is this tree calculating?",
                    "Interpret the purpose of this MIN operation in the algebra tree.",
                    "Which column's minimum value is this tree extracting?",
                    "What is the outcome of the MIN aggregation shown here?",
                    "Explain the basic goal of this MIN algebra tree."
                ],
                "level2": [
                    "Which value is returned as the minimum by this relational algebra tree?",
                    "Explain what the MIN function computes in this tree structure.",
                    "Describe how the MIN aggregation is being applied to the table data.",
                    "What role does the MIN operator play in this query tree?"
                ],
                "level3": [
                    "Analyze and explain the aggregation operation involving MIN.",
                    "Give a detailed interpretation of this MIN aggregation.",
                    "What is the logic behind using MIN here in the layered tree?",
                    "Explain the end-to-end function of the MIN operation within this tree."
                ]
            },
            "MAX": {
                "level1": [
                    "What maximum value is this algebra tree designed to retrieve?",
                    "Describe the role of MAX in this query tree.",
                    "What does this tree say about the largest value of a column?",
                    "How is maximum aggregation represented here?",
                    "What column's max is being fetched in this tree?"
                ],
                "level2": [
                    "Explain what attribute this MAX tree aggregates.",
                    "Interpret the purpose of this MAX aggregation.",
                    "What value does MAX return from this structure?",
                    "Analyze this tree to find how MAX is implemented."
                ],
                "level3": [
                    "Provide a detailed explanation of the MAX computation in this tree.",
                    "How does the tree structure apply the MAX operation to the data?",
                    "Break down the use of MAX in this relational tree format.",
                    "Explain the data flow and result computation of the MAX node."
                ]
            },
            "COUNT": {
                "level1": [
                    "What count does this algebra tree return?",
                    "Interpret the aggregation tree computing COUNT.",
                    "How many rows are being counted by this expression?",
                    "What is the function of COUNT in this structure?",
                    "Describe what is being quantified in this algebra tree."
                ],
                "level2": [
                    "What does the COUNT function in this tree return?",
                    "Analyze how the COUNT is performed in this query.",
                    "How is the number of entries derived in this tree?",
                    "Explain the COUNT process used in this algebra expression."
                ],
                "level3": [
                    "Explain in detail what COUNT operation is represented by the algebra tree.",
                    "Provide a breakdown of this COUNT query in relational algebra terms.",
                    "Discuss how COUNT is computed structurally in this tree.",
                    "Describe each step that leads to the final COUNT result in this operation."
                ]
            }
        }

        question = random.choice(templates_by_op.get(agg, {}).get(level, [
            f"Interpret the aggregation performed in this tree involving {agg.lower()}"
        ]))

        answer = f"{agg.lower()} of {col} from {self.table_name}"

        return {
            "type": "DIQ",
            "level": level.upper(),
            "question": question,
            "tree": tree,
            "answer": answer
        }

    def generate_ecq(self, level="level1", agg_type=None):
        if not self.columns:
            return None

        level = (level or "level1").lower()
        if level not in ["level1", "level2", "level3"]:
            level = "level1"

        col = self._random_column()
        agg = agg_type.upper() if agg_type and agg_type.upper() in self.aggregates else self._random_aggregate()

        templates_by_op = {
            "SUM": {
                "level1": [
                    f"Explain how the aggregation γ sum({col})({self.table_name}) works in relational algebra.",
                    f"What does γ sum({col})({self.table_name}) compute? Provide a brief explanation.",
                    f"Describe the role of the sum operation γ sum({col})({self.table_name})."
                ],
                "level2": [
                    f"Provide a detailed explanation of γ sum({col})({self.table_name}).",
                    f"How does the sum aggregation γ sum({col})({self.table_name}) function?",
                    f"Explain the effect of applying sum on the '{col}' column in γ sum({col})({self.table_name})."
                ],
                "level3": [
                    f"Discuss the in-depth operation and impact of γ sum({col})({self.table_name}).",
                    f"Explain the relational algebra summation process in γ sum({col})({self.table_name}).",
                    f"Analyze the detailed behavior of the sum aggregation γ sum({col})({self.table_name})."
                ],
            },
            "AVG": {
                "level1": [
                    f"Explain how the average aggregation γ avg({col})({self.table_name}) works.",
                    f"What does γ avg({col})({self.table_name}) compute? Provide a brief explanation.",
                    f"Describe the function of avg in γ avg({col})({self.table_name})."
                ],
                "level2": [
                    f"Provide a detailed explanation of γ avg({col})({self.table_name}).",
                    f"How is average calculated in γ avg({col})({self.table_name})?",
                    f"Explain how avg aggregates the '{col}' column in γ avg({col})({self.table_name})."
                ],
                "level3": [
                    f"Discuss the detailed implementation of average in γ avg({col})({self.table_name}).",
                    f"Analyze how the avg operator aggregates data in γ avg({col})({self.table_name}).",
                    f"Explain the purpose and effect of the average aggregation in γ avg({col})({self.table_name})."
                ],
            },
            "MIN": {
                "level1": [
                    f"Explain how the minimum aggregation γ min({col})({self.table_name}) works.",
                    f"What does γ min({col})({self.table_name}) compute? Provide a brief explanation.",
                    f"Describe the role of min in γ min({col})({self.table_name})."
                ],
                "level2": [
                    f"Provide a detailed explanation of γ min({col})({self.table_name}).",
                    f"How is the minimum value found in γ min({col})({self.table_name})?",
                    f"Explain how min aggregates the '{col}' column in this expression."
                ],
                "level3": [
                    f"Discuss the detailed behavior of the min operator in γ min({col})({self.table_name}).",
                    f"Analyze how the min function is applied in the aggregation γ min({col})({self.table_name}).",
                    f"Explain the purpose and effect of the min aggregation in relational algebra."
                ],
            },
            "MAX": {
                "level1": [
                    f"Explain how the maximum aggregation γ max({col})({self.table_name}) works.",
                    f"What does γ max({col})({self.table_name}) compute? Provide a brief explanation.",
                    f"Describe the role of max in γ max({col})({self.table_name})."
                ],
                "level2": [
                    f"Provide a detailed explanation of γ max({col})({self.table_name}).",
                    f"How is the maximum value found in γ max({col})({self.table_name})?",
                    f"Explain how max aggregates the '{col}' column in this expression."
                ],
                "level3": [
                    f"Discuss the detailed behavior of the max operator in γ max({col})({self.table_name}).",
                    f"Analyze how the max function is applied in the aggregation γ max({col})({self.table_name}).",
                    f"Explain the purpose and effect of the max aggregation in relational algebra."
                ],
            },
            "COUNT": {
                "level1": [
                    f"Explain how the count aggregation γ count({col})({self.table_name}) works.",
                    f"What does γ count({col})({self.table_name}) compute? Provide a brief explanation.",
                    f"Describe the role of count in γ count({col})({self.table_name})."
                ],
                "level2": [
                    f"Provide a detailed explanation of γ count({col})({self.table_name}).",
                    f"How is the count value computed in γ count({col})({self.table_name})?",
                    f"Explain how count aggregates the '{col}' column in this expression."
                ],
                "level3": [
                    f"Discuss the detailed behavior of the count operator in γ count({col})({self.table_name}).",
                    f"Analyze how the count function is applied in the aggregation γ count({col})({self.table_name}).",
                    f"Explain the purpose and effect of the count aggregation in relational algebra."
                ],
            }
        }

        question = random.choice(templates_by_op.get(agg, {}).get(level, [
            f"Explain the aggregation γ {agg.lower()}({col})({self.table_name}) in relational algebra."
        ]))

        base_answer = (
            f"The operator γ {agg.lower()}({col})({self.table_name}) computes the {agg.lower()} of the '{col}' column "
            f"across all records in the '{self.table_name}' table. It performs an aggregation without grouping."
        )

        if level == "level2":
            answer = base_answer + " This involves applying the aggregation function on the entire relation, summarizing the column's data."
        elif level == "level3":
            answer = (
                base_answer +
                " This aggregation operator processes the entire dataset without grouping attributes, "
                "yielding a single summarized value that represents the chosen aggregate function applied to the specified column."
            )
        else:
            answer = base_answer

        return {
            "type": "ECQ",
            "level": level.upper(),
            "question": question,
            "answer": answer
        }

    def generate_all_question_types(self, level="level1", agg_type=None):
        output = []
        try:
            bq = self.generate_bq(level=level, agg_type=agg_type)
            output.append({**bq, "type": "BQ"})
        except Exception as e:
            output.append({"type": "BQ", "error": str(e), "level": level})

        for func_name in ["generate_tfq", "generate_mcq", "generate_mtq", "generate_ecq", "generate_diq", "generate_oeq"]:
            try:
                method = getattr(self, func_name)
                result = method(level=level, agg_type=agg_type)
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

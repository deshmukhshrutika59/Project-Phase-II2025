import os
import json
import pandas as pd
import random
import hashlib
import streamlit as st
from streamlit_mermaid import st_mermaid
from schemas.schema import get_schema_by_name
from unit_test.select import SelectionGenerator
from unit_test.projection import ProjectionGenerator
from unit_test.rename import RenameGenerator
from unit_test.aggregate import AggregateGenerator
from unit_test.join import JoinGenerator
from unit_test.set_operation import SetOperationGenerator
from unit_test.cross_join import CrossJoinGenerator
from unit_test.division import DivisionGenerator
from unit_test.group_by import GroupByQuestionGenerator
from unit_test.query_tree import QueryTreeGenerator

# --- Helper Functions ---
def generate_questions_for_types(generator, question_types, level, num_per_type, **kwargs):
    questions = []
    for q_type in question_types:
        method = getattr(generator, f"generate_{q_type.lower()}", None)
        if method:
            for _ in range(num_per_type):
                try:
                    q = method(level=level, **kwargs)  # Pass any extra arguments dynamically
                    if q:
                        if isinstance(q, tuple) and len(q) == 2:
                            q = {"question": q[0], "answer": q[1]}
                        q["type"] = q_type
                        questions.append(q)
                except Exception as e:
                    st.warning(f"Error generating {q_type} question: {e}")
    return questions

def mermaid_key(table_name, i, qinfo):
    unique_str = f"{table_name}_{i}_{qinfo.get('question', '')}_{qinfo.get('tree', '')}"
    unique_hash = hashlib.md5(unique_str.encode()).hexdigest()
    return f"mermaid_{table_name}_{i}_{unique_hash}"

def generate_mermaid_er_diagram(schema):
    lines = ["erDiagram"]
    for table_name, columns in schema.items():
        if not isinstance(columns, dict):
            continue
        lines.append(f"  {table_name} {{")
        for attr, info in columns.items():
            if isinstance(info, dict):
                attr_type = info.get("type", "string").lower()
                suffix = " PK" if info.get("primary_key") else ""
                lines.append(f"    {attr_type} {attr}{suffix}")
        lines.append("  }")

    for table_name, columns in schema.items():
        if not isinstance(columns, dict):
            continue
        for attr, info in columns.items():
            if isinstance(info, dict) and "foreign_key" in info:
                fk = info["foreign_key"]
                if "." in fk:
                    ref_table, _ = fk.split(".")
                    lines.append(f"  {table_name} ||--o| {ref_table} : \"{attr}\"")
    return "\n".join(lines)

def display_table_info(table_name, table_columns):
    primary_keys = [attr for attr, info in table_columns.items() if isinstance(info, dict) and info.get("primary_key")]
    foreign_keys = [(attr, info["foreign_key"]) for attr, info in table_columns.items() if isinstance(info, dict) and "foreign_key" in info]
    st.markdown(f"### Table: `{table_name}`")
    st.write("#### Primary Key(s):", primary_keys if primary_keys else "None")
    st.write("#### Foreign Key(s):", foreign_keys if foreign_keys else "None")

# --- Main Application ---
def main():
    st.title("Relational Algebra Question Generator")

    config_data = {}
    if os.path.exists("config.json"):
        with open("config.json", "r") as f:
            config_data = json.load(f)

    selected_topic = config_data.get("topic", "SELECT")
    selected_level = config_data.get("level", "LEVEL1")
    selected_join_type = config_data.get("subtopic", "inner") if selected_topic == "JOIN" else None
    selected_set_op = config_data.get("subtopic", "union") if selected_topic == "SET_OPERATION" else None
    selected_agg_type = config_data.get("subtopic","sum") if selected_topic == "AGGREGATE" else None
    selected_que_type = config_data.get("questiontype",["BQ"])
    num_questions_val = config_data.get("num_questions", 3)

    topic = selected_topic
    level = selected_level
    join_subtopic = selected_join_type
    set_op_type = selected_set_op
    agg_op_type = selected_agg_type
    question_types = selected_que_type if isinstance(selected_que_type, list) else [selected_que_type]
    num_questions = num_questions_val
    submitted = True

    schema = get_schema_by_name()

    if not schema:
        st.error("No schema found. Please check your schema configuration.")
        return

    if submitted:
        st.subheader("📌 ER Diagram of the Schema")
        st_mermaid(generate_mermaid_er_diagram(schema))
        st.markdown("---")

        total_questions = 0

        if topic == "DIVISION":
            valid_pairs = []
            for table1_name, table1_schema in schema.items():
                for table2_name, table2_schema in schema.items():
                    if table1_name == table2_name:
                        continue
                    if not isinstance(table1_schema, dict) or not isinstance(table2_schema, dict):
                        continue
                    if "sample_data" not in table1_schema or "sample_data" not in table2_schema:
                        continue

                    shared_attrs = list(set(table1_schema.keys()) & set(table2_schema.keys()) - {"sample_data"})
                    if shared_attrs:
                        valid_pairs.append((table1_name, table2_name, table1_schema, table2_schema, shared_attrs))

            if not valid_pairs:
                st.warning("No valid table pairs found for division.")
            else:
                for table1_name, table2_name, table1_schema, table2_schema, shared_attrs in valid_pairs:
                    display_table_info(table1_name, table1_schema)
                    st.markdown(f"**Dividing `{table1_name}` by `{table2_name}` using shared attributes: `{shared_attrs}`**")

                    st.markdown(f"#### Sample Data from `{table1_name}`")
                    st.dataframe(pd.DataFrame(table1_schema["sample_data"]))
                    st.markdown(f"#### Sample Data from `{table2_name}`")
                    st.dataframe(pd.DataFrame(table2_schema["sample_data"]))

                    gen = DivisionGenerator(table1_name, table2_name, table1_schema, table2_schema)
                    questions = generate_questions_for_types(gen, question_types, level.lower(), num_questions)

                    if questions:
                        st.markdown("### Generated Questions")
                        for i, qinfo in enumerate(questions, 1):
                            qtype = qinfo.get("type", "-")
                            st.markdown(f"**[{qtype}] Q{i}:** {qinfo.get('question', '[No question]')}")

                            if qtype == "MCQ" and qinfo.get("options"):
                                for k, v in qinfo["options"].items():
                                    st.write(f"{k}) {v}")
                                st.write(f"*Answer:* {qinfo.get('answer', '')}")

                            elif qtype == "MTQ" and qinfo.get("pairs"):
                                for op, desc in qinfo["pairs"]:
                                    st.write(f"{op}: {desc}")
                                st.write(f"*Answer:* {qinfo.get('answer', '')}")

                            elif qtype == "DIQ":
                                tree = qinfo.get("tree")
                                if tree:
                                    if tree.strip().startswith("graph"):
                                        unique_key = mermaid_key(table1_name, i, qinfo)
                                        st_mermaid(tree, key=unique_key)
                                    else:
                                        lines = [line.strip() for line in tree.split("\n") if line.strip()]
                                        if len(lines) > 1:
                                            mermaid = "graph TD\n"
                                            prev_node = None
                                            for idx, line in enumerate(lines):
                                                node_id = f"n{idx}"
                                                mermaid += f'    {node_id}["{line}"]\n'
                                                if prev_node:
                                                    mermaid += f"    {prev_node} --> {node_id}\n"
                                                prev_node = node_id
                                            unique_key = mermaid_key(table1_name, i, qinfo)
                                            st_mermaid(mermaid, key=unique_key)
                                        else:
                                            st.code(tree, language="text")
                                st.write(f"**Answer:** `{qinfo.get('answer', '')}`")

                            else:
                                st.markdown(f"**Answer:** `{qinfo.get('answer', 'N/A')}`")
                            st.markdown("---")
                            total_questions += 1

                st.success(f"✅ Total Questions Generated for Division: {total_questions}")

        else:
            for table_name, table_columns in random.sample(list(schema.items()), len(schema)):
                if not isinstance(table_columns, dict):
                    continue

                # Generate questions based on selected topic
                if topic == "SELECT":
                    gen = SelectionGenerator(table_name, table_columns)
                    questions = generate_questions_for_types(gen, question_types, level.lower(), num_questions)

                elif topic == "PROJECTION":
                    gen = ProjectionGenerator(table_name, table_columns)
                    questions = generate_questions_for_types(gen, question_types, level.lower(), num_questions)

                elif topic == "RENAME":
                    gen = RenameGenerator(table_name, table_columns)
                    questions = generate_questions_for_types(gen, question_types, level.lower(), num_questions)

                elif topic == "AGGREGATE":
                    gen = AggregateGenerator(table_name, table_columns)
                    questions = generate_questions_for_types(gen, question_types, level.lower(), num_questions, agg_type=agg_op_type)

                elif topic == "JOIN":
                    gen = JoinGenerator(table_name, table_columns, schema)
                    questions = generate_questions_for_types(gen, question_types, level.lower(), num_questions, join_type=join_subtopic)

                elif topic == "SET_OPERATION":
                    gen = SetOperationGenerator(table_name, table_columns)
                    questions = generate_questions_for_types(gen, question_types, level.lower(), num_questions, set_op_type=set_op_type)

                elif topic == "CROSS_JOIN":
                    gen = CrossJoinGenerator(table_name, table_columns)
                    questions = generate_questions_for_types(gen, question_types, level.lower(), num_questions)
                    
                elif topic == "GROUP_BY":
                    gen = GroupByQuestionGenerator(table_name, table_columns)
                    questions = generate_questions_for_types(gen, question_types, level.lower(), num_questions)
                    
                elif topic == "QUERY_TREE":
                    gen = QueryTreeGenerator(table_name, table_columns)
                    questions = generate_questions_for_types(gen, question_types, level.lower(), num_questions)
                else:
                    continue

                if questions:
                    st.markdown("### Generated Questions")
                    for i, qinfo in enumerate(questions, 1):
                        display_table_info(table_name, table_columns)
                        if "sample_data" in table_columns:
                            sample_df = pd.DataFrame(table_columns["sample_data"])
                            st.markdown("#### Sample Data:")
                            st.dataframe(sample_df)
                        else:
                            st.markdown("No sample data available.")
                        qtype = qinfo.get("type", "-")
                        st.markdown(f"**[{qtype}] Q{i}:** {qinfo.get('question', '[No question]')}")

                        if qtype == "MCQ" and qinfo.get("options"):
                            for k, v in qinfo["options"].items():
                                st.write(f"{k}) {v}")
                            st.write(f"*Answer:* {qinfo.get('answer', '')}")

                        elif qtype == "MTQ":
                            # For GROUP_BY and similar: options/answers
                            if qinfo.get("options"):
                                for k, v in qinfo["options"].items():
                                    st.write(f"{k}) {v}")
                                st.write(f"*Answer:* {qinfo.get('answer', '')}")
                                correct_letters = [k for k, v in qinfo.get("answers", {}).items() if v]
                                if correct_letters:
                                    st.write("**Correct Statements:**")
                                    for k in correct_letters:
                                        st.write(f"{k}) {qinfo['options'][k]}")
                            # For JOIN, SET_OPERATION, etc.: pairs
                            elif qinfo.get("pairs"):
                                for op, desc in qinfo["pairs"]:
                                    st.write(f"{op}: {desc}")
                                st.write(f"*Answer:* {qinfo.get('answer', '')}")

                        elif qtype in ["BQ", "OEQ"] :
                            tree = qinfo.get("tree")
                            if tree:
                                st.markdown("**Query Tree:**")
                                st.code(tree, language="text")
                            # Always show the answer
                            st.write(f"**Answer:** `{qinfo.get('answer', 'N/A')}`")
                            
                        elif qtype == "DIQ":
                            tree = qinfo.get("tree")
                            if tree:
                                if tree.strip().startswith("graph"):
                                    unique_key = mermaid_key(table_name, i, qinfo)
                                    st_mermaid(tree, key=unique_key)
                                else:
                                    if "|" in tree:
                                        lines = [line.strip() for line in tree.split("|") if line.strip()]
                                    else:
                                        lines = [line.strip() for line in tree.split("\n") if line.strip()]
                                    if len(lines) > 1:
                                        mermaid = "graph TD\n"
                                        prev_node = None
                                        for idx, line in enumerate(lines):
                                            node_id = f"n{idx}"
                                            mermaid += f'    {node_id}["{line}"]\n'
                                            if prev_node:
                                                mermaid += f"    {prev_node} --> {node_id}\n"
                                            prev_node = node_id
                                        unique_key = mermaid_key(table_name, i, qinfo)
                                        st_mermaid(mermaid, key=unique_key)
                                    else:
                                        # Fallback: just show the tree as text
                                        st.code(tree, language="text")
                            st.write(f"**Answer:** `{qinfo.get('answer', '')}`")         

                        else:
                            st.markdown(f"**Answer:** `{qinfo.get('answer', 'N/A')}`")
                        st.markdown("---")
                        total_questions += 1

            st.success(f"✅ Total Questions Generated: {total_questions}")

if __name__ == "__main__":
    main()

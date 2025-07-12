import json
import subprocess
import argparse

def main():
    parser = argparse.ArgumentParser(description="Relational Algebra Question Generator")

    parser.add_argument("--topic", required=True, choices=[
        "SELECT", "PROJECTION", "RENAME", "AGGREGATE", "JOIN",
        "SET_OPERATION", "CROSS_JOIN", "DIVISION", "GROUP_BY", "QUERY_TREE"
    ], help="Topic name")

    parser.add_argument("--subtopic", help="Subtopic (e.g., join type or set operation)")

    parser.add_argument("--level", required=True, choices=["LEVEL1", "LEVEL2", "LEVEL3"], help="Difficulty level")

    parser.add_argument("--questiontypes", required=True, help="Comma-separated question types (e.g., BQ,MCQ,TFQ)")

    parser.add_argument("--num_questions", type=int, required=True, help="Number of questions per type")

    args = parser.parse_args()

    selected_qtypes = [qt.strip() for qt in args.questiontypes.split(",")]

    config = {
        "topic": args.topic,
        "subtopic": args.subtopic,
        "level": args.level,
        "num_questions": args.num_questions,
        "questiontype": selected_qtypes
    }

    # Save to config file
    with open("config.json", "w") as f:
        json.dump(config, f)

    print("🔧 Configuration saved. Launching Streamlit...")
    subprocess.run(["python", "-m", "streamlit", "run", "streamlit_app.py", "--", args.topic])

if __name__ == "__main__":
    main()
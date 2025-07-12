# 🧮 Relational Algebra Auto Question Generator

An intelligent, command-line-based educational tool designed to generate relational algebra questions in  
natural language, along with their corresponding validated queries and visual representations. Developed as  
part of an internship at [AksharaPlus.org](https://www.aksharaplus.org), this project showcases the application  
of intelligent automation in advancing database education.

---

## 🎯 Project Objectives

- Automate the creation of practice and assessment questions for relational algebra  
- Support multiple difficulty levels and question types for personalized learning  
- Generate syntactically correct and logically valid queries  
- Provide visual query trees to aid conceptual understanding  
- Allow easy interaction via command-line interface (CLI)  

---

## 🧠 Key Features

- Automatic question generation using rule-based logic  
- Command-line user inputs for operation, difficulty level, question type, and number of questions  
- Random schema selection from predefined datasets  
- Query validation using Python’s `unittest` framework  
- Visual output with Mermaid.js diagrams for query trees  
- Modular architecture for easy expansion and maintenance  
- Supports future integration with Small Language Models (SLMs)  

---

## 🧰 Technologies Used

- Python 3  
- Command-Line Interface (CLI)  
- `unittest` (for backend validation)  
- Mermaid.js (for query tree visualization)  
- Streamlit *(for optional UI)*  

---

## 🛠️ Supported Operations

- Selection  
- Projection  
- Join  
- Rename  
- Set Operations (Union, Intersection, Difference)  
- Aggregate Functions  
- Cross Join  
- Division  

---

## ❓ Supported Question Types

- `MCQ` – Multiple Choice Questions  
- `TFQ` – True/False Questions  
- `OEQ` – Open-Ended Questions  
- `GQ` / `BQ` – Generated/Base Query Questions  
- `ECQ` – Expression Completion Questions  
- `DIQ` – Diagram-based Input Questions  

---

## 🚀 How to Use

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/relational-algebra-question-generator.git
cd relational-algebra-question-generator
```
### 🚀 2. Run the CLI

```bash
python cli.py --topic SELECT --level LEVEL3 --questiontypes BQ --num_questions 10
```
### 📊 3. Parameters Description

| Parameter          | Description                                | Example                |
|-------------------|--------------------------------------------|------------------------|
| `--topic`         | Operation type (e.g., SELECT, JOIN)         | `--topic SELECT`       |
| `--level`         | Difficulty level                            | `--level LEVEL3`       |
| `--questiontypes` | Question format (MCQ, TFQ, etc.)            | `--questiontypes BQ`   |
| `--num_questions` | Number of questions to generate             | `--num_questions 10`   |

> 🔀 **Note:** The schema is randomly selected from a predefined set.

---

### 🔮 Future Enhancements

- Integration with **Small Language Models (SLMs)** / **Large Language Models (LLMs)**
- Optional **GUI using Streamlit**
- **User-defined schema upload** functionality
- **Export questions** to PDF or HTML formats

### 🙏 Internship & Acknowledgments

This project was developed as part of a **skill-based internship** in collaboration with [**AksharaPlus.org**](https://www.aksharaplus.org).

#### 🧑‍🏫 Guidance and Support

- **Dr. Venkat N. Gudivada** – Mentor and Research Advisor  
- **Dr. Rajurkar A. M.** – Internship Guide and Head, CSE Department, MGM COE Nanded  
- **Dr. Lathkar G. S.** – Director, MGM COE Nanded  

---

### 👥 Team Members

- Ambika Gangawar  
- Shrutika Deshmukh  
- Vishal Dhavale 


---

### 👨‍💻 Author & Credit

This project is an **internship project** developed under the mentorship of **AksharaPlus.org**.  
All rights reserved by the respective authors and academic collaborators.

📌 **Project Type**: Academic Internship  
🏢 **Organization**: [AksharaPlus.org](https://www.aksharaplus.org)  
📅 **Year**: 2025  






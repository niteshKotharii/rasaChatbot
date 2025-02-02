import pandas as pd

# Load the Excel file
excel_file = "questions_answers.xlsx"  
sheet_name = "Sheet1"  
df = pd.read_excel(excel_file, sheet_name=sheet_name, header=None)  

# Extract questions from the first column
questions = df[0].tolist()  # Assuming questions are in the first column (column index 0)

# Generate the nlu.yml content
nlu_content = """version: "3.0"
nlu:
  - intent: ask_complex_question
    examples: |
"""

# Add each question as an example
for question in questions:
    nlu_content += f"      - {question}\n"

# Write the content to a nlu.yml file
output_file = "nlu2.yml"
with open(output_file, "w") as file:
    file.write(nlu_content)

print(f"nlu.yml file has been created with {len(questions)} examples.")
import pandas as pd
import yaml

# Load clustered Excel file
file_path = "clustered_questions.xlsx"  # Update with your file name
data = pd.read_excel(file_path)

# Ensure the Excel file has the correct columns
assert {"Question", "Answer", "Cluster"}.issubset(data.columns), "Missing required columns in Excel file."

# Group data by clusters
clusters = data.groupby("Cluster")

# Initialize Rasa files' data
nlu_data = {"version": "3.1", "nlu": []}
domain_data = {"version": "3.1", "intents": [], "responses": {}}
stories_data = {"version": "3.1", "stories": []}

# Generate data for each cluster
for cluster_name, group in clusters:
    # Define intent and response names
    intent_name = f"intent_{cluster_name}"
    response_name = f"utter_{cluster_name}"
    
    # Add intent to domain.yml
    domain_data["intents"].append(intent_name)
    
    # Add training examples to nlu.yml
    examples = [{"text": question} for question in group["Question"]]
    nlu_data["nlu"].append({"intent": intent_name, "examples": examples})
    
    # Add responses to domain.yml
    responses = [{"text": f"{answer}"} for answer in group["Answer"]]
    domain_data["responses"][response_name] = responses

    
    # Add story to stories.yml
    story = {
        "story": f"Respond to {intent_name}",
        "steps": [
            {"intent": intent_name},
            {"action": response_name},
        ],
    }
    stories_data["stories"].append(story)

# Save files
with open("nlu2.yml", "w") as nlu_file:
    yaml.dump(nlu_data, nlu_file, allow_unicode=True, sort_keys=False)

with open("domain2.yml", "w") as domain_file:
    yaml.dump(domain_data, domain_file, allow_unicode=True, sort_keys=False)

with open("stories2.yml", "w") as stories_file:
    yaml.dump(stories_data, stories_file, allow_unicode=True, sort_keys=False)

print("Rasa files generated: nlu.yml, domain.yml, and stories.yml")

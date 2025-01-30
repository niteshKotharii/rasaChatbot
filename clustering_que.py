import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import re

# Step 1: Load the Excel file
file_path = "questions_answers.xlsx"  
df = pd.read_excel(file_path)

if "Question" not in df.columns or "Answer" not in df.columns:
    raise ValueError("The Excel file must contain 'Question' and 'Answer' columns.")

# Step 2: Preprocess the questions
def preprocess_text(text):
    text = re.sub(r"[^\w\s]", "", text)  # Remove punctuation
    text = text.lower().strip()  # Lowercase and strip spaces
    return text

df["Cleaned_Question"] = df["Question"].apply(preprocess_text)

# Step 3: Convert questions to numerical format using TF-IDF
vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
X = vectorizer.fit_transform(df["Cleaned_Question"])

# Step 4: Determine the optimal number of clusters (optional)
# Use silhouette score or elbow method to find the best 'k'
best_k = 0
best_score = -1
for k in range(2, 51):  # Try clustering with k=2 to k=50
    kmeans = KMeans(n_clusters=k, random_state=42)
    labels = kmeans.fit_predict(X)
    score = silhouette_score(X, labels)
    if score > best_score:
        best_k = k
        best_score = score

print(f"Optimal number of clusters: {best_k}")

# Step 5: Perform KMeans clustering
kmeans = KMeans(n_clusters=best_k, random_state=42)
df["Cluster"] = kmeans.fit_predict(X)

# Step 6: Save the clustered data
output_file = "clustered_questions.xlsx"
df.to_excel(output_file, index=False)
print(f"Clustered data saved to {output_file}")

import spacy
from sklearn.metrics.pairwise import cosine_similarity
import json
import pandas as pd


NUMBER_OF_GROUPS = 10 # It has to be less than the number of companies

# Load the English language model in spaCy
nlp = spacy.load('en_core_web_md')

# Load the JSON data
with open('all_corporates.json', 'r') as file:
    data = json.load(file)

# Extract and preprocess descriptions
descriptions = [company['description'] for company in data]
preprocessed_descriptions = []

def preprocess(text):
    # Remove punctuation and stop words
    doc = nlp(text)
    tokens = [token.text for token in doc if not token.is_punct and not token.is_stop]
    return ' '.join(tokens)

for description in descriptions:
    # Perform preprocessing steps (remove stopwords, punctuation, etc.)
    preprocessed_description = preprocess(description)
    preprocessed_descriptions.append(preprocessed_description)

# Convert descriptions to embeddings
description_embeddings = [nlp(description).vector for description in preprocessed_descriptions]

# Calculate cosine similarity between all pairs of descriptions
similarity_matrix = cosine_similarity(description_embeddings, description_embeddings)

# Define a threshold for similarity score to group companies
threshold = 0.9999

# Group companies based on similarity scores
groups = {}
for i in range(NUMBER_OF_GROUPS):
    groups[i] = [j for j, score in enumerate(similarity_matrix[i]) if score >= threshold]

for i in range(NUMBER_OF_GROUPS, len(data)):
    max_similarity = 0
    max_similarity_index = 0
    for j in range(NUMBER_OF_GROUPS):
        if similarity_matrix[i][j] > max_similarity:
            max_similarity = similarity_matrix[i][j]
            max_similarity_index = j
    groups[max_similarity_index].append(i)

grouped_companies = []

for group_id, group_members in groups.items():
    temp_group = []
    print(f"Group {group_id + 1}:")
    for member_id in group_members:
        temp_group.append([data[member_id]['name'], data[member_id]['description']])
        print(data[member_id]['name'], data[member_id]['description'])
    grouped_companies.append(temp_group)
    print()

total = 0
for group in grouped_companies:
    total += len(group) 
    print("Group's members : " + str(len(group)))
print("Total number of companies : " + str(total))

df = pd.DataFrame()

for i, group in enumerate(grouped_companies, start=1):
    group_df = pd.DataFrame(group, columns=[f'Group {i} Name', f'Group {i} Description'])
    df = pd.concat([df, group_df], axis=1)

# Save the DataFrame to an Excel file
output_excel_file = 'grouped_companies.xlsx'
df.to_excel(output_excel_file, index=False)

print(f"Data saved to {output_excel_file}")


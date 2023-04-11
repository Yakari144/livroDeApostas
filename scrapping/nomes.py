import json
import numpy as np
import pandas as pd
import spacy
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity

# Load a pre-trained spaCy model
nlp = spacy.load('en_core_web_md')

# Define a function to extract named entities from a text document
def extract_entities(text):
    doc = nlp(text)
    entities = [ent.text for ent in doc.ents if ent.label_ == '']
    return entities

# Load the JSON data from a file
with open('leagues.json', 'r') as f:
    data = json.load(f)

# Extract the "camp name" field from each object
camp_names = [obj.get('jogo', '') for obj in data["jogos"]]

# Extract named entities from the camp names
entities = [extract_entities(name) for name in camp_names]

# Create a matrix of entity similarities using cosine similarity
similarity_matrix = cosine_similarity(np.vstack(entities))

# Apply a clustering algorithm to the similarity matrix
kmeans = KMeans(n_clusters=10)
kmeans.fit(similarity_matrix)

# Assign cluster labels to each entity
entity_labels = kmeans.labels_

# Group entities by cluster label
entity_clusters = {}
for i, label in enumerate(entity_labels):
    if label not in entity_clusters:
        entity_clusters[label] = []
    entity_clusters[label].append(entities[i])

# Print the clusters of similar camp names
for cluster in entity_clusters.values():
    print(cluster)

import numpy as np
from sentence_transformers import SentenceTransformer
import pandas as pd
model = SentenceTransformer("all-mpnet-base-v2")
def description_embeddings(data = pd.read_csv("games.csv")):
    descriptions = data["Description"].fillna("").astype(str).tolist()
    embeddings = model.encode(descriptions)
    return np.array(embeddings)
print(description_embeddings().shape)
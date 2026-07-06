import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from preprocessing import tag_encoding
import pandas as pd
def cosine_matrix():
    encoded_tags = tag_encoding()
    game_cosine = cosine_similarity(encoded_tags, encoded_tags)
    return game_cosine

def get_gamesimilarity(name):
    name = name.lower().strip().replace("-", " ")
    found = False
    data = pd.read_csv("games.csv")     
    matrix = cosine_matrix()
    similarity_list = []
    for i in range(len(data)):
        if data["Name"][i].lower().strip().replace("-", " ") == name:
            found = True
            for index, score in enumerate(matrix[i]):
                if index == i:
                    continue          
                similarity_list.append((data["Name"][index], score))
            break
    if not found:
        return "Game not found"
    else:
        sorted_list = sorted(similarity_list, key = lambda item: item[1], reverse = True)
        return sorted_list

def game_weights():
    data = pd.read_csv("games.csv")
    weights = []
    for i in range(len(data)):
        weights.append(data["Rating"][i]-6)
    return weights

def taste_vector():
    tags = tag_encoding()
    weights = game_weights()
    encoded_weights = []
    for i in range(len(tags)):
        p = np.array(tags[i])
        q = p*weights[i]
        encoded_weights.append(q)
    weighted_array = np.sum(encoded_weights, axis = 0)
    return weighted_array


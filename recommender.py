import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.linear_model import Ridge
from preprocessing import *
import pandas as pd
from sklearn.linear_model import Ridge
def cosine_matrix(data):
    encoded_tags = tag_encoding(data)
    game_cosine = cosine_similarity(encoded_tags, encoded_tags)
    return game_cosine

def get_gamesimilarity(name, data):
    name = name.lower().strip().replace("-", " ")
    found = False
    matrix = cosine_matrix(data)
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

def game_weights(data):
    weights = []
    for i in range(len(data)):
        weights.append(data["Rating"][i]-6)
    return weights

def taste_vector(data, exclude_index = None):
    tags = tag_encoding(data)
    weights = game_weights(data)
    encoded_weights = []
    for i in range(len(tags)):
        if i != exclude_index:
            p = np.array(tags[i])
            q = p*weights[i]
            encoded_weights.append(q)
    weighted_array = np.sum(encoded_weights, axis = 0)
    return weighted_array

def smoothed_score_vector(data, m=5, baseline=0, exclude_index=None):
    from preprocessing import filter_tags, preprocess_data
    taste = taste_vector(data, exclude_index=exclude_index)
    tags = filter_tags(data)
    tag_counts, _ = preprocess_data(data)
    if exclude_index is not None:
        excluded_tags = tag_encoding(data)[exclude_index]
        for i in range(len(tags)):
            tag = tags[i]
            tag_counts[tag] = tag_counts[tag] - excluded_tags[i]
    tag_dict = {
        "Tags": tags,
        "Weights": taste
    }
    df = pd.DataFrame(tag_dict)
    df["Frequency"] = df["Tags"].map(tag_counts)
    smoothed_array = []
    for i in range(len(df)):
        score = (
            df["Weights"].iloc[i] + (baseline * m)
        ) / (m + df["Frequency"].iloc[i])
        smoothed_array.append(score)
    return smoothed_array

def leave_one_out_scores(data):
    tags = tag_encoding(data)
    scores = []

    for i in range(len(tags)):
        game_vector = tags[i]
        tag_count = np.sum(game_vector)

        if tag_count != 0:
            p = np.array(
                smoothed_score_vector(data, exclude_index=i)
            ) * game_vector

            q = np.sum(p) / tag_count
        else:
            q = np.nan

        scores.append(q)

    return scores


def leave_one_out_ridge(X, y):
    predictions = []
    for i in range(len(X)):
        mask = np.arange(len(X)) != i
        X_train = X[mask]
        y_train = y[mask]
        X_test = X[i].reshape(1, -1)
        model = Ridge(alpha=1.0)
        model.fit(X_train, y_train)
        prediction = model.predict(X_test)
        p = prediction[0]
        predictions.append(p)
    return predictions



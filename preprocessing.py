import pandas as pd
import csv
TAG_ALIASES = {
    "role playing": "rpg",
    "role playing game": "rpg",
    "action rpg" : "rpg",
    "3rd person": "third person",
    "3rd person perspective": "third person",
}

def normalise_tag(word):
    new_word = word.lower().strip().replace("-", " ")
    if new_word in TAG_ALIASES:
        new_word = TAG_ALIASES[new_word]
    return new_word

def preprocess_data():
    data = pd.read_csv("games.csv") 
    normalised_tags = []
    tag_counts = {}
    for i in range(len(data)):
        if pd.isna(data["Tags"][i]):
            continue
        else:
            indiv_tag = data["Tags"][i].split("|")
            for tag in indiv_tag:
                tag = normalise_tag(tag)
                normalised_tags.append(tag)
                if tag in tag_counts:
                    tag_counts[tag] = tag_counts[tag] + 1                    
                else:
                    tag_counts[tag] = 1
    return tag_counts, normalised_tags

q,m = preprocess_data()
sorted_genre = sorted(q.items(), key = lambda item: item[1], reverse =  True)
print(sorted_genre[:20])


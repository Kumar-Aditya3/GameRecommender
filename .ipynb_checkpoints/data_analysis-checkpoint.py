import pandas as pd
import requests
import csv
def load_data():
    data = pd.read_csv("games.csv")
    tag_counts = {}
    genre_counts = {}
    for i in range(len(data)):
        if pd.isna(data["Tags"][i]):
            continue
        else:
            indiv_tag = data["Tags"][i].split("|")
            for tag in indiv_tag:
                if tag in tag_counts:
                    tag_counts[tag] = tag_counts[tag] + 1                    
                else:
                    tag_counts[tag] = 1
        if pd.isna(data["Genres"][i]):
            continue
        else:
            indiv_genre = data["Genres"][i].split("|")
            for genre in indiv_genre: 
                if genre in genre_counts:
                    genre_counts[genre] = genre_counts[genre] + 1                    
                else:
                    genre_counts[genre] = 1
    sorted_tags = sorted(tag_counts.items(), key = lambda item: item[1], reverse =  True)
    sorted_genre = sorted(genre_counts.items(), key = lambda item: item[1], reverse =  True)
    print(sorted_tags[:20])
    print(sorted_genre[:20])

load_data()
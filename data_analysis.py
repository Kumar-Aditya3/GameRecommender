import pandas as pd
import requests
import csv
def load_data():
    data = pd.read_csv("games.csv")
    tag_counts = {}
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
    print(tag_counts)



load_data()
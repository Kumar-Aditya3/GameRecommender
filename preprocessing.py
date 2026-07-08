import pandas as pd
import numpy as np
TAG_ALIASES = {
    # RPG aliases
    "role playing": "rpg",
    "role playing game": "rpg",
    # Perspective
    "3rd person": "third person",
    "3rd person perspective": "third person",
    # Shooter
    "fps": "first person shooter",

    # Multiplayer
    "online multiplayer": "multiplayer",

    # Co-op
    "cooperative": "co op",
    "online co op": "co op",

    # PvP
    "online pvp": "pvp",

}

unwanted_tags = [
    "steam trading cards",
    "steam achievements",
    "full controller support",
    "masterpiece"
]

def normalise_tag(word):
    new_word = word.lower().strip().replace("-", " ")
    if new_word in TAG_ALIASES:
        new_word = TAG_ALIASES[new_word]
    return new_word

def preprocess_data(data = pd.read_csv("games.csv")):
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


def preprocess_developers(data = pd.read_csv("games.csv")):
    developer_counts = {}

    for i in range(len(data)):
        if pd.isna(data["Developers"][i]):
            continue

        indiv_developer = set(data["Developers"][i].split("|"))
        for developer in indiv_developer:
            developer = developer.strip()
            if not developer:
                continue
            if developer in developer_counts:
                developer_counts[developer] = developer_counts[developer] + 1
            else:
                developer_counts[developer] = 1

    return developer_counts

def filter_developers(data = pd.read_csv("games.csv")):
    counts = preprocess_developers(data)
    filtered_devs = []
    for dev in counts:
        if counts[dev] >1:
            filtered_devs.append(dev)
    return filtered_devs

def filter_tags(data = pd.read_csv("games.csv")):
    tag_counts, normalised_tags = preprocess_data(data)
    useful_tags= [
        tag for tag, count in tag_counts.items()
        if count > 2 and tag not in unwanted_tags
    ]
    return useful_tags


def normalise_game_tag(data = pd.read_csv("games.csv")):
    list_games_tags = []
    for i in range(len(data)):
        game_tags = []
        if not pd.isna(data["Tags"][i]):
            game = data["Tags"][i].split("|")
            for tag in game:
                game_tags.append(normalise_tag(tag))
                game_tags = list(dict.fromkeys(game_tags))
        list_games_tags.append(game_tags)
    return list_games_tags

def filter_tagbase(data = pd.read_csv("games.csv")):
    filtered_game_tags = []
    all_game_tags = normalise_game_tag(data)
    useful_tags = filter_tags(data)
    for game_tag in all_game_tags:
        filtered_tags = []
        for tag in game_tag:
            if tag in useful_tags:
                filtered_tags.append(tag)
        filtered_game_tags.append(filtered_tags)
    return filtered_game_tags

def tag_encoding(data = pd.read_csv("games.csv")):
    data1 = filter_tagbase(data)
    filteredtags = filter_tags(data)
    encodedgames = []
    for i in range(len(data1)):
        game_encoding = []
        for tag in filteredtags:
            if tag in data1[i]:
                game_encoding.append(1)
            else:
                game_encoding.append(0)
        encodedgames.append(game_encoding)
    return encodedgames

def game_developers(data = pd.read_csv("games.csv")):
    gamedev_data = []
    for i in range(len(data)):
        dev_list = data["Developers"][i]
        indivgame_dev = []
        if not pd.isna(dev_list): 
            indiv_devs = dev_list.split("|")
            for developer in indiv_devs:
                    developer = developer.strip()
                    if not developer:
                        continue
                    else:
                        if developer not in indivgame_dev:
                            indivgame_dev.append(developer)
        gamedev_data.append(indivgame_dev)
    return gamedev_data

def filter_devbase(data = pd.read_csv("games.csv")):
    gamedev_data = game_developers(data)
    filtered_devs = filter_developers(data)
    filtered_gamedev = []
    for i in range(len(gamedev_data)):
        indivgame_filterdev = []
        for developer in gamedev_data[i]:
            if developer in filtered_devs:
                indivgame_filterdev.append(developer)
        filtered_gamedev.append(indivgame_filterdev)
    return filtered_gamedev

def dev_encoding(data = pd.read_csv("games.csv")):
    data_devs = filter_developers(data)
    filteredevs = filter_devbase(data)
    encodedgames = []
    for i in range(len(filteredevs)):
        game_encoding = []
        for devs in data_devs:
            if devs in filteredevs[i]:
                game_encoding.append(1)
            else:
                game_encoding.append(0)
        encodedgames.append(game_encoding)
    return encodedgames

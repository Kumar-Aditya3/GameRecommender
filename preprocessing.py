import pandas as pd
import csv
TAG_ALIASES = {
    # RPG aliases
    "role playing": "rpg",
    "role playing game": "rpg",
    "role-playing": "rpg",

    # Perspective
    "3rd person": "third person",
    "3rd-person": "third person",
    "3rd person perspective": "third person",
    "3rd-person perspective": "third person",
    "first-person": "first person",

    # Shooter
    "fps": "first person shooter",
    "third-person shooter": "third person shooter",

    # Multiplayer
    "online multiplayer": "multiplayer",

    # Co-op
    "cooperative": "co-op",
    "online co-op": "co-op",

    # PvP
    "online pvp": "pvp",

    # Formatting aliases
    "action-adventure": "action adventure",
    "free-to-play": "free to play",
    "sci-fi": "sci fi",
    "souls-like": "soulslike",
    "post-apocalyptic": "post apocalyptic",
    "fast-paced": "fast paced",
    "team-based": "team based",
    "turn-based": "turn based",
    "party-based rpg": "party based rpg",
    "real-time strategy": "real time strategy",
    "steam-trading-cards": "steam trading cards",
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


def filter_tags():
    tag_counts, normalised_tags = preprocess_data()
    useful_tags= [
        tag for tag, count in tag_counts.items()
        if count > 2
    ]
    return useful_tags


def normalise_game_tag():
    games = pd.read_csv("games.csv")
    list_games_tags = []
    for i in range(len(games)):
        game_tags = []
        if not pd.isna(games["Tags"][i]):
            game = games["Tags"][i].split("|")
            for tag in game:
                game_tags.append(normalise_tag(tag))
                game_tags = list(dict.fromkeys(game_tags))
        list_games_tags.append(game_tags)
    return list_games_tags

def filter_tagbase():
    filtered_game_tags = []
    all_game_tags = normalise_game_tag()
    useful_tags =  filter_tags()
    for game_tag in all_game_tags:
        filtered_tags = []
        for tag in game_tag:
            if tag in useful_tags:
                filtered_tags.append(tag)
        filtered_game_tags.append(filtered_tags)
    return filtered_game_tags

def tag_encoding():
    data = filter_tagbase()
    filteredtags = filter_tags()
    encodedgames = []
    for i in range(len(data)):
        game_encoding = []
        for tag in filteredtags:
            if tag in data[i]:
                game_encoding.append(1)
            else:
                game_encoding.append(0)
        encodedgames.append(game_encoding)
    return encodedgames
encoded_games = tag_encoding()

print(len(encoded_games))
print(len(encoded_games[2]))
print(encoded_games[3])




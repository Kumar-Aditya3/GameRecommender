
TEST_MODE = False
if TEST_MODE == True:
    game = "Cyberpunk 2077"
else:
    game = input("Enter a game name: ")
def gamedata(game):
    import os
    from dotenv import load_dotenv
    import requests
    url = "https://api.rawg.io/api/games"
    load_dotenv()
    api =  os.getenv("RAWGAPI")

    params = {
        "key": api,
        "search": game
    }   
    data = requests.get(url, params=params).json()
    print("Which of the following games match yours?")
    number_of_games = len(data["results"])
    if number_of_games == 0:
        print("No games were found")
        return
    else:
        if TEST_MODE == True:
            i = 1
        else:
            for i in range(min(5, number_of_games)):
                print("Game", i+1, ":", data["results"][i]["name"])
            while True:
                    try:
                        i = int(input("Please enter the correct serial number: "))
                        if i  > min(5, number_of_games) or i < 1:
                            print("Please enter a value in range: ")
                        else:
                            break
                    except ValueError:
                        print("That is not a Number")
        i = i - 1
        genres = []
        tags = []
        g1 = data["results"][i] 
        for genre in g1["genres"]:
            genres.append(genre["name"])  
        for tag in g1["tags"]:
            if tag["language"] == "eng":
                tags.append(tag["name"])
        if TEST_MODE == True:
            rating = 10
        else: 
            while True:
                try:
                    rating = int(input("Please enter your rating for the game out of 10: "))
                    if rating  > 10 or rating < 0:
                        print("Please enter a value in range: ")
                    else:
                        break
                except ValueError:
                    print("That is not a Number")
        info = {"Name": data["results"][i]["name"], "Genres": genres, "Tags": tags, "Rating": rating}
        return info
info = (gamedata(game))
def savegame(info):
    import csv
    import os
    info["Genres"] = "|".join(info["Genres"])
    info["Tags"] = "|".join(info["Tags"])
    file_exists = os.path.exists("games.csv")
    if file_exists:
        with open("games.csv","r",newline = "", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Name"] == info["Name"]:
                    print("MATCH FOUND")
                    return
    fieldnames = ["Name", "Genres", "Tags","Rating"]
    with open("games.csv","a",newline = "", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames = fieldnames)
        if file_exists == False:
            writer.writeheader()
        writer.writerow(info)
print(savegame(info))
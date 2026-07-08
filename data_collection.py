TEST_MODE = False
def savegame(info, data):
    import csv
    import os

    if data is not None:
        existing_names = set(data["Name"].astype(str))
        if info["Name"] in existing_names:
            print("MATCH FOUND")
            return

    info["Genres"] = "|".join(info["Genres"])
    info["Tags"] = "|".join(info["Tags"])
    info["Developers"] = "|".join(info["Developers"])
    fieldnames = ["Name", "Genres", "Tags", "Developers", "Description", "Rating"]
    file_exists = os.path.exists("games.csv")
    with open("games.csv","a",newline = "", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames = fieldnames)
        if file_exists == False:
            writer.writeheader()
        writer.writerow(info)
        
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
        game_id = g1["id"]
        detail_url = f"https://api.rawg.io/api/games/{game_id}"
        detail_data = requests.get(detail_url, params={"key": api}).json()
        description = detail_data.get("description_raw", "")
        developers = []

        for developer in detail_data.get("developers", []):
            developers.append(developer["name"])
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
        info = {
            "Name": data["results"][i]["name"],
            "Genres": genres,
            "Tags": tags,
            "Developers": developers,
            "Description": description,
            "Rating": rating,
        }
        return info


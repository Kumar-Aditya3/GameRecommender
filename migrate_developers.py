import os

import pandas as pd
import requests
from dotenv import load_dotenv


def normalise_name(name):
    return name.lower().strip().replace("-", " ")


def fetch_developers(game_name, api_key):
    url = "https://api.rawg.io/api/games"
    params = {"key": api_key, "search": game_name}
    search_data = requests.get(url, params=params).json()
    results = search_data.get("results", [])

    if not results:
        return []

    target_name = normalise_name(game_name)
    selected_game = results[0]
    for result in results:
        if normalise_name(result["name"]) == target_name:
            selected_game = result
            break

    detail_url = f"https://api.rawg.io/api/games/{selected_game['id']}"
    detail_data = requests.get(detail_url, params={"key": api_key}).json()

    developers = []
    for developer in detail_data.get("developers", []):
        developers.append(developer["name"])

    description = detail_data.get("description_raw", "")

    return developers, description


def migrate_developers(games):
    load_dotenv()
    api_key = os.getenv("RAWGAPI")
    if not api_key:
        raise ValueError("RAWGAPI is not set in the environment.")

    if "Developers" not in games.columns:
        games["Developers"] = ""
    if "Description" not in games.columns:
        games["Description"] = ""

    developer_column = []
    description_column = []
    for _, row in games.iterrows():
        current_developers = row.get("Developers", "")
        current_description = row.get("Description", "")
        has_developers = pd.notna(current_developers) and str(current_developers).strip()
        has_description = pd.notna(current_description) and str(current_description).strip()

        if has_developers and has_description:
            developer_column.append(current_developers)
            description_column.append(current_description)
            continue

        developers, description = fetch_developers(row["Name"], api_key)

        if has_developers:
            developer_column.append(current_developers)
        else:
            developer_column.append("|".join(developers))

        if has_description:
            description_column.append(current_description)
        else:
            description_column.append(description)

    games["Developers"] = developer_column
    games["Description"] = description_column
    games = games[["Name", "Genres", "Tags", "Developers", "Description", "Rating"]]
    games.to_csv("games.csv", index=False)


if __name__ == "__main__":
    migrate_developers(pd.read_csv("games.csv"))

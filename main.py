import pandas as pd

from data_collection import savegame 
from data_collection import gamedata
TEST_MODE = False
data = pd.read_csv("games.csv")
if TEST_MODE == True:
    game = "Cyberpunk 2077"
else:
    game = input("Enter a game name: ")

info = gamedata(game)
if info is not None:
    savegame(info, data)


from data_collection import savegame 
from data_collection import gamedata
TEST_MODE = False
if TEST_MODE == True:
    game = "Cyberpunk 2077"
else:
    game = input("Enter a game name: ")

info = (gamedata(game))

print(savegame(info))

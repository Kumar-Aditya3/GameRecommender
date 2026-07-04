import os
from dotenv import load_dotenv
import requests
url = "https://api.rawg.io/api/games"
load_dotenv()
api =  os.getenv("RAWGAPI")
print(api)

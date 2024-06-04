from src.models.database import Database
from src.models.session import Session

import json 

db = Database()
db.setup()

s = Session("matis@datarockstars.ai", "matis")
s.signin()

data = {      
    "email" : ""
}

with open("session.json", 'w') as outfile:
    json.dump(data, outfile)
import json

with open("config.json", "r") as f:
    data = json.load(f)
    token = data["token"]
    db_path = data["db_path"]
    f.close()


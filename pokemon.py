"""
Pokemon ETL - Extract + Store stage
 
Pulls Pokemon data from PokeAPI and stores it in MongoDB, demonstrating
full CRUD (Create, Read, Update, Delete).
"""
 
import requests
from pymongo import MongoClient
 
# ---- CONFIG ----
MONGODB_URI = "mongodb://63.183.2.26:27017"
DB_NAME = "pokemon_etl"
COLLECTION_NAME = "pokemon"
 
 
# ---------------------------------------------------------------------------
# EXTRACT
# ---------------------------------------------------------------------------
def get_pokemon_data(name: str) -> dict:
    """Fetch full detail for a single Pokemon and shape it into a clean dict."""
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}")
    data = response.json()
 
    return {
        "pokemon_id": data["id"],
        "name": data["name"],
        "height": data["height"],
        "weight": data["weight"],
        "types": [entry["type"]["name"] for entry in data["types"]],
        "abilities": [entry["ability"]["name"] for entry in data["abilities"]],
        "stats": {entry["stat"]["name"]: entry["base_stat"] for entry in data["stats"]},
    }
 
 
def get_pokemon_names(limit: int = 10) -> list[str]:
    """Fetch a plain list of Pokemon names from the API."""
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon?limit={limit}")
    data = response.json()
    return [entry["name"] for entry in data["results"]]
 
 
def get_many_pokemon(limit: int = 10) -> list[dict]:
    """Fetch full detail for the first `limit` Pokemon."""
    names = get_pokemon_names(limit=limit)
    return [get_pokemon_data(name) for name in names]
 
 
# ---------------------------------------------------------------------------
# MAIN - extract a batch, then demo full CRUD against MongoDB
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # --- Extract ---
    all_pokemon = get_many_pokemon(limit=10)
    print(f"Extracted {len(all_pokemon)} Pokemon.")
    print(all_pokemon[0])
 
    # --- Connect to MongoDB ---
    client = MongoClient(MONGODB_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    print("Databases visible:", client.list_database_names())
 
    # --- Create ---
    pokemon_doc = get_pokemon_data("bulbasaur")
    collection.insert_one(pokemon_doc)
    print("Inserted:", collection.find_one({"name": "bulbasaur"}))
 
    # --- Update ---
    collection.update_one({"name": "bulbasaur"}, {"$set": {"caught": True}})
    print("After update:", collection.find_one({"name": "bulbasaur"}))
 
    # --- Delete ---
    # delete_many (not delete_one) to catch any duplicates from repeated test runs
    collection.delete_many({"name": "bulbasaur"})
    print("After delete:", collection.find_one({"name": "bulbasaur"}))


'''
Json schema for the Pokemon document in MongoDB:

{
    "pokemon_id": int,
    "name": str,
    "height": int,
    "weight": int,
    "types": list[str],
    "abilities": list[str],
    "stats": dict[str, int],
    "caught": bool (optional)
}
'''


from bson import ObjectId

def convert_objectid(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
import json

docs = list(collection.find({}))
print(json.dumps(docs, default=convert_objectid))


with open("pokemon_export.json", "w") as f:
    json.dump(docs, f, indent=2, default=convert_objectid)

print("Exported to pokemon_export.json")


#Check if the document was exported correctly
with open("pokemon_export.json") as f:
    print(f.read())



'''' NOw for the Boto 3 upload to s3 bucket'''


import boto3

s3 = boto3.client("s3", region_name="eu-central-1")

s3.upload_file(
    "pokemon_export.json",
    "se-data-with-ai-etl-project",
    "harry-stevens/pokemon_export.json"
)

print("Uploaded to S3")
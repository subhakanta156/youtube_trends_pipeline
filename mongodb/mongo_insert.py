import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_ingestion.config import COUNTRIES

from mongo_config import db


import json



def insert_data_from_json():
    for country, code in COUNTRIES.items():
        file_path = f"data_ingestion/data/raw/{country.lower()}/trending_{country.lower()}.json"


        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    db[f"{country.lower()}_trending"].insert_many(data)
                else:
                    db[f"{country.lower()}_trending"].insert_one(data)
            print(f" Inserted data for {country}")
        else:
            print(f" File not found: {file_path}")

if __name__ == "__main__":
    insert_data_from_json()

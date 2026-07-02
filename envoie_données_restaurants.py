import pandas as pd
import certifi
from pymongo import MongoClient
import datetime
import random


uri= "mongodb+srv://Matt:Matthias@cluster0.mnr1sl1.mongodb.net/"
client = MongoClient(uri, tlsCAFile=certifi.where())
db = client["talabat_db"]

# Lecture du CSV
df = pd.read_csv("talabat_enhanced_orders.csv")

# Liste de cuisines pour enrichir le NoSQL de manière réaliste
cuisines = ["Italien", "Burgers", "Asiatique", "Libanais", "Indien", "Fast-Food", "Salades"]

# On groupe par Restaurant_ID pour n'avoir que les uniques
unique_restos = df.groupby("Restaurant_ID").first().reset_index()

restaurants_list = []
for index, row in unique_restos.iterrows():
    resto_id = int(row["Restaurant_ID"])
    
    doc_restaurant = {
        "_id": resto_id,
        "nom": f"Restaurant {resto_id}",
        "type_cuisine": random.choice(cuisines),
        "location": {
            "type": "Point",
            "coordinates": [float(row["Restaurant_Lon"]), float(row["Restaurant_Lat"])]
        },
        "ville_principale": row["City"]
    }
    restaurants_list.append(doc_restaurant)

# Insertion dans la collection 'restaurants'
if restaurants_list:
    db.restaurants.delete_many({}) # Optionnel : nettoie la collection avant
    db.restaurants.insert_many(restaurants_list)
    print(f"Succès : {len(restaurants_list)} restaurants uniques importés !")
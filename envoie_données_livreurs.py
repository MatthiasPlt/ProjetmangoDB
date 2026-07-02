import pandas as pd
import certifi
from pymongo import MongoClient
import datetime
import random


uri= "mongodb+srv://<username>:<password>@cluster0.mnr1sl1.mongodb.net/"
client = MongoClient(uri, tlsCAFile=certifi.where())
db = client["talabat_db"]

# Lecture du CSV
df = pd.read_csv("talabat_enhanced_orders.csv")

# Types de pannes pour l'historique de maintenance
pannes = ["Crevaison", "Problème Batterie", "Révision standard", "Freins usés"]

# On groupe par Driver_ID pour n'avoir que les livreurs uniques
unique_drivers = df.groupby("Driver_ID").first().reset_index()

livreurs_list = []
for index, row in unique_drivers.iterrows():
    driver_id = int(row["Driver_ID"])
    
    # Génération d'un historique de maintenance imbriqué (pure logique NoSQL)
    historique_maintenance = []
    nb_interventions = random.randint(0, 2) # 0 à 2 interventions par véhicule
    for i in range(nb_interventions):
        historique_maintenance.append({
            "date_intervention": datetime.datetime(2025, random.randint(1, 12), random.randint(1, 28)),
            "type_panne": random.choice(pannes),
            "cout_reparation": round(random.uniform(20.0, 150.0), 2)
        })

    doc_livreur = {
        "_id": driver_id,
        "nom_livreur": f"Livreur_{driver_id}",
        "vehicule": row["Driver_Vehicle"],
        "statut_global": row["Driver_Availability"],
        "maintenance": historique_maintenance
    }
    livreurs_list.append(doc_livreur)

# Insertion dans la collection 'livreurs'
if livreurs_list:
    db.livreurs.delete_many({}) # Optionnel : nettoie la collection avant
    db.livreurs.insert_many(livreurs_list)
    print(f"Succès : {len(livreurs_list)} livreurs uniques importés !")
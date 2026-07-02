import pandas as pd
import certifi
from pymongo import MongoClient
import datetime


uri= "mongodb+srv://<username>:<password>@cluster0.mnr1sl1.mongodb.net/"
client = MongoClient(uri, tlsCAFile=certifi.where())
db = client["talabat_db"]


df = pd.read_csv("talabat_enhanced_orders.csv")


commandes_list = []
for index, row in df.iterrows():
 
    order_time = datetime.datetime.strptime(row["Order_Time"], "%Y-%m-%d %H:%M:%S")
    delivery_time = datetime.datetime.strptime(row["Delivery_Time"], "%Y-%m-%d %H:%M:%S")

  
    commande = {
        "_id": int(row["Order_ID"]),
        "user_id": row["User_ID"],
        "restaurant": {
            "id": int(row["Restaurant_ID"]),
            "location": { "type": "Point", "coordinates": [row["Restaurant_Lon"], row["Restaurant_Lat"]] }
        },
        "customer": {
            "city": row["City"],
            "location": { "type": "Point", "coordinates": [row["Customer_Lon"], row["Customer_Lat"]] }
        },
        "driver": {
            "id": int(row["Driver_ID"]),
            "vehicle": row["Driver_Vehicle"],
            "availability": row["Driver_Availability"],
            "location": { "type": "Point", "coordinates": [row["Driver_Lon"], row["Driver_Lat"]] }
        },
        "item": {
            "name": row["Item_Name"],
            "quantity": int(row["Quantity"])
        },
        "financial": {
            "total_price": float(row["Total_Price"]),
            "payment_method": row["Payment_Method"]
        },
        "logistics": {
            "order_status": row["Order_Status"],
            "duration_minutes": int(row["Delivery_Duration_Minutes"]),
            "distance_km": float(row["Delivery_Distance_km"]),
            "traffic_level": row["Traffic_Level"]
        },
        "timestamps": {
            "order_time": order_time,
            "delivery_time": delivery_time
        }
    }
    commandes_list.append(commande)

    # Insertion par paquets pour aller plus vite (Bulk insert)
    if len(commandes_list) == 5000:
        db.commandes.insert_many(commandes_list)
        commandes_list = []

if commandes_list:
    db.commandes.insert_many(commandes_list)

print("Données importées avec succès dans MongoDB !")
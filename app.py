from flask import Flask, jsonify
from pymongo import MongoClient
import certifi

app = Flask(__name__)

uri= "mongodb+srv://Matt:Matthias@cluster0.mnr1sl1.mongodb.net/"
client = MongoClient(uri, tlsCAFile=certifi.where())
db = client["talabat_db"]

@app.route('/api/kpi/revenue-by-city', methods=['GET'])
def get_revenue_by_city():
    """1. Chiffre d'affaires total et panier moyen par ville"""
    pipeline = [
        {
            "$group": {
                "_id": "$customer.city",
                "chiffre_affaires": { "$sum": "$financial.total_price" },
                "panier_moyen": { "$avg": "$financial.total_price" },
                "nombre_commandes": { "$sum": 1 }
            }
        },
        { "$sort": { "chiffre_affaires": -1 } }
    ]
    result = list(db.commandes.aggregate(pipeline))
    return jsonify(result)


@app.route('/api/kpi/traffic-impact', methods=['GET'])
def get_traffic_impact():
    """2. Impact du trafic sur le temps de livraison moyen"""
    pipeline = [
        {
            "$group": {
                "_id": "$logistics.traffic_level",
                "duree_moyenne_minutes": { "$avg": "$logistics.duration_minutes" }
            }
        },
        { "$sort": { "duree_moyenne_minutes": 1 } }
    ]
    result = list(db.commandes.aggregate(pipeline))
    return jsonify(result)


@app.route('/api/kpi/best-vehicles-high-traffic', methods=['GET'])
def get_best_vehicles():
    """3. Véhicule le plus rapide en cas de trafic intense (High)"""
    pipeline = [
        { "$match": { "logistics.traffic_level": "High" } },
        {
            "$group": {
                "_id": "$driver.vehicle",
                "temps_moyen_minutes": { "$avg": "$logistics.duration_minutes" }
            }
        },
        { "$sort": { "temps_moyen_minutes": 1 } }
    ]
    result = list(db.commandes.aggregate(pipeline))
    return jsonify(result)


@app.route('/api/kpi/top-items', methods=['GET'])
def get_top_items():
    """4. Top 5 des articles les plus commandés"""
    pipeline = [
        {
            "$group": {
                "_id": "$item.name",
                "quantite_totale": { "$sum": "$item.quantity" }
            }
        },
        { "$sort": { "quantite_totale": -1 } },
        { "$limit": 5 }
    ]
    result = list(db.commandes.aggregate(pipeline))
    return jsonify(result)


@app.route('/api/kpi/maintenance-costs', methods=['GET'])
def get_maintenance_costs():
    """5. Coût total de maintenance par type de véhicule (Collection livreurs)"""
    pipeline = [
        { "$unwind": "$maintenance" },
        {
            "$group": {
                "_id": "$vehicule",
                "cout_total_reparations": { "$sum": "$maintenance.cout_reparation" },
                "nombre_interventions": { "$sum": 1 }
            }
        },
        { "$sort": { "cout_total_reparations": -1 } }
    ]
    result = list(db.livreurs.aggregate(pipeline))
    return jsonify(result)


@app.route('/api/kpi/hourly-activity', methods=['GET'])
def get_hourly_activity():
    """6. Volume de commandes par heure de la journée"""
    pipeline = [
        {
            "$group": {
                "_id": { "$hour": "$timestamps.order_time" },
                "total_commandes": { "$sum": 1 }
            }
        },
        { "$sort": { "_id": 1 } }
    ]
    result = list(db.commandes.aggregate(pipeline))
    return jsonify(result)

@app.route('/api/kpi/global-stats', methods=['GET'])
def get_global_stats():
    """Compteurs globaux : CA total, Total commandes, Distance totale"""
    pipeline = [
        {
            "$group": {
                "_id": None,
                "total_ca": { "$sum": "$financial.total_price" },
                "total_commandes": { "$sum": 1 },
                "total_distance": { "$sum": "$logistics.distance_km" }
            }
        }
    ]
    result = list(db.commandes.aggregate(pipeline))
    if result:
        return jsonify(result[0])
    return jsonify({"total_ca": 0, "total_commandes": 0, "total_distance": 0})


if __name__ == '__main__':
    # Lancement du serveur API Flask sur le port 5000
    print("Lancement de l'API Talabat Logistics...")
    app.run(debug=True, port=5000)
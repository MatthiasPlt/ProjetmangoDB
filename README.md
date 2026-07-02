

## Architecture du Projet

Le projet est découpé en plusieurs couches distinctes :
1. **Base de données (MongoDB) :** Stockage des collections `commandes`, `restaurants` et `livreurs`.
2. **Backend (Flask) :** API REST exécutant des requêtes d'agrégation NoSQL complexes et distribuant les données au format JSON.
3. **Frontend (Streamlit) :** Tableau de bord interactif et dynamique consommant l'API pour afficher des graphiques métiers.

---

##  Guide d'Installation et de Lancement

Suivez ces étapes dans l'ordre pour exécuter le projet parfaitement sur votre machine.

### Étape 1 : Cloner le projet et installer les dépendances
Ouvrez votre terminal dans le dossier du projet et installez les modules Python requis :
```bash
pip install flask pymongo streamlit requests pandas 
python envoie_données_commandes.py
python envoie_données_livreurs.py
python envoie_données_restaurants.py    
python app.py
# puis dans un autre terminal 
python -m streamlit run dashboard.py

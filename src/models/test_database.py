import time
import sys #pour aller chercher les classes où il faut
sys.path.append('./src/models')
from database import Database  # Remplacer éventuellement par le chemin réel de la classe Database si changement stockage du test check_directory

db = Database()
try:
    # Supprime la table `logs` et la recrée
    db.execute("DROP TABLE IF EXISTS logs")
    db.execute("CREATE TABLE logs (id INTEGER PRIMARY KEY UNIQUE, uid INTEGER, action VARCHAR, value VARCHAR)")

    # Test d'insertion
    query = "INSERT INTO logs (uid, action, value) VALUES (?, ?, ?)"
    params = (0, "logged", str(int(time.time())))
    db.execute(query, params)
    print("Données insérées avec succès.")
except Exception as e:
    print(f"Erreur : {e}")
finally:
    db.close()

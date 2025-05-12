import hashlib
from src.models.database import Database
import time 
import json

class Session:

    def __init__(self, email, password) -> None:
        self.logged : bool = False
        self.email : str =  email
        self._password : str = password

    def hash(self) -> str: #fonction de codage 
        return hashlib.sha256(self._password.encode(encoding="utf-32")).hexdigest()

    def exist(self) -> bool: #fonction de contrôle de l'existence dans DB sur la base de l'info codée
        db = Database()
        query = "SELECT uid FROM users WHERE password=? AND email=?" #formalisation requête avec placeholder pour sécurité injection SQL
        res = db.execute(query, (self.hash(), self.email))  # utilisation des paramètres
        return res.fetchone() is not None

    def getUID(self):
        db = Database()
        query = "SELECT uid FROM users WHERE password=? AND email=?" #via string avec placeholders
        res = db.execute(query, (self.hash(), self.email))  # utilisation des paramètres
        row = res.fetchone() #ajout code gestion de l'exception si utilisateur non trouvé
        if row : 
            return row[0] # retourne le UID tel qu'il existe
        else : 
            return None

    # conservation de la trace de connexion de l'utilisateur et l'enregistre dans la table logs
    def login(self):
        uid = self.getUID()  # Récupère l'UID réel
    
        if uid is not None:
            db = Database()
            query = "INSERT INTO logs (uid, action, value) VALUES (?, ?, ?)" # insertion dans les logs string avec placeholders
            db.execute(f"INSERT INTO logs (uid, action, value) VALUES ( {self.getUID()} , \"logged\", '{int(time.time())}')")
            db.execute(query, (self.getUID(), "logged", int(time.time())))  # utilisation des paramètres sécurisés
            db.commit()
            self.logged = True
        else:
            print("Cet utilisateur n'existe pas dans la base") #contrôle terminal

    def signin(self):
        if not self.exist():
            db = Database()
            query = "INSERT INTO users (email, password) VALUES (?, ?)" # avec les placeholders
            db.execute(query, (self.email, self.hash()))  # utilisation des paramètres
            db.commit()
            print("l'utilisateur est mainteant créé")
            return True
        else:
            print("Utilisateur déjà dans la DB")
            return False

    def persist(self):
        """ sauvegarde email dans le fichier JSON session.json"""
        data = {
                "email" : self.email #stockage de l'email du user en ligne
        }
        with open("session.json", 'w') as outfile: #ouvre le fichier en mode write
            json.dump(data, outfile) #écrit l'objet json  dans le fichier

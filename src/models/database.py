import sqlite3

class Database :
#    def __init__(self) -> None:
#        self.__db = sqlite3.connect("project.db")

    def __init__(self):
        """
        Initialise la connexion à la base de données SQLite.
        """
        try:
            #self.connection = sqlite3.connect("project.db")  # appel de la base de données
            self.connection = sqlite3.connect("project.db", check_same_thread=False)  # 🔥 Ajout de check_same_thread=False
            self.connection.row_factory = sqlite3.Row  # Facultatif : pour récupérer les résultats sous forme de dictionnaire
            print("✅ Connexion SQLite établie avec support multi-thread")
        except sqlite3.Error as e:
            print(f"Erreur lors de la connexion à la base de données : {e}")
            raise

    def setup(self):
        self.execute("CREATE TABLE IF NOT EXISTS users(uid INTEGER PRIMARY KEY UNIQUE ,email VARCHAR UNIQUE, password VARCHAR)")
        self.execute("CREATE TABLE IF NOT EXISTS logs(id INTEGER PRIMARY KEY UNIQUE ,uid INTEGER ,action VARCHAR ,value VARCHAR)")
        try:
            self.execute(f"INSERT INTO users (email,password) VALUES ('admin', 'admin')")
        except:
            print("Admin already exists.")
        self.commit()

    def drop(self):
        self.execute("DROP TABLE IF EXISTS users")
        self.execute("DROP TABLE IF EXISTS logs")
        self.commit()

    #def execute(self, query:str):
    #    return self.__db.execute(query)
    
    def execute(self, query, params=None):
        """
        Exécute une requête SQL.
        :param query: Requête SQL avec placeholders (?)
        :param params: Tuple ou liste contenant les paramètres.
        :return: Curseur contenant les résultats.
        """
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor
        except sqlite3.Error as e:
            print(f"Erreur lors de l'exécution de la requête : {e}")
            raise
    
    def fetch_one(self, query, params=None):
        """
        Exécute une requête SQL et retourne une seule ligne.
        :param query: Requête SQL avec placeholders (?).
        :param params: Tuple ou liste contenant les paramètres.
        :return: Une seule ligne sous forme de tuple, ou (0,) si aucun résultat.
        """
        try:
            cursor = self.execute(query, params)
            result = cursor.fetchone()
            print(f"🔎 fetch_one Résultat: {result}")  # Debugging
            return result 
        
        except sqlite3.Error as e:
            print(f"❌ Erreur dans fetch_one : {e}")
            return None

    def commit(self):
        """
        Valide les modifications dans la base de données.
        """
        try:
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"Erreur lors du commit : {e}")
            raise

    def close(self):
        """
        Ferme la connexion à la base de données.
        """
        if self.connection:
            self.connection.close()
  
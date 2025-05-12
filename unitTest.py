from src.models.database import Database
from src.models.session import Session

import unittest


class UnitTest(unittest.TestCase):

    def setUp(self):
        """ s'exécute avant chaque test pour initialiser la BD et nettoyer les entrées de test. """
        self.db  = Database()  # initialisation de la BD
        self.db.execute("DELETE FROM users WHERE email LIKE 'test_%'")  # Nettoyage de la tablevuniquement pour les entrées de test avant chaque test
        self.db.commit()

    def tearDown(self):
        self.db.close()  # Ferme la connexion après chaque test

    def test_execute(self):
        """ test : vérifie l'insertion et la récupération"""
        self.db.execute("INSERT INTO users (email, password) VALUES (?, ?)", ("test_user@gmail.com", "password123!"))
        self.db.commit()

        res = self.db.execute("SELECT * FROM users WHERE email=?", ("test_user@gmail.com",))
        result = res.fetchone()

        self.assertIsNotNone(result, "La méthode execute ne fonctionne pas correctement.")
        self.assertGreater(len(result), 0, "La requête SELECT n'a retourné aucun résultat.")

    def test_commit(self):
        """ Teste l'insertion d'un utilisateur et la récupération de son UID. """
        s = Session("test@gmail.com", "12345678901!")  # Création d'une session utilisateur
        self.db.execute("INSERT INTO users (email, password) VALUES (?, ?)", (s.email, s.hash()))
        self.db.commit()

        # Requête sécurisée avec placeholders
        res = self.db.execute("SELECT uid FROM users WHERE password = ? AND email = ?", (s.hash(), s.email))
        result = res.fetchone()

        self.assertIsNotNone(result, "Aucun résultat trouvé pour l'utilisateur inséré.")
        self.assertGreater(len(result), 0, "La fonction commit ne fonctionne pas correctement.") # vérifie qu'il s'agit bien d'un uid valide

if __name__ == '__main__':
    unittest.main()
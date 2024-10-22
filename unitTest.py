from src.models.database import Database
from src.models.session import Session

import unittest


class UnitTest (unittest.TestCase):

    def test_execute(self):
        db = Database() #cible la DB
        res = db.execute("SELECT * FROM users") # définitrequête ensemble des données de la base
        self.assertIsNotNone(res, "execute function doesn't works !!!") #check résultat existe

    def test_commit(self):
        db = Database()
        s = Session("test@gmail.com", "123456789") #crée un objet session pour l'utilisateur précisé
        db.execute("INSERT INTO users (email,password) VALUES (?,?)", (s.email, s.hash())) #insère un nouvel utilisateur dans users
        print(f"SELECT uid FROM users WHERE password='{s.hash()}' and email='{s.email}'")
        res = db.execute(f"SELECT uid FROM users WHERE password='{s.hash()}' and email='{s.email}'")
        self.assertEqual(len(res.fetchone()), 1, "commit function doesn't work !!!" ) #check fonctinnement de commit 


if __name__ == '__main__':
    unittest.main()
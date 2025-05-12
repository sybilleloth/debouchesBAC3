from src.models.session import Session
from src.models.database import Database  # Import de la classe Database

db = Database()  # Instanciation de la base de données

def email_exists(email):
    """Vérifie si l'email est déjà enregistré dans la base de données"""
    query = "SELECT COUNT(*) FROM users WHERE email = ?"
    result = db.fetch_one(query, (email,))
    print(f"🔍 Vérification email '{email}' - Résultat: {result}")  # Debugging
    if result:
        return result[0] > 0
    return False

# vérifie si l’utilisateur s’est déjà connecté pour accepter / refuser l’inscription
def signup(login, mdp):
    if email_exists(login):  # Vérification avant d'insérer dans la base
        print("⛔ Cet email existe déjà, inscription refusée.")  # Log de refus
        return False  # Empêche l'inscription
    
    s = Session(login,mdp)
    try:
        s.signin()  # Insère l'utilisateur dans la base
        s.login()  # Connecte l'utilisateur après inscription
        if s.logged:
            s.persist()
            return True # Inscription réussie
        else:
            return False # Échec d'authentification après inscription
    
    except Exception as e:
        print(f"🔥 Erreur lors de l'inscription : {e}")
        return False # Évite toute inscription en cas d'erreur
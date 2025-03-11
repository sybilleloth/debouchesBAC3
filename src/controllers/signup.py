from src.models.session import Session

# vérifie si l’utilisateur s’est déjà connecté pour accepter / refuser l’inscription
def signup(login, mdp):
    s = Session(login,mdp)
    
    s.signin()
    s.login()
    if s.logged:
        s.persist()
        return True
    else:
        return False
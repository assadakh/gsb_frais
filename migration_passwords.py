import os
import django
from django.contrib.auth.hashers import make_password

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gsb_frais.settings')
django.setup()

from frais.models import Visiteur

def migrer_mots_de_passe():
    visiteurs = Visiteur.objects.all()
    compteur = 0
    
    print("Début de la migration des mots de passe...")
    
    for v in visiteurs:
        # On vérifie si le mot de passe est déjà haché
        # Un hash Django commence toujours par "pbkdf2_sha256$"
        if not v.mdp.startswith('pbkdf2_'):
            print(f"Hachage du mot de passe pour {v.login}...")
            v.mdp = make_password(v.mdp)
            v.save()
            compteur += 1
        else:
            print(f"Le mot de passe de {v.login} est déjà haché.")
            
    print(f"\nTerminé ! {compteur} mots de passe ont été hachés.")

if __name__ == "__main__":
    migrer_mots_de_passe()
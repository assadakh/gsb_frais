import os
import django
from datetime import date
from django.contrib.auth.hashers import make_password

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gsb_frais.settings')
django.setup()

from frais.models import Visiteur, Etat, FraisForfait

print("Initialisation de la base de donnees GSB...")

# ============================================================================
# 1. CREER LES ETATS
# ============================================================================
print("\nCreation des etats...")

etats_data = [
    {'id': 'CR', 'libelle': 'Fiche créée - saisie en cours'},
    {'id': 'CL', 'libelle': 'Saisie clôturée'},
    {'id': 'VA', 'libelle': 'Validée et mise en paiement'},
    {'id': 'RB', 'libelle': 'Remboursée'},
]

for etat in etats_data:
    obj, created = Etat.objects.get_or_create(
        id=etat['id'],
        defaults={'libelle': etat['libelle']}
    )
    if created:
        print(f"  [OK] {etat['id']} - {etat['libelle']}")
    else:
        print(f"  [INFO] {etat['id']} existe deja")

# ============================================================================
# 2. CREER LES FRAIS FORFAITAIRES
# ============================================================================
print("\nCreation des frais forfaitaires...")

frais_forfait_data = [
    {'id': 'ETP', 'libelle': 'Forfait Etape', 'montant': 110.00},
    {'id': 'KM', 'libelle': 'Frais Kilométrique', 'montant': 0.62},
    {'id': 'NUI', 'libelle': 'Nuitée Hôtel', 'montant': 80.00},
    {'id': 'REP', 'libelle': 'Repas Restaurant', 'montant': 25.00},
]

for frais in frais_forfait_data:
    obj, created = FraisForfait.objects.get_or_create(
        id=frais['id'],
        defaults={
            'libelle': frais['libelle'],
            'montant': frais['montant']
        }
    )
    if created:
        print(f"  [OK] {frais['id']} - {frais['libelle']} ({frais['montant']} EUR)")
    else:
        print(f"  [INFO] {frais['id']} existe deja")

# ============================================================================
# 3. CREER LES VISITEURS
# ============================================================================
print("\nCreation des visiteurs...")

visiteurs_data = [
    {'id': 'a131', 'nom': 'Villechalane', 'prenom': 'Louis', 'login': 'lvillachane', 'mdp': 'jux7g', 'adresse': '8 rue des Charmes', 'cp': '46000', 'ville': 'Cahors', 'dateembauche': date(2005, 12, 21)},
    {'id': 'a17', 'nom': 'Andre', 'prenom': 'David', 'login': 'dandre', 'mdp': 'oppg5', 'adresse': '1 rue Petit', 'cp': '46200', 'ville': 'Lalbenque', 'dateembauche': date(1998, 11, 23)},
    {'id': 'a55', 'nom': 'Bedos', 'prenom': 'Christian', 'login': 'cbedos', 'mdp': 'gmhxd', 'adresse': '1 rue Peranud', 'cp': '46250', 'ville': 'Montcuq', 'dateembauche': date(1995, 1, 12)},
    {'id': 'a93', 'nom': 'Tusseau', 'prenom': 'Louis', 'login': 'ltusseau', 'mdp': 'ktp3s', 'adresse': '22 rue des Ternes', 'cp': '46123', 'ville': 'Gramat', 'dateembauche': date(2000, 5, 1)},
    {'id': 'b13', 'nom': 'Bentot', 'prenom': 'Pascal', 'login': 'pbentot', 'mdp': 'doyw1', 'adresse': '11 allée des Cerises', 'cp': '46512', 'ville': 'Bessines', 'dateembauche': date(1992, 7, 9)},
    {'id': 'b16', 'nom': 'Bioret', 'prenom': 'Luc', 'login': 'lbioret', 'mdp': 'hrjfs', 'adresse': '1 Avenue gambetta', 'cp': '46000', 'ville': 'Cahors', 'dateembauche': date(1998, 5, 11)},
    {'id': 'b19', 'nom': 'Bunisset', 'prenom': 'Francis', 'login': 'fbunisset', 'mdp': '4vbnd', 'adresse': '10 rue des Perles', 'cp': '93100', 'ville': 'Montreuil', 'dateembauche': date(1987, 10, 21)},
    {'id': 'b25', 'nom': 'Bunisset', 'prenom': 'Denise', 'login': 'dbunisset', 'mdp': 's1y1r', 'adresse': '23 rue Manin', 'cp': '75019', 'ville': 'paris', 'dateembauche': date(2010, 12, 5)},
    {'id': 'b28', 'nom': 'Cacheux', 'prenom': 'Bernard', 'login': 'bcacheux', 'mdp': 'uf7r3', 'adresse': '114 rue Blanche', 'cp': '75017', 'ville': 'Paris', 'dateembauche': date(2009, 11, 12)},
    {'id': 'b34', 'nom': 'Cadic', 'prenom': 'Eric', 'login': 'ecadic', 'mdp': '6u8dc', 'adresse': '123 avenue de la République', 'cp': '75011', 'ville': 'Paris', 'dateembauche': date(2008, 9, 23)},
    {'id': 'b825', 'nom': 'Labu', 'prenom': 'Marco', 'login': 'emlabu', 'mdp': 'u68cd', 'adresse': '321 avenue de la Mer', 'cp': '30240', 'ville': 'Grau du Roi', 'dateembauche': date(2018, 9, 23)},
    {'id': 'b4', 'nom': 'Charoze', 'prenom': 'Catherine', 'login': 'ccharoze', 'mdp': 'u817o', 'adresse': '100 rue Petit', 'cp': '75019', 'ville': 'Paris', 'dateembauche': date(2005, 11, 12)},
    {'id': 'b50', 'nom': 'Clepkens', 'prenom': 'Christophe', 'login': 'cclepkens', 'mdp': 'bw1us', 'adresse': '12 allée des Anges', 'cp': '93230', 'ville': 'Romainville', 'dateembauche': date(2003, 8, 11)},
    {'id': 'b59', 'nom': 'Cottin', 'prenom': 'Vincenne', 'login': 'vcottin', 'mdp': '2hoh9', 'adresse': '36 rue Des Roches', 'cp': '93100', 'ville': 'Monteuil', 'dateembauche': date(2001, 11, 18)},
    {'id': 'c14', 'nom': 'Daburon', 'prenom': 'François', 'login': 'fdaburon', 'mdp': '7oqpv', 'adresse': '13 rue de Chanzy', 'cp': '94000', 'ville': 'Créteil', 'dateembauche': date(2002, 2, 11)},
    {'id': 'c3', 'nom': 'De', 'prenom': 'Philippe', 'login': 'pde', 'mdp': 'gk9kx', 'adresse': '13 rue Barthes', 'cp': '94000', 'ville': 'Créteil', 'dateembauche': date(2010, 12, 14)},
    {'id': 'c54', 'nom': 'Debelle', 'prenom': 'Michel', 'login': 'mdebelle', 'mdp': 'od5rt', 'adresse': '181 avenue Barbusse', 'cp': '93210', 'ville': 'Rosny', 'dateembauche': date(2006, 11, 23)},
    {'id': 'd13', 'nom': 'Debelle', 'prenom': 'Jeanne', 'login': 'jdebelle', 'mdp': 'nvwqq', 'adresse': '134 allée des Joncs', 'cp': '44000', 'ville': 'Nantes', 'dateembauche': date(2000, 5, 11)},
    {'id': 'd23', 'nom': 'Defay', 'prenom': 'Nicolas', 'login': 'ndefay', 'mdp': '12-Soleil&', 'adresse': '51 Boulevard Gaston Monnerville', 'cp': '97440', 'ville': 'Saint-Denis', 'dateembauche': date(2023, 8, 1)},
    {'id': 'd51', 'nom': 'Debroise', 'prenom': 'Michel', 'login': 'mdebroise', 'mdp': 'sghkb', 'adresse': '2 Bld Jourdain', 'cp': '44000', 'ville': 'Nantes', 'dateembauche': date(2001, 4, 17)},
    {'id': 'e22', 'nom': 'Desmarquest', 'prenom': 'Nathalie', 'login': 'ndesmarquest', 'mdp': 'f1fob', 'adresse': '14 Place d Arc', 'cp': '45000', 'ville': 'Orléans', 'dateembauche': date(2005, 11, 12)},
    {'id': 'e24', 'nom': 'Desnost', 'prenom': 'Pierre', 'login': 'pdesnost', 'mdp': '4k2o5', 'adresse': '16 avenue des Cèdres', 'cp': '23200', 'ville': 'Guéret', 'dateembauche': date(2001, 2, 5)},
    {'id': 'e39', 'nom': 'Dudouit', 'prenom': 'Frédéric', 'login': 'fdudouit', 'mdp': '44im8', 'adresse': '18 rue de l église', 'cp': '23120', 'ville': 'GrandBourg', 'dateembauche': date(2000, 8, 1)},
    {'id': 'e49', 'nom': 'Duncombe', 'prenom': 'Claude', 'login': 'cduncombe', 'mdp': 'qf77j', 'adresse': '19 rue de la tour', 'cp': '23100', 'ville': 'La souteraine', 'dateembauche': date(1987, 10, 10)},
    {'id': 'e5', 'nom': 'Enault-Pascreau', 'prenom': 'Céline', 'login': 'cenault', 'mdp': 'y2qdu', 'adresse': '25 place de la gare', 'cp': '23200', 'ville': 'Gueret', 'dateembauche': date(1995, 9, 1)},
    {'id': 'e52', 'nom': 'Eynde', 'prenom': 'Valérie', 'login': 'veynde', 'mdp': 'i7sn3', 'adresse': '3 Grand Place', 'cp': '13015', 'ville': 'Marseille', 'dateembauche': date(1999, 11, 1)},
    {'id': 'e63', 'nom': 'Alphonsine', 'prenom': 'Emmanuel', 'login': 'ealphonsine', 'mdp': '12-Soleil&', 'adresse': '51 Boulevard Gaston Monnerville', 'cp': '97440', 'ville': 'Saint-Denis', 'dateembauche': date(2023, 8, 1)},
    {'id': 'f21', 'nom': 'Finck', 'prenom': 'Jacques', 'login': 'jfinck', 'mdp': 'mpb3t', 'adresse': '10 avenue du Prado', 'cp': '13002', 'ville': 'Marseille', 'dateembauche': date(2001, 11, 10)},
    {'id': 'f39', 'nom': 'Frémont', 'prenom': 'Fernande', 'login': 'ffremont', 'mdp': 'xs5tq', 'adresse': '4 route de la mer', 'cp': '13012', 'ville': 'Allauh', 'dateembauche': date(1998, 10, 1)},
    {'id': 'f4', 'nom': 'Gest', 'prenom': 'Alain', 'login': 'agest', 'mdp': 'dywvt', 'adresse': '30 avenue de la mer', 'cp': '13025', 'ville': 'Berre', 'dateembauche': date(1985, 11, 1)},
]

for data in visiteurs_data:
    # ON HACHE LE MOT DE PASSE AVANT L'INSERTION
    mot_de_passe_clair = data['mdp']
    data['mdp'] = make_password(mot_de_passe_clair)

    # On utilise update_or_create pour forcer la mise à jour si le visiteur existe déjà
    visiteur, created = Visiteur.objects.update_or_create(
        id=data['id'],
        defaults=data
    )
    
    action = "[CREATION]" if created else "[MISE A JOUR]"
    print(f"  {action} {visiteur.prenom} {visiteur.nom} -> MDP haché OK")

# ============================================================================
# RESUME
# ============================================================================
print("\n" + "="*60)
print("BASE DE DONNEES INITIALISEE AVEC SUCCES !")
print("="*60)

print(f"\nStatistiques :")
print(f"  - Etats : {Etat.objects.count()}")
print(f"  - Frais forfaitaires : {FraisForfait.objects.count()}")
print(f"  - Visiteurs : {Visiteur.objects.count()}")

print(f"\nExemples de connexion :")
print(f"  - Login: dandre      / Mot de passe: oppg5")
print(f"  - Login: lvillachane / Mot de passe: jux7g")
print(f"  - Login: cbedos      / Mot de passe: gmhxd")
print(f"  - Login: ndefay      / Mot de passe: 12-Soleil&")

print(f"\nVous pouvez maintenant lancer le serveur :")
print(f"   python manage.py runserver")
print(f"\n   Puis ouvrir : http://localhost:8000/")
print("="*60 + "\n")
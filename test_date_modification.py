"""
Script de test pour verifier la mise a jour de la date de modification
"""
import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gsb_frais.settings')
django.setup()

from frais.models import Visiteur, FicheFrais, LigneFraisForfait, LigneFraisHorsForfait, FraisForfait

print("=" * 60)
print("TEST DE LA MISE A JOUR DE LA DATE DE MODIFICATION")
print("=" * 60)

# Recuperer un visiteur de test
visiteur = Visiteur.objects.first()
print(f"\n1. Visiteur de test : {visiteur}")

# Recuperer ou creer une fiche du mois en cours
mois = date.today().strftime('%Y%m')
fiche, created = FicheFrais.objects.get_or_create(
    idvisiteur=visiteur,
    mois=mois,
    defaults={
        'nbjustificatifs': 0,
        'montantvalide': 0,
        'datemodif': date.today() - timedelta(days=5),  # 5 jours dans le passe
        'idetat_id': 'CR'
    }
)

if created:
    print(f"\n2. Fiche creee pour le mois {mois}")
else:
    print(f"\n2. Fiche existante pour le mois {mois}")

# Afficher la date initiale
print(f"\n3. Date de modification AVANT : {fiche.datemodif}")

# Test 1 : Modifier un frais forfaitaire
print("\n4. Test 1 : Modification d'un frais forfaitaire...")
frais_forfait = FraisForfait.objects.first()
ligne_forfait, _ = LigneFraisForfait.objects.get_or_create(
    idvisiteur=visiteur,
    mois=mois,
    idfraisforfait=frais_forfait,
    defaults={'quantite': 0}
)

# Modifier la quantite
from frais.views import maj_frais_forfait
maj_frais_forfait(visiteur, mois, {frais_forfait.id: 5})

# Recharger la fiche
fiche.refresh_from_db()
print(f"   Date de modification APRES modification forfait : {fiche.datemodif}")
print(f"   Date du jour : {date.today()}")
if fiche.datemodif == date.today():
    print("   [OK] Date mise a jour correctement")
else:
    print("   [ERREUR] Date NON mise a jour")

# Test 2 : Ajouter un frais hors forfait
print("\n5. Test 2 : Ajout d'un frais hors forfait...")
from frais.views import creer_nouveau_frais_hors_forfait

# Changer la date pour tester
FicheFrais.objects.filter(idvisiteur=visiteur, mois=mois).update(
    datemodif=date.today() - timedelta(days=1)
)

creer_nouveau_frais_hors_forfait(
    visiteur,
    mois,
    "Test frais",
    date.today().strftime('%d/%m/%Y'),
    "25.50"
)

# Recharger la fiche
fiche.refresh_from_db()
print(f"   Date de modification APRES ajout hors forfait : {fiche.datemodif}")
if fiche.datemodif == date.today():
    print("   [OK] Date mise a jour correctement")
else:
    print("   [ERREUR] Date NON mise a jour")

# Test 3 : Supprimer un frais hors forfait
print("\n6. Test 3 : Suppression d'un frais hors forfait...")
frais_hf = LigneFraisHorsForfait.objects.filter(
    idvisiteur=visiteur,
    mois=mois
).first()

if frais_hf:
    # Changer la date pour tester
    FicheFrais.objects.filter(idvisiteur=visiteur, mois=mois).update(
        datemodif=date.today() - timedelta(days=2)
    )

    from frais.views import supprimer_frais_hors_forfait
    supprimer_frais_hors_forfait(frais_hf.id)

    # Recharger la fiche
    fiche.refresh_from_db()
    print(f"   Date de modification APRES suppression : {fiche.datemodif}")
    if fiche.datemodif == date.today():
        print("   [OK] Date mise a jour correctement")
    else:
        print("   [ERREUR] Date NON mise a jour")
else:
    print("   [INFO] Aucun frais hors forfait a supprimer")

print("\n" + "=" * 60)
print("FIN DES TESTS")
print("=" * 60)

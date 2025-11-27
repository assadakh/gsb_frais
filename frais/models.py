"""
Modèles Django pour l'application GSB Frais
Équivalent de la classe PdoGsb (class.pdogsb.inc.php)
Ces modèles correspondent EXACTEMENT à votre base de données MySQL existante
"""
from django.db import models


class Visiteur(models.Model):
    """
    Modèle correspondant à la table 'Visiteur'
    Représente un visiteur médical GSB
    """
    id = models.CharField(primary_key=True, max_length=4, db_column='id')
    nom = models.CharField(max_length=30, null=True, blank=True, db_column='nom')
    prenom = models.CharField(max_length=30, null=True, blank=True, db_column='prenom')
    login = models.CharField(max_length=20, null=True, blank=True, db_column='login')
    mdp = models.CharField(max_length=20, null=True, blank=True, db_column='mdp')  # ← CORRIGÉ : 20 au lieu de 255
    adresse = models.CharField(max_length=40, null=True, blank=True, db_column='adresse')  # ← CORRIGÉ : 40 au lieu de 30
    cp = models.CharField(max_length=5, null=True, blank=True, db_column='cp')
    ville = models.CharField(max_length=30, null=True, blank=True, db_column='ville')
    dateembauche = models.DateField(db_column='dateEmbauche', null=True, blank=True)

    class Meta:
        db_table = 'Visiteur'  # ← CORRIGÉ : Majuscule
        managed = True  # ← CORRIGÉ : True pour SQLite

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class Etat(models.Model):
    """
    Modèle correspondant à la table 'Etat'
    États possibles d'une fiche de frais (CR, CL, VA, RB, etc.)
    """
    id = models.CharField(primary_key=True, max_length=2, db_column='id')
    libelle = models.CharField(max_length=30, null=True, blank=True, db_column='libelle')  # ← CORRIGÉ : varchar(30)

    class Meta:
        db_table = 'Etat'  # ← CORRIGÉ : Majuscule
        managed = True  # ← CORRIGÉ : True pour SQLite

    def __str__(self):
        return self.libelle or self.id


class FraisForfait(models.Model):
    """
    Modèle correspondant à la table 'FraisForfait'
    Types de frais forfaitaires (repas, nuitée, étape, km)
    """
    id = models.CharField(primary_key=True, max_length=3, db_column='id')
    libelle = models.CharField(max_length=20, null=True, blank=True, db_column='libelle')
    montant = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, db_column='montant')

    class Meta:
        db_table = 'FraisForfait'  # ← CORRIGÉ : Majuscules
        managed = True  # ← CORRIGÉ : True pour SQLite

    def __str__(self):
        return self.libelle or self.id


class FicheFrais(models.Model):
    """
    Modèle correspondant à la table 'FicheFrais'
    Fiche de frais mensuelle d'un visiteur
    """
    idvisiteur = models.ForeignKey(
        Visiteur, 
        on_delete=models.CASCADE,  # ← CORRIGÉ : CASCADE au lieu de DO_NOTHING pour SQLite
        db_column='idVisiteur'
    )
    mois = models.CharField(max_length=6, db_column='mois')
    nbjustificatifs = models.IntegerField(db_column='nbJustificatifs', null=True, blank=True, default=0)
    montantvalide = models.DecimalField(
        db_column='montantValide', 
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        default=0
    )
    datemodif = models.DateField(db_column='dateModif', null=True, blank=True)
    idetat = models.ForeignKey(
        Etat, 
        on_delete=models.CASCADE,  # ← CORRIGÉ : CASCADE au lieu de DO_NOTHING
        db_column='idEtat',
        default='CR'  # ← AJOUTÉ : valeur par défaut
    )

    class Meta:
        db_table = 'FicheFrais'  # ← CORRIGÉ : Majuscules
        unique_together = (('idvisiteur', 'mois'),)
        managed = True  # ← CORRIGÉ : True pour SQLite

    def __str__(self):
        return f"Fiche {self.mois} - {self.idvisiteur}"


class LigneFraisForfait(models.Model):
    """
    Modèle correspondant à la table 'LigneFraisForfait'
    Ligne de frais forfaitaire dans une fiche
    """
    idvisiteur = models.ForeignKey(
        Visiteur, 
        on_delete=models.CASCADE,  # ← CORRIGÉ : CASCADE
        db_column='idVisiteur'
    )
    mois = models.CharField(max_length=6, db_column='mois')
    idfraisforfait = models.ForeignKey(
        FraisForfait, 
        on_delete=models.CASCADE,  # ← CORRIGÉ : CASCADE
        db_column='idFraisForfait'
    )
    quantite = models.IntegerField(null=True, blank=True, default=0, db_column='quantite')

    class Meta:
        db_table = 'LigneFraisForfait'  # ← CORRIGÉ : Majuscules
        unique_together = (('idvisiteur', 'mois', 'idfraisforfait'),)
        managed = True  # ← CORRIGÉ : True pour SQLite

    def __str__(self):
        return f"{self.idfraisforfait.libelle} - Qté: {self.quantite}"


class LigneFraisHorsForfait(models.Model):
    """
    Modèle correspondant à la table 'LigneFraisHorsForfait'
    Ligne de frais hors forfait dans une fiche
    """
    id = models.AutoField(primary_key=True, db_column='id')
    idvisiteur = models.ForeignKey(
        Visiteur, 
        on_delete=models.CASCADE,  # ← CORRIGÉ : CASCADE
        db_column='idVisiteur'
    )
    mois = models.CharField(max_length=6, db_column='mois')
    libelle = models.CharField(max_length=100, null=True, blank=True, db_column='libelle')
    date = models.DateField(null=True, blank=True, db_column='date')
    montant = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, db_column='montant')

    class Meta:
        db_table = 'LigneFraisHorsForfait'  # ← CORRIGÉ : Majuscules
        managed = True  # ← CORRIGÉ : True pour SQLite

    def __str__(self):
        return f"{self.libelle} - {self.montant}€"
"""
Contrôleurs de l'application GSB Frais
Équivalent EXACT des fichiers:
- c_connexion.php
- c_gererFrais.php
- c_etatFrais.php
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from datetime import datetime, date
from .models import Visiteur, FicheFrais, LigneFraisForfait, LigneFraisHorsForfait, FraisForfait, Etat
from .utils import (
    est_connecte, connecter, deconnecter, 
    get_mois, date_anglais_vers_francais, date_francais_vers_anglais,
    les_qte_frais_valides, valide_infos_frais, get_nom_mois
)


# ============================================================================
# CONTRÔLEUR CONNEXION
# ============================================================================

def connexion(request):
    """
    Gère la connexion des visiteurs avec vérification de mot de passe haché
    """
    if est_connecte(request):
        return redirect('accueil')

    if request.method != 'POST':
        return render(request, 'frais/v_connexion.html', {'is_login_page': True})

    login = request.POST.get('login', '')
    mdp_saisi = request.POST.get('mdp', '') # Le mot de passe en clair tapé par l'user

    try:
        # 1. On cherche l'utilisateur SEULEMENT par son login
        visiteur = Visiteur.objects.get(login=login)

        # 2. On compare le mot de passe saisi avec le hash en base
        if check_password(mdp_saisi, visiteur.mdp):
            # C'est gagné !
            connecter(request, visiteur.id, visiteur.nom, visiteur.prenom)
            return redirect('accueil')
        else:
            # Mauvais mot de passe
            messages.error(request, "Login ou mot de passe incorrect")
            return render(request, 'frais/v_connexion.html', {'is_login_page': True})

    except Visiteur.DoesNotExist:
        # Login inconnu
        messages.error(request, "Login ou mot de passe incorrect")
        return render(request, 'frais/v_connexion.html', {'is_login_page': True})


def deconnexion_view(request):
    """
    Déconnecte l'utilisateur
    Équivalent de: deconnecter()
    """
    deconnecter(request)
    return redirect('connexion')


def accueil(request):
    """
    Page d'accueil après connexion
    Redirige vers la page de gestion des frais
    """
    if not est_connecte(request):
        return redirect('connexion')

    # Rediriger vers la page de saisie des frais
    return redirect('gerer_frais')


# ============================================================================
# CONTRÔLEUR GESTION DES FRAIS - Équivalent de c_gererFrais.php
# ============================================================================

def gerer_frais(request):
    """
    Gère la saisie des frais du mois en cours
    Équivalent EXACT de c_gererFrais.php
    """
    if not est_connecte(request):
        return redirect('connexion')

    id_visiteur = request.session.get('idVisiteur')
    visiteur = Visiteur.objects.get(id=id_visiteur)

    # Obtenir le mois actuel (format aaaamm)
    # Équivalent de: $mois = getMois(date("d/m/Y"))
    mois = datetime.now().strftime('%Y%m')
    num_annee = mois[0:4]
    num_mois = mois[4:6]

    # TOUJOURS vérifier et créer la fiche si elle n'existe pas
    # Équivalent de: $pdo->estPremierFraisMois($idVisiteur, $mois)
    if not FicheFrais.objects.filter(idvisiteur=visiteur, mois=mois).exists():
        # Équivalent de: $pdo->creeNouvellesLignesFrais($idVisiteur, $mois)
        creer_nouvelles_lignes_frais(visiteur, mois)

    # Traiter les actions
    action = request.POST.get('action', 'saisirFrais')

    if action == 'validerMajFraisForfait':
        # Récupérer les frais du formulaire
        les_frais = {}
        for key in request.POST:
            if key.startswith('frais_'):
                id_frais = key.replace('frais_', '')
                les_frais[id_frais] = request.POST.get(key, 0)
        
        # Équivalent de: lesQteFraisValides($lesFrais)
        if les_qte_frais_valides(les_frais):
            # Équivalent de: $pdo->majFraisForfait($idVisiteur, $mois, $lesFrais)
            maj_frais_forfait(visiteur, mois, les_frais)
            messages.success(request, "Frais forfaitaires mis à jour avec succès")
        else:
            messages.error(request, "Les valeurs des frais doivent être numériques")
    
    elif action == 'validerCreationFrais':
        date_frais = request.POST.get('dateFrais', '').strip()
        libelle = request.POST.get('libelle', '').strip()
        montant = request.POST.get('montant', '').strip()

        # Équivalent de: valideInfosFrais($dateFrais, $libelle, $montant)
        erreurs = valide_infos_frais(date_frais, libelle, montant)

        if erreurs:
            for erreur in erreurs:
                messages.error(request, erreur)
        else:
            # Équivalent de: $pdo->creeNouveauFraisHorsForfait(...)
            creer_nouveau_frais_hors_forfait(visiteur, mois, libelle, date_frais, montant)
            messages.success(request, "Frais hors forfait ajouté avec succès")
    
    elif action == 'supprimerFrais':
        id_frais = request.POST.get('idFrais')
        # Équivalent de: $pdo->supprimerFraisHorsForfait($idFrais)
        supprimer_frais_hors_forfait(id_frais)
        messages.success(request, "Frais hors forfait supprimé avec succès")
    
    # Récupérer les données pour l'affichage
    # Équivalent de: $pdo->getLesFraisHorsForfait($idVisiteur, $mois)
    les_frais_hors_forfait = get_les_frais_hors_forfait(visiteur, mois)
    
    # Équivalent de: $pdo->getLesFraisForfait($idVisiteur, $mois)
    les_frais_forfait = get_les_frais_forfait(visiteur, mois)
    
    context = {
        'les_frais_forfait': les_frais_forfait,
        'les_frais_hors_forfait': les_frais_hors_forfait,
        'num_annee': num_annee,
        'num_mois': num_mois,
        'nom_mois': get_nom_mois(num_mois)
    }
    
    return render(request, 'frais/v_listeFrais.html', context)


# ============================================================================
# CONTRÔLEUR ÉTAT DES FRAIS - Équivalent de c_etatFrais.php
# ============================================================================


def etat_frais(request):
    """
    Gère la consultation de l'état des fiches de frais
    Équivalent EXACT de c_etatFrais.php
    """
    if not est_connecte(request):
        return redirect('connexion')
    
    id_visiteur = request.session.get('idVisiteur')
    visiteur = Visiteur.objects.get(id=id_visiteur)
    
    action = request.GET.get('action', 'selectionnerMois')
    
    if action == 'selectionnerMois':
        # Équivalent de: $lesMois=$pdo->getLesMoisDisponibles($idVisiteur)
        les_mois = get_les_mois_disponibles(visiteur)
        
        # Sélectionner le dernier mois par défaut
        # Équivalent de: $lesCles = array_keys($lesMois); $moisASelectionner = $lesCles[0];
        mois_a_selectionner = None
        if les_mois:
            mois_a_selectionner = list(les_mois.keys())[0]
        
        context = {
            'les_mois': les_mois,
            'mois_a_selectionner': mois_a_selectionner
        }
        return render(request, 'frais/v_listeMois.html', context)
    
    elif action == 'voirEtatFrais':
        le_mois = request.GET.get('lstMois')
        
        # Équivalent de: $lesMois=$pdo->getLesMoisDisponibles($idVisiteur)
        les_mois = get_les_mois_disponibles(visiteur)
        mois_a_selectionner = le_mois
        
        # Équivalent de: $pdo->getLesFraisHorsForfait($idVisiteur, $leMois)
        les_frais_hors_forfait = get_les_frais_hors_forfait(visiteur, le_mois)
        
        # Équivalent de: $pdo->getLesFraisForfait($idVisiteur, $leMois)
        les_frais_forfait = get_les_frais_forfait(visiteur, le_mois)
        
        # Équivalent de: $pdo->getLesInfosFicheFrais($idVisiteur, $leMois)
        les_infos_fiche_frais = get_les_infos_fiche_frais(visiteur, le_mois)
        
        num_annee = le_mois[0:4]
        num_mois = le_mois[4:6]
        
        lib_etat = les_infos_fiche_frais.get('libEtat', '')
        montant_valide = les_infos_fiche_frais.get('montantValide', 0)
        nb_justificatifs = les_infos_fiche_frais.get('nbJustificatifs', 0)
        date_modif = les_infos_fiche_frais.get('dateModif', '')
        
        # Équivalent de: dateAnglaisVersFrancais($dateModif)
        if date_modif:
            date_modif = date_anglais_vers_francais(date_modif)
        
        context = {
            'les_mois': les_mois,
            'mois_a_selectionner': mois_a_selectionner,
            'les_frais_hors_forfait': les_frais_hors_forfait,
            'les_frais_forfait': les_frais_forfait,
            'num_annee': num_annee,
            'num_mois': num_mois,
            'nom_mois': get_nom_mois(num_mois),
            'lib_etat': lib_etat,
            'montant_valide': montant_valide,
            'nb_justificatifs': nb_justificatifs,
            'date_modif': date_modif
        }
        
        return render(request, 'frais/v_etatFrais.html', context)
    
    return redirect('etat_frais')


# ============================================================================
# FONCTIONS MÉTIER - Équivalent des méthodes de class.pdogsb.inc.php
# ============================================================================

def get_les_frais_hors_forfait(visiteur, mois):
    """
    Équivalent de: $pdo->getLesFraisHorsForfait($idVisiteur, $mois)
    """
    frais = LigneFraisHorsForfait.objects.filter(
        idvisiteur=visiteur,
        mois=mois
    ).order_by('-date')

    # Convertir les dates au format français
    les_lignes = []
    for f in frais:
        les_lignes.append({
            'id': f.id,
            'date': date_anglais_vers_francais(f.date) if f.date else '',
            'libelle': f.libelle,
            'montant': f.montant
        })

    return les_lignes


def get_les_frais_forfait(visiteur, mois):
    """
    Équivalent de: $pdo->getLesFraisForfait($idVisiteur, $mois)
    """
    frais = LigneFraisForfait.objects.filter(
        idvisiteur=visiteur,
        mois=mois
    ).select_related('idfraisforfait').order_by('idfraisforfait__id')
    
    les_lignes = []
    for f in frais:
        les_lignes.append({
            'idfrais': f.idfraisforfait.id,
            'libelle': f.idfraisforfait.libelle,
            'quantite': f.quantite
        })
    
    return les_lignes


def get_les_mois_disponibles(visiteur):
    """
    Équivalent de: $pdo->getLesMoisDisponibles($idVisiteur)
    """
    fiches = FicheFrais.objects.filter(
        idvisiteur=visiteur
    ).order_by('-mois')
    
    les_mois = {}
    for fiche in fiches:
        mois = fiche.mois
        num_annee = mois[0:4]
        num_mois = mois[4:6]
        les_mois[mois] = {
            'mois': mois,
            'numAnnee': num_annee,
            'numMois': num_mois
        }
    
    return les_mois


def get_les_infos_fiche_frais(visiteur, mois):
    """
    Équivalent de: $pdo->getLesInfosFicheFrais($idVisiteur, $mois)
    """
    try:
        fiche = FicheFrais.objects.select_related('idetat').get(
            idvisiteur=visiteur,
            mois=mois
        )
        
        return {
            'idEtat': fiche.idetat.id,
            'dateModif': fiche.datemodif,
            'nbJustificatifs': fiche.nbjustificatifs if fiche.nbjustificatifs else 0,
            'montantValide': fiche.montantvalide if fiche.montantvalide else 0,
            'libEtat': fiche.idetat.libelle
        }
    except FicheFrais.DoesNotExist:
        return {}


def creer_nouvelles_lignes_frais(visiteur, mois):
    """
    Équivalent de: $pdo->creeNouvellesLignesFrais($idVisiteur, $mois)
    """
    # Récupérer le dernier mois saisi
    # Équivalent de: $dernierMois = $this->dernierMoisSaisi($idVisiteur)
    dernier_mois = FicheFrais.objects.filter(
        idvisiteur=visiteur
    ).order_by('-mois').first()
    
    # Si la dernière fiche est en cours de création, la clôturer
    # Équivalent de: if($laDerniereFiche['idEtat']=='CR') majEtatFicheFrais(...)
    if dernier_mois and dernier_mois.idetat.id == 'CR':
        etat_cl = Etat.objects.get(id='CL')
        dernier_mois.idetat = etat_cl
        dernier_mois.datemodif = date.today()
        dernier_mois.save()
    
    # Créer la nouvelle fiche de frais
    etat_cr = Etat.objects.get(id='CR')
    FicheFrais.objects.create(
        idvisiteur=visiteur,
        mois=mois,
        nbjustificatifs=0,
        montantvalide=0,
        datemodif=date.today(),
        idetat=etat_cr
    )
    
    # Créer les lignes de frais forfait
    # Équivalent de: $lesIdFrais = $this->getLesIdFrais()
    les_id_frais = FraisForfait.objects.all()
    for frais_forfait in les_id_frais:
        LigneFraisForfait.objects.create(
            idvisiteur=visiteur,
            mois=mois,
            idfraisforfait=frais_forfait,
            quantite=0
        )


def maj_frais_forfait(visiteur, mois, les_frais):
    """
    Équivalent de: $pdo->majFraisForfait($idVisiteur, $mois, $lesFrais)
    """
    for id_frais, quantite in les_frais.items():
        LigneFraisForfait.objects.filter(
            idvisiteur=visiteur,
            mois=mois,
            idfraisforfait__id=id_frais
        ).update(quantite=int(quantite))

    # Mettre à jour la date de modification de la fiche
    FicheFrais.objects.filter(
        idvisiteur=visiteur,
        mois=mois
    ).update(datemodif=date.today())


def creer_nouveau_frais_hors_forfait(visiteur, mois, libelle, date_frais, montant):
    """
    Équivalent de: $pdo->creeNouveauFraisHorsForfait($idVisiteur, $mois, $libelle, $date, $montant)
    """
    # Équivalent de: $dateFr = dateFrancaisVersAnglais($date)
    date_ang = date_francais_vers_anglais(date_frais)

    LigneFraisHorsForfait.objects.create(
        idvisiteur=visiteur,
        mois=mois,
        libelle=libelle,
        date=date_ang,
        montant=montant
    )

    # Mettre à jour la date de modification de la fiche
    FicheFrais.objects.filter(
        idvisiteur=visiteur,
        mois=mois
    ).update(datemodif=date.today())


def supprimer_frais_hors_forfait(id_frais):
    """
    Équivalent de: $pdo->supprimerFraisHorsForfait($idFrais)
    """
    # Récupérer le frais avant de le supprimer pour mettre à jour la fiche
    try:
        frais = LigneFraisHorsForfait.objects.get(id=id_frais)
        visiteur = frais.idvisiteur
        mois = frais.mois

        # Supprimer le frais
        frais.delete()

        # Mettre à jour la date de modification de la fiche
        FicheFrais.objects.filter(
            idvisiteur=visiteur,
            mois=mois
        ).update(datemodif=date.today())
    except LigneFraisHorsForfait.DoesNotExist:
        pass
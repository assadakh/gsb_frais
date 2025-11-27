"""
Fonctions utilitaires pour l'application GSB
Équivalent EXACT du fichier fct.inc.php
"""
from datetime import datetime, timedelta
from decimal import Decimal


def est_connecte(request):
    """
    Teste si un visiteur est connecté
    Équivalent de: estConnecte()
    """
    return 'idVisiteur' in request.session


def connecter(request, id, nom, prenom):
    """
    Enregistre dans la session les infos d'un visiteur
    Équivalent de: connecter($id, $nom, $prenom)
    """
    request.session['idVisiteur'] = id
    request.session['nom'] = nom
    request.session['prenom'] = prenom


def deconnecter(request):
    """
    Détruit la session active
    Équivalent de: deconnecter()
    """
    request.session.flush()


def date_francais_vers_anglais(date_fr):
    """
    Transforme une date au format français jj/mm/aaaa vers le format anglais aaaa-mm-jj
    Équivalent de: dateFrancaisVersAnglais($maDate)
    
    Args:
        date_fr (str): Date au format jj/mm/aaaa
    
    Returns:
        str: Date au format aaaa-mm-jj ou None si erreur
    """
    try:
        parties = date_fr.split('/')
        if len(parties) == 3:
            jour, mois, annee = parties
            return f"{annee}-{mois.zfill(2)}-{jour.zfill(2)}"
    except:
        pass
    return None


def date_anglais_vers_francais(date_ang):
    """
    Transforme une date au format anglais aaaa-mm-jj vers le format français jj/mm/aaaa
    Équivalent de: dateAnglaisVersFrancais($maDate)
    
    Args:
        date_ang (str ou date): Date au format aaaa-mm-jj
    
    Returns:
        str: Date au format jj/mm/aaaa
    """
    try:
        if isinstance(date_ang, str):
            parties = date_ang.split('-')
            if len(parties) == 3:
                annee, mois, jour = parties
                return f"{jour}/{mois}/{annee}"
        else:
            # Si c'est un objet date
            return date_ang.strftime('%d/%m/%Y')
    except:
        pass
    return ""


def get_mois(date_str):
    """
    Retourne le mois au format aaaamm selon le jour dans le mois
    Équivalent de: getMois($date)
    
    Args:
        date_str (str): Date au format jj/mm/aaaa
    
    Returns:
        str: Mois au format aaaamm
    """
    try:
        parties = date_str.split('/')
        if len(parties) == 3:
            jour, mois, annee = parties
            mois = mois.zfill(2)
            return f"{annee}{mois}"
    except:
        pass
    return datetime.now().strftime('%Y%m')


def est_entier_positif(valeur):
    """
    Indique si une valeur est un entier positif ou nul
    Équivalent de: estEntierPositif($valeur)
    
    Args:
        valeur: Valeur à tester
    
    Returns:
        bool: True si entier positif, False sinon
    """
    try:
        val = int(valeur)
        return val >= 0
    except:
        return False


def est_tableau_entiers(tab_entiers):
    """
    Indique si un tableau de valeurs est constitué d'entiers positifs ou nuls
    Équivalent de: estTableauEntiers($tabEntiers)
    
    Args:
        tab_entiers (list): Liste de valeurs
    
    Returns:
        bool: True si tous entiers positifs, False sinon
    """
    for valeur in tab_entiers:
        if not est_entier_positif(valeur):
            return False
    return True


def est_date_depassee(date_testee):
    """
    Vérifie si une date est inférieure d'un an à la date actuelle
    Équivalent de: estDateDepassee($dateTestee)

    Args:
        date_testee (str): Date au format jj/mm/aaaa

    Returns:
        bool: True si date dépassée (> 1 an), False sinon
    """
    try:
        parties = date_testee.split('/')
        if len(parties) == 3:
            jour, mois, annee = map(int, parties)
            date_test = datetime(annee, mois, jour)
            # Note: datetime.now() retourne la date système actuelle
            # Pour les tests, on utilise la vraie date du jour
            date_limite = datetime.now() - timedelta(days=365)
            return date_test < date_limite
    except:
        return True
    return False


def est_date_valide(date_str):
    """
    Vérifie la validité du format d'une date française jj/mm/aaaa
    Équivalent de: estDateValide($date)
    
    Args:
        date_str (str): Date au format jj/mm/aaaa
    
    Returns:
        bool: True si date valide, False sinon
    """
    try:
        parties = date_str.split('/')
        if len(parties) != 3:
            return False
        
        jour, mois, annee = map(int, parties)
        
        # Vérifier que c'est une date valide
        datetime(annee, mois, jour)
        return True
    except:
        return False


def les_qte_frais_valides(les_frais):
    """
    Vérifie que le dictionnaire de frais ne contient que des valeurs numériques
    Équivalent de: lesQteFraisValides($lesFrais)
    
    Args:
        les_frais (dict): Dictionnaire des frais
    
    Returns:
        bool: True si toutes les quantités sont valides, False sinon
    """
    return est_tableau_entiers(les_frais.values())


def valide_infos_frais(date_frais, libelle, montant):
    """
    Vérifie la validité des trois arguments : la date, le libellé et le montant
    Équivalent de: valideInfosFrais($dateFrais, $libelle, $montant)
    
    Args:
        date_frais (str): Date au format jj/mm/aaaa
        libelle (str): Libellé du frais
        montant (str ou Decimal): Montant du frais
    
    Returns:
        list: Liste des erreurs (vide si pas d'erreur)
    """
    erreurs = []
    
    if not date_frais or date_frais.strip() == '':
        erreurs.append("Le champ date ne doit pas être vide")
    else:
        if not est_date_valide(date_frais):
            erreurs.append("Date invalide")
        else:
            if est_date_depassee(date_frais):
                erreurs.append("date d'enregistrement du frais dépassé, plus de 1 an")
    
    if not libelle or libelle.strip() == '':
        erreurs.append("Le champ description ne peut pas être vide")
    
    if not montant or str(montant).strip() == '':
        erreurs.append("Le champ montant ne peut pas être vide")
    else:
        try:
            m = Decimal(str(montant))
            if m <= 0:
                erreurs.append("Le montant doit être supérieur à 0")
        except:
            erreurs.append("Le champ montant doit être numérique")
    
    return erreurs


def get_nom_mois(numero_mois):
    """
    Retourne le nom du mois en français
    
    Args:
        numero_mois (str ou int): Numéro du mois (01-12)
    
    Returns:
        str: Nom du mois
    """
    mois_dict = {
        '01': 'Janvier', '02': 'Février', '03': 'Mars', '04': 'Avril',
        '05': 'Mai', '06': 'Juin', '07': 'Juillet', '08': 'Août',
        '09': 'Septembre', '10': 'Octobre', '11': 'Novembre', '12': 'Décembre'
    }
    return mois_dict.get(str(numero_mois).zfill(2), '')
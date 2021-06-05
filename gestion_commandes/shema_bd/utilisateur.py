"""Utilisateur"""
from mongoengine import StringField, BooleanField, Document

from gestion_commandes.shema_bd.commande import obtenir_commandes, supprimer_commande


class Utilisateur(Document):
    """Class Utilisateur, représente un utilisateur."""
    nom = StringField(required=True, max_length=50)
    prenom = StringField(required=True, max_length=50)
    mdp = StringField(required=True)
    email = StringField(required=True, unique=True)
    est_admin = BooleanField(default=False, required=True)


def cree_utilisateur(nom, prenom, mdp, email):
    """Permet de crée un utilisateur"""
    utilisateur = Utilisateur(nom=nom, prenom=prenom, mdp=mdp, email=email)
    utilisateur.save()


def obtenir_utilisateur(nom_champ, valeur):
    """Permet d'obtenir un utilisateur selon le champ qui lui est spécifié (id, email)"""
    if nom_champ == 'id':
        return Utilisateur.objects.get(id=valeur)
    elif nom_champ == 'email':
        return Utilisateur.objects.get(email=valeur)


def obtenir_utilisateurs():
    """Permet d'obtenir toutes les utilisateurs"""
    return Utilisateur.objects()


def supprimer_utilisateur(email):
    """Permet de supprimer un utilisateur selon son email"""
    # On obtient les commandes de l'utilisateur
    commandes_utilisateur = obtenir_commandes(email_utilisateur=email)
    # On supprime ses commandes
    for commande in commandes_utilisateur:
        supprimer_commande(id=commande.id)
    # On supprime l'utilisateur
    Utilisateur.objects.get(email=email).delete()


def modifier_utilisateur(email, nom_champ, nouvelle_valeur):
    """Permet de modifier un utilisateur en lui spécifiant
    le champ (nom, prenom, mdp, email, est_admin)
    à changer ainsi que sa nouvelle valeur"""
    if nom_champ == 'nom':
        return Utilisateur.objects.get(email=email).update(nom=nouvelle_valeur)
    elif nom_champ == 'prenom':
        return Utilisateur.objects.get(email=email).update(prenom=nouvelle_valeur)
    elif nom_champ == 'mdp':
        return Utilisateur.objects.get(email=email).update(mdp=nouvelle_valeur)
    elif nom_champ == 'email':
        return Utilisateur.objects.get(email=email).update(email=nouvelle_valeur)
    elif nom_champ == 'est_admin':
        return Utilisateur.objects.get(email=email).update(est_admin=nouvelle_valeur)

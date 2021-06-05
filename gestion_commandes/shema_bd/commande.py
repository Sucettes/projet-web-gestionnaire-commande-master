"""Commande"""
from datetime import datetime
from decimal import Decimal

from mongoengine import \
    Document, StringField, ListField, DateField, EmbeddedDocumentField, DecimalField

from gestion_commandes.shema_bd.relation_produit import RelationProduit


class Commande(Document):
    """Class Commande, représente une commande."""
    nom = StringField(max_length=50)
    date_creation = DateField(default=datetime.now())
    relation_produit = ListField(EmbeddedDocumentField(RelationProduit))
    email_utilisateur = StringField(required=True)
    total_avant_taxes = DecimalField(default=0.00)
    total = DecimalField(default=0.00)

    def calculer_total(self):
        """Permet de calculer le total avec les taxes."""
        prix = Decimal(0)
        for relation in self.relation_produit:
            prix += relation.prix
        prix = round((prix * Decimal(1.15)), 2)
        self.total = prix
        self.save()

    def calculer_total_avant_taxes(self):
        """Permet de calculer le total sans les taxes."""
        prix = Decimal(0)
        for relation in self.relation_produit:
            prix += relation.prix
        self.total_avant_taxes = round(prix, 2)
        self.save()


def creer_commande(nom_commande, email_utilisateur):
    """Permet de crée une commande lorsqu'on lui envoie le nom de la commande
    et l'email de l'utilisateur"""
    commande = Commande(nom=nom_commande, email_utilisateur=email_utilisateur)
    commande.save()
    return commande


def obtenir_commande(id):
    """Permet d'obtenir une commande grâce à son id"""
    return Commande.objects.get(id=id)


def obtenir_commandes(email_utilisateur):
    """Permet d'obtenir tout les commandes d'un utilisateur grâce à son email"""
    return Commande.objects(email_utilisateur=email_utilisateur)


def modifier_commande(id_commande, nom_champ, nouvelle_valeur):
    """Permet de modifier la commande en lui spécifiant le champs (nom, produits) à changer."""
    if nom_champ == 'nom':
        return Commande.objects.get(id=id_commande).update(nom=nouvelle_valeur)
    elif nom_champ == 'produits':
        return Commande.objects.get(id=id_commande).update(relation_produit=nouvelle_valeur)


def supprimer_commande(id):
    """Permet de supprimer une commande grâce à son id"""
    Commande.objects.get(id=id).delete()

"""Produit"""
from mongoengine import Document, StringField, DecimalField, BooleanField


class Produit(Document):
    """Class Produit, représente un produit."""
    nom = StringField(max_length=50, required=True, unique=True)
    prix = DecimalField(required=True)
    description = StringField(max_length=250)
    categorie = StringField(max_length=50, required=True)
    en_stock = BooleanField(default=True)


def cree_produit(nom, description, prix, categorie):
    """Permet de crée un produit"""
    produit = Produit(nom=nom, description=description, prix=prix, categorie=categorie)
    produit.save()
    return produit


def obtenir_produit(nom_champ, valeur):
    """Permet d'obtenir un produit selon le champ qui lui est spécifié (id, nom)"""
    if nom_champ == 'id':
        return Produit.objects.get(id=valeur)
    elif nom_champ == 'nom':
        return Produit.objects.get(nom=valeur)


def obtenir_produits_recherche(categorie, nom):
    """Permet d'obtenir les produits de la recherche"""
    if categorie == "all":
        return Produit.objects(nom__icontains=nom, en_stock=True).limit(5).order_by('nom')
    else:
        return Produit.objects(categorie=categorie,
                               nom__icontains=nom, en_stock=True).limit(5).order_by('nom')


def obtenir_produits():
    """Permet d'obtenir tous les produits de la BD"""
    return Produit.objects()


def modifier_produit(id_produit, nom_champ, nouvelle_valeur):
    """Permet de modifier un produit en spécifiant le champs à modifier
    (nom, categorie, description, prix, en_stock)"""
    if nom_champ == 'categorie':
        return Produit.objects.get(id=id_produit).update(categorie=nouvelle_valeur)
    elif nom_champ == 'description':
        return Produit.objects.get(id=id_produit).update(description=nouvelle_valeur)
    elif nom_champ == 'prix':
        return Produit.objects.get(id=id_produit).update(prix=nouvelle_valeur)
    elif nom_champ == 'nom':
        return Produit.objects.get(id=id_produit).update(nom=nouvelle_valeur)
    elif nom_champ == 'en_stock':
        return Produit.objects.get(id=id_produit).update(en_stock=nouvelle_valeur)


def supprimer_produit(id):
    """Permet de supprimer un produit grâce à son id"""
    Produit.objects.get(id=id).delete()

"""Categories"""
from mongoengine import Document, StringField


class Categorie(Document):
    """Class Categorie, représente une catégorie."""
    nom = StringField(max_length=50, unique=True)

    def __str__(self):
        return self.nom


def cree_categorie(nom):
    """Permet de crée une catégorie"""
    categorie = Categorie(nom=nom)
    categorie.save()


def obtenir_categorie(nom):
    """Permet d'obtenir une catégorie"""
    categorie = Categorie.objects.get(nom=nom)
    return categorie


def obtenir_categories():
    """Permet d'obtenir tout les catégories"""
    categories = Categorie.objects()
    return categories


def supprimer_categorie(id):
    """Permet de supprimer une catégorie grâce à son id"""
    Categorie.objects.get(id=id).delete()

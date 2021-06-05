"""Relation produit"""
from bson import ObjectId
from mongoengine import StringField, EmbeddedDocument, DecimalField, ObjectIdField


class RelationProduit(EmbeddedDocument):
    """Class RelationProduit, un EmbeddedDocument de produit."""
    id = ObjectIdField(required=True, default=lambda: ObjectId())
    nom = StringField(max_length=50)
    prix = DecimalField(required=True)
    description = StringField(max_length=250)
    categorie = StringField(max_length=50)

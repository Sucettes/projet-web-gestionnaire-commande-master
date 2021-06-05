"""Gestions commande url"""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('authentification/', views.authentification, name='authentification'),
    path('inscription/', views.inscription, name='inscription'),
    path('recherche_produits/', views.recherche_produits, name='recherche_produits'),
    path('commande/<str:id_commande>/', views.commande, name='commande'),
    path('commande/<str:id_commande>/recherche/', views.recherche, name='recherche'),
    path('admin/', views.admin, name='admin'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('commande/<str:id_commande>/<str:id_relation_produit>/retirer/',
         views.retirer_produit_commande, name='retirer_produit_commande'),
    path('admin/produits/', views.produits, name='produits'),
    path('admin/produits/creation/', views.creation_produit, name='creation_produit'),
    path('admin/produits/modifier/<str:id_produit>/', views.modification_produit,
         name='modifier_produit'),
    path('admin/utilisateur/modifier/<str:id_utilisateur>/', views.modification_utilisateur,
         name='modifier_utilisateur'),
    path('admin/utilisateur/creation/', views.creation_utilisateur, name='creation_utilisateur'),
]

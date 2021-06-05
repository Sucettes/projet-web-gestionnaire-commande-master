"""projet_gestion_commandes URL Configuration"""
from django.urls import path, include

urlpatterns = [
    path('', include('gestion_commandes.urls'))
]

handler403 = "gestion_commandes.views.error_403"
handler404 = "gestion_commandes.views.error_404"
handler500 = "gestion_commandes.views.error_500"

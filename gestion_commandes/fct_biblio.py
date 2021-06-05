"""Bibliothèque de fonctions"""
from django.http import QueryDict


def obtenir_utilisateur_connecter(request):
    """Prend une requête en paramètre, puis retourne l'email de l'utilisateur connecté."""
    cookie = request.COOKIES.get("email_utilisateur")
    return cookie


def valider_creation_utilisateur(request):
    """Permet de valider les champs de la création d'un utilisateur."""
    from gestion_commandes.validations import valider_email_existant, valider_email
    # Validation des champs et récupération des messages d'erreurs.
    lst_messages = validation_utilisateur(request)

    # Validation si le email est déja utiliser.
    if valider_email_existant(request.POST['email']):
        lst_messages.append("L'email est déjà utilisé.")

    # Validation si le email est du bon format.
    if len(valider_email(request.POST['email'])) > 0:
        messages = valider_email(request.POST['email'])
        for msg in messages:
            lst_messages.append(msg)

    return lst_messages


def validation_utilisateur_modification(request):
    """Permet de valider et de retourner les messages d'erreurs
    lors de la modification d'un utilisateur."""
    from gestion_commandes.validations import valider_nom, valider_prenom, \
        valider_mdp, valider_mdp_identique
    lst_messages = []
    # Validation si le nom est de bon format.
    if len(valider_nom(request.PUT['nom'])) > 0:
        messages = valider_nom(request.PUT['nom'])
        for msg in messages:
            lst_messages.append({"message": msg})

    # Validation si le prénom est de bon format.
    if len(valider_prenom(request.PUT['prenom'])) > 0:
        messages = valider_prenom(request.PUT['prenom'])
        for msg in messages:
            lst_messages.append({"message": msg})

    # Validation si le mots de passe est de bon format.
    if len(valider_mdp(request.PUT['mdp'])) > 0:
        messages = valider_mdp(request.PUT['mdp'])
        for msg in messages:
            lst_messages.append({"message": msg})

    # Validation si les mots de passe sont identiques.
    if valider_mdp_identique(request.PUT['mdpConf'], request.PUT['mdp']) is False:
        lst_messages.append({"message": "Les deux mots de passe doivent être identiques."})

    return lst_messages


def validation_utilisateur(request):
    """Permet de valider et de retourner les messages d'erreurs si l'utilisateur est invalide."""
    from gestion_commandes.validations import valider_nom, valider_prenom, valider_mdp, \
        valider_mdp_identique
    lst_messages = []
    # Validation si le nom est du bon format.
    if len(valider_nom(request.POST['nom'])) > 0:
        messages = valider_nom(request.POST['nom'])
        for msg in messages:
            lst_messages.append(msg)

    # Validation si le prenom est de bon format.
    if len(valider_prenom(request.POST['prenom'])) > 0:
        messages = valider_prenom(request.POST['prenom'])
        for msg in messages:
            lst_messages.append(msg)

    # Validation si le mots de passe est de bon format.
    if len(valider_mdp(request.POST['mdp'])) > 0:
        messages = valider_mdp(request.POST['mdp'])
        for msg in messages:
            lst_messages.append(msg)

    # Validation si les mots de passe sont identiques.
    if valider_mdp_identique(request.POST['mdpConf'], request.POST['mdp']) is False:
        lst_messages.append("Les deux mots de passe doivent être identiques.")

    return lst_messages


def validation_produit(request):
    """Permet de valider les champs lors de la création d'un produit"""
    from gestion_commandes.validations import valider_nom_produit, valider_prix, valider_description
    lst_messages = []
    # Validation si le nom est du bon format.
    if len(valider_nom_produit(request.POST['nom'])) > 0:
        messages = valider_nom_produit(request.POST['nom'])
        for msg in messages:
            lst_messages.append(msg)

    # Validation du format du prix.
    if len(valider_prix(request.POST['prix'])) > 0:
        messages = valider_prix(request.POST['prix'])
        for msg in messages:
            lst_messages.append(msg)

    # Validation du format de la description.
    if len(valider_description(request.POST['description'])) > 0:
        messages = valider_description(request.POST['description'])
        for msg in messages:
            lst_messages.append(msg)

    return lst_messages


def valiation_produit_modification(request):
    """Permet de valider les champs lors de la modification d'un produit"""
    from gestion_commandes.validations import valider_nom_produit, valider_prix, valider_description
    lst_messages = []
    request.PUT = QueryDict(request.body)
    # Validation si le nom est du bon format.
    if len(valider_nom_produit(request.PUT['nom'])) > 0:
        messages = valider_nom_produit(request.PUT['nom'])
        for msg in messages:
            lst_messages.append({"message": msg})

    # Validation du format du prix.
    if len(valider_prix(request.PUT['prix'])) > 0:
        messages = valider_prix(request.PUT['prix'])
        for msg in messages:
            lst_messages.append({"message": msg})

    # Validation du format de la description.
    if len(valider_description(request.PUT['desc'])) > 0:
        messages = valider_description(request.PUT['desc'])
        for msg in messages:
            lst_messages.append({"message": msg})

    return lst_messages

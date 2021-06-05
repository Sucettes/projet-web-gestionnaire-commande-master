from django.http import JsonResponse, HttpResponse, QueryDict
from django.shortcuts import render, redirect

from gestion_commandes.fct_biblio import obtenir_utilisateur_connecter, \
    valider_creation_utilisateur, \
    validation_produit, valiation_produit_modification, validation_utilisateur_modification
from gestion_commandes.shema_bd.categorie import obtenir_categories
from gestion_commandes.shema_bd.commande import creer_commande, obtenir_commande, \
    modifier_commande, \
    supprimer_commande, obtenir_commandes
from gestion_commandes.shema_bd.produit import obtenir_produits, cree_produit, modifier_produit, \
    obtenir_produits_recherche, obtenir_produit
from gestion_commandes.shema_bd.relation_produit import RelationProduit
from gestion_commandes.shema_bd.utilisateur import cree_utilisateur, obtenir_utilisateurs, \
    modifier_utilisateur, obtenir_utilisateur, supprimer_utilisateur
from gestion_commandes.validations import \
    verifier_utilisateur_connecter, valider_nom_commande, \
    valider_email_existant, valider_utilisateur_login, valider_est_admin, \
    valider_utilisateur_acces_commande, \
    valider_commande_contient_produit, verifier_produit_existe, valider_categorie


def index(request):
    """Views index (page principale)."""
    # Verifier si l'utilisateur est connecter.
    if verifier_utilisateur_connecter(request):
        email_utilisateur = obtenir_utilisateur_connecter(request)
        # On vérifie qu'il est admin pour définir la valeur admin.
        est_admin = False
        if valider_est_admin(request):
            est_admin = True

        commandes_utilisateur = obtenir_commandes(email_utilisateur=email_utilisateur)

        if request.method == 'POST':
            if valider_nom_commande(request.POST['nom_commande']):
                context = {"commandesUtilisateur": commandes_utilisateur,
                           "email": email_utilisateur,
                           "message": "La commande est créée.", "admin": est_admin}

                creer_commande(nom_commande=request.POST['nom_commande'],
                               email_utilisateur=email_utilisateur)
            else:
                context = {"commandesUtilisateur": commandes_utilisateur,
                           "email": email_utilisateur,
                           "msg_erreur": "Le nom de la commande est invalide.",
                           "admin": est_admin}
        else:
            context = {"commandesUtilisateur": commandes_utilisateur,
                       "email": email_utilisateur, "admin": est_admin}

        return render(request, 'gestion_commandes/index.html', context)
    else:
        return redirect('authentification')


def inscription(request):
    """Views inscription (page d'inscription), permet de s'inscrire."""
    # Verifier si l'utilisateur est connecter.
    if verifier_utilisateur_connecter(request) is False:
        template_retour = "gestion_commandes/inscription.html"
        context = None

        if request.method == 'POST':
            # Appelle de la fonction pour valider l'utilisateur.
            lst_message = valider_creation_utilisateur(request)

            # Vérification si on peut créé l'utilisateur puis sa création.
            if len(lst_message) == 0 or lst_message is None:
                cree_utilisateur(request.POST['nom'], request.POST['prenom'], request.POST['mdp'],
                                 request.POST['email'])

                context = {"message": "Votre compte a bien été créé !"}
                return render(request, template_retour, context)
            else:
                context = {"validationCreation": lst_message}
        return render(request, template_retour, context)
    else:
        return redirect('index')


def authentification(request):
    """Views authentification (page d'authentification), permet de se connecter."""
    # Verifier si l'utilisateur est connecté.
    if verifier_utilisateur_connecter(request) is False:
        template_retour = "gestion_commandes/authentification.html"
        context = None
        if request.method == 'POST':
            # Validation si l'email existe.
            if valider_email_existant(request.POST['email']):
                # Validation si le mot de passe et l'email sont ceux d'un utilisateur.
                if valider_utilisateur_login(request.POST['email'], request.POST['mdp']):
                    # Création du retour
                    response = redirect('index')

                    # Netoyage des cookies pour eviter les problemes potentiels.
                    response.delete_cookie('email_utilisateur')
                    response.delete_cookie('mdp_utilisateur')

                    # Ajout du email dans le cookie (Il expire apres 2700 secondes.)
                    response.set_cookie(key='email_utilisateur', value=request.POST['email'], max_age=2700)
                    # Ajout du mdp dans le cookie (Il expire apres 2700 secondes.)
                    response.set_cookie(key='mdp_utilisateur', value=request.POST['mdp'], max_age=2700)

                    return response
                else:
                    context = {"message": "Les identifiants sont invalides!"}
            else:
                context = {"message": "Les identifiants sont invalides!"}
        return render(request, template_retour, context)
    else:
        return redirect('index')


def commande(request, id_commande):
    """Views commande. Elle permet de voir, modifier, supprimer une commande grace à son id."""
    # Verifier si l'utilisateur est connecter.
    if verifier_utilisateur_connecter(request):
        email_utilisateur = obtenir_utilisateur_connecter(request)
        if request.method == 'PUT':
            commande_bd = obtenir_commande(id=id_commande)
            request.PUT = QueryDict(request.body)

            commande_bd.calculer_total()
            commande_bd.calculer_total_avant_taxes()

            # Verification si le nom a été modifié.
            if request.PUT['nom'] != commande_bd.nom:
                # Validation si le nouveau nom respect les critères.
                if valider_nom_commande(request.PUT['nom']):
                    modifier_commande(id_commande=id_commande, nom_champ='nom',
                                      nouvelle_valeur=request.PUT['nom'])
                    return HttpResponse(200)
                else:
                    lst_messages = [{"message": "Le nom de la commande est invalide."}]
                    return JsonResponse(lst_messages, safe=False)
            return HttpResponse(304)

        if request.method == 'DELETE':
            # Validation si c'est bien une commande de l'utilisateur connecté.
            if valider_utilisateur_acces_commande(id_commande=id_commande,
                                                  email_utilisateur=email_utilisateur):
                supprimer_commande(id=id_commande)
                return HttpResponse(status=204)
            else:
                return render(request, 'gestion_commandes/403.html', {"email": " "}, status=403)

        if request.method == 'GET':
            # Valider si l'utilisateur à accès à la commande.
            if valider_utilisateur_acces_commande(id_commande=id_commande,
                                                  email_utilisateur=email_utilisateur):
                context = {"email": email_utilisateur, "commande": obtenir_commande(id=id_commande)}

                return render(request, 'gestion_commandes/commande.html', context)
            else:

                return render(request, 'gestion_commandes/403.html', {"email": " "}, status=403)
    else:
        return redirect('authentification')


def retirer_produit_commande(request, id_commande, id_relation_produit):
    """Views retire le produit de la commande"""
    if verifier_utilisateur_connecter(request):
        email_utilisateur = obtenir_utilisateur_connecter(request)
        # Validation si c'est bien une commande de l'utilisateur connecté.
        if valider_utilisateur_acces_commande(id_commande=id_commande, email_utilisateur=email_utilisateur):
            une_commande = obtenir_commande(id=id_commande)
            une_relation = valider_commande_contient_produit(une_commande, id_relation_produit)
            if une_relation is not None:
                une_commande.relation_produit.pop(une_commande.relation_produit.index(une_relation))
                modifier_commande(
                    id_commande=une_commande.id, nom_champ='produits', nouvelle_valeur=une_commande.relation_produit)

            une_commande.calculer_total()
            une_commande.calculer_total_avant_taxes()

            return redirect('commande', id_commande)
        else:
            # status 403 + page template custom 403 | il n'as pas access a la commande.
            return render(request, 'gestion_commandes/403.html', {"email": " "}, status=403)
    else:
        return redirect('authentification')


def recherche(request, id_commande):
    """Views page recherche"""
    # Verifier si l'utilisateur est connecter.
    if verifier_utilisateur_connecter(request):
        email_utilisateur = obtenir_utilisateur_connecter(request)
        if request.method == 'PUT':

            request.PUT = QueryDict(request.body)

            # Validation si c'est bien une commande de l'utilisateur connecté.
            if valider_utilisateur_acces_commande(id_commande=id_commande, email_utilisateur=email_utilisateur):
                nom_produit = request.PUT['nom_produit']
                un_produit = verifier_produit_existe(nom_produit)

                if un_produit is not None:
                    une_commande = obtenir_commande(id_commande)
                    une_relation = RelationProduit(nom=un_produit.nom, prix=un_produit.prix,
                                                   description=un_produit.description,
                                                   categorie=un_produit.categorie)
                    une_commande.relation_produit.append(une_relation)
                    modifier_commande(id_commande=une_commande.id, nom_champ='produits',
                                      nouvelle_valeur=une_commande.relation_produit)

                    une_commande.calculer_total()
                    une_commande.calculer_total_avant_taxes()

                    # Le produit a été ajouté.
                    return HttpResponse(200)
                else:
                    # Le produit n'as pas été ajouter.
                    return HttpResponse(404)
            else:
                return render(request, 'gestion_commandes/403.html', {"email": " "}, status=403)

        if request.method == 'GET':
            if valider_utilisateur_acces_commande(id_commande=id_commande, email_utilisateur=email_utilisateur):
                # Permet d'obtenir les catégories
                categories = obtenir_categories()

                context = {'commande_id': id_commande, "categories": categories, "email": email_utilisateur}

                return render(request, "gestion_commandes/recherche_produit.html", context)
            else:
                # status 403 + page template custom 403 | il n'as pas access a la commande.
                return render(request, 'gestion_commandes/403.html', {"email": " "}, status=403)
    else:
        return redirect("authentification")


def recherche_produits(request):
    """Permet de récupéré la liste des produits."""
    # Représente la catégorie reçu
    cat = request.GET['cat']
    # Représente le nom reçu
    nom = request.GET['nom']

    produits = obtenir_produits_recherche(cat, nom)
    produits_retour = []
    for produit in produits:
        produits_retour.append({'nom': produit.nom, 'categorie': produit.categorie,
                                'description': produit.description, 'prix': produit.prix})

    return JsonResponse(produits_retour, safe=False)


def admin(request):
    """Views admin (page admin)"""
    # Verifier si l'utilisateur est connecter.
    if verifier_utilisateur_connecter(request):
        email_utilisateur = obtenir_utilisateur_connecter(request)
        if valider_email_existant(email_utilisateur):
            if valider_est_admin(request) is True:
                # On obtient la liste de toutes les catégories
                categories = obtenir_categories()
                utilisateurs = obtenir_utilisateurs()

                context = {"email": email_utilisateur, "categories": categories, "utilisateurs": utilisateurs}

                return render(request, 'gestion_commandes/admin.html', context)

        return render(request, 'gestion_commandes/403.html', {"email": " "}, status=403)
    else:
        return redirect('authentification')


def produits(request):
    """Views produits (page accessible par l'administrateur uniquement)"""
    # Verifier si l'utilisateur est connecter.
    if verifier_utilisateur_connecter(request):
        email_utilisateur = obtenir_utilisateur_connecter(request)
        if valider_email_existant(email_utilisateur):
            if valider_est_admin(request) is True:
                produits = obtenir_produits()
                context = {"email": email_utilisateur, "produits": produits}
                return render(request, 'gestion_commandes/produits.html', context)

        # status 403 + page template custom 403
        return render(request, 'gestion_commandes/403.html', {"email": " "}, status=403)
    else:
        return redirect('authentification')


def creation_produit(request):
    """Views création produit (page accessible par l'administrateur uniquement)"""
    # Verifier si l'utilisateur est connecter.
    if verifier_utilisateur_connecter(request):
        email_utilisateur = obtenir_utilisateur_connecter(request)
        if valider_email_existant(email_utilisateur):
            if valider_est_admin(request) is True:

                if request.method == 'POST':

                    lst_messages = validation_produit(request)
                    categories = obtenir_categories()

                    # Validation si la catégorie est présente dans la requête.
                    if "categorie" not in request.POST:
                        lst_messages.append("La catégorie n'a pas été selectionnée")
                    elif len(valider_categorie(request.POST['categorie'])) > 0:
                        messages = valider_categorie(request.POST['categorie'])
                        for msg in messages:
                            lst_messages.append(msg)

                    # On vérifie qu'il n'y as pas d'erreur jusqu'à présent pour ne pas envoyer de caractères spéciaux
                    if len(lst_messages) > 0:
                        context = {"email": email_utilisateur, "categories": categories, "msg_erreur": lst_messages,
                                   "creation": True}
                        # On redirige l'usager afin de ne pas envoyer des caractères indésirables à la BD
                        return render(request, 'gestion_commandes/produit.html', context)

                    # Validation si il y a un produit déja existant avec le nom
                    if verifier_produit_existe(request.POST['nom']):
                        lst_messages.append("Le nom est déjà utilisé.")
                        context = {"email": email_utilisateur, "categories": categories, "msg_erreur": lst_messages,
                                   "creation": True}
                        return render(request, 'gestion_commandes/produit.html', context)

                    cree_produit(nom=request.POST['nom'], description=request.POST['description'],
                                 prix=request.POST['prix'], categorie=request.POST['categorie'])

                    context = {"email": email_utilisateur, "categories": categories,
                               "message": "Le produit a bien été créé !", "creation": True}
                    return render(request, 'gestion_commandes/produit.html', context)

                categories = obtenir_categories()
                context = {"email": email_utilisateur, "categories": categories, "creation": True}
                return render(request, 'gestion_commandes/produit.html', context)
            else:
                # status 403 + page template custom 403 | interdit
                return render(request, 'gestion_commandes/403.html', {"email": " "}, status=403)
    else:
        return redirect('authentification')


def modification_produit(request, id_produit):
    """Views modification d'un produit (page accessible par l'administrateur uniquement)"""
    # Verifier si l'utilisateur est connecter.
    if verifier_utilisateur_connecter(request):
        email_utilisateur = obtenir_utilisateur_connecter(request)
        if valider_email_existant(email_utilisateur):
            if valider_est_admin(request) is True:

                if request.method == 'PUT':
                    # On crée une query avec la chaîne que l'on à reçu.
                    request.PUT = QueryDict(request.body)
                    lst_messages = valiation_produit_modification(request)
                    produit_bd = obtenir_produit(nom_champ='id', valeur=id_produit)

                    # Validation si la catégorie est présente dans la requête.
                    if "categorie" not in request.PUT:
                        lst_messages.append({"message": "La catégorie n'a pas été selectionnée"})
                    elif len(valider_categorie(request.PUT['categorie'])) > 0:
                        messages = valider_categorie(request.PUT['categorie'])
                        for msg in messages:
                            lst_messages.append({"message": msg})

                    if len(lst_messages) > 0:
                        return JsonResponse(lst_messages, safe=False)

                    if request.PUT['nom'] != produit_bd.nom:
                        # Validation si il y a un produit déja existant avec le nom
                        if verifier_produit_existe(request.PUT['nom']):
                            lst_messages.append({"message": "Le nom est déjà utilisé."})
                            return JsonResponse(lst_messages, safe=False)
                    changement = False
                    if produit_bd.nom != request.PUT['nom']:
                        modifier_produit(id_produit=id_produit, nom_champ='nom',
                                         nouvelle_valeur=request.PUT['nom'])
                        changement = True
                    if produit_bd.description != request.PUT['desc']:
                        modifier_produit(id_produit=id_produit, nom_champ='description',
                                         nouvelle_valeur=request.PUT['desc'])
                        changement = True
                    if produit_bd.categorie != request.PUT['categorie']:
                        modifier_produit(id_produit=id_produit, nom_champ='categorie',
                                         nouvelle_valeur=request.PUT['categorie'])
                        changement = True
                    if produit_bd.prix != request.PUT['prix']:
                        modifier_produit(id_produit=id_produit, nom_champ='prix',
                                         nouvelle_valeur=request.PUT['prix'])
                        changement = True

                    # Permet de savoir si le produit est en stock
                    en_stock = True
                    if "en_stock" not in request.PUT:
                        en_stock = False
                    if produit_bd.en_stock != en_stock:
                        modifier_produit(id_produit=id_produit, nom_champ='en_stock', nouvelle_valeur=en_stock)
                        changement = True
                    if changement:
                        return HttpResponse(200)
                    else:
                        return HttpResponse(304)

                produit_bd = obtenir_produit(nom_champ='id', valeur=id_produit)
                categories = obtenir_categories()
                context = {"email": email_utilisateur, "categories": categories,
                           "modification": True, "produit": produit_bd}
                return render(request, 'gestion_commandes/produit.html', context)
            else:
                # status 403 + page template custom 403 | interdit
                return render(request, 'gestion_commandes/403.html', {"email": " "}, status=403)
    else:
        return redirect('authentification')


def modification_utilisateur(request, id_utilisateur):
    """Views modification d'un utilisateur (page accessible par l'administrateur uniquement)"""
    # Verifier si l'utilisateur est connecter.
    if verifier_utilisateur_connecter(request):
        email_utilisateur = obtenir_utilisateur_connecter(request)
        if valider_email_existant(email_utilisateur):
            if valider_est_admin(request) is True:

                if request.method == 'PUT':
                    # On crée une query avec la chaîne que l'on a reçu.
                    request.PUT = QueryDict(request.body)
                    utilisateur = obtenir_utilisateur(nom_champ='id', valeur=id_utilisateur)

                    # Validation de l'utilisateur
                    lst_messages = validation_utilisateur_modification(request)

                    # Validation si l'utilisateur est entrain de retirer sa permission administrateur
                    if "estAdmin" not in request.PUT:
                        if utilisateur.email == email_utilisateur:
                            lst_messages.append(
                                {"message": "Vous ne pouvez pas vous retirez votre permission administrateur."})

                    if len(lst_messages) > 0:
                        return JsonResponse(lst_messages, safe=False)

                    if utilisateur.nom != request.PUT['nom']:
                        modifier_utilisateur(email=utilisateur.email, nom_champ='nom',
                                             nouvelle_valeur=request.PUT['nom'])
                    if utilisateur.prenom != request.PUT['prenom']:
                        modifier_utilisateur(email=utilisateur.email, nom_champ='prenom',
                                             nouvelle_valeur=request.PUT['prenom'])
                    if utilisateur.mdp != request.PUT['mdp']:
                        modifier_utilisateur(email=utilisateur.email, nom_champ='mdp',
                                             nouvelle_valeur=request.PUT['mdp'])
                    bool_admin = True
                    if "estAdmin" not in request.PUT:
                        bool_admin = False
                    if utilisateur.est_admin != bool_admin:
                        modifier_utilisateur(email=utilisateur.email, nom_champ='est_admin',
                                             nouvelle_valeur=bool_admin)
                    return HttpResponse(200)

                if request.method == 'DELETE':
                    utilisateur = obtenir_utilisateur(nom_champ='id', valeur=id_utilisateur)

                    # Validation si l'utilisateur souhaite supprimer son propre compte.
                    if email_utilisateur == utilisateur.email:
                        return HttpResponse(status=403)

                    supprimer_utilisateur(email=utilisateur.email)
                    return HttpResponse(status=204)
                utilisateur = obtenir_utilisateur(nom_champ='id', valeur=id_utilisateur)
                commandes_utilisateur = obtenir_commandes(email_utilisateur=utilisateur.email)
                context = {"email": email_utilisateur, "modification": True, "utilisateur": utilisateur,
                           "commandes_utilisateur": commandes_utilisateur}

                return render(request, 'gestion_commandes/utilisateur.html', context)
            else:
                # status 403 + page template custom 403 | interdit
                return render(request, 'gestion_commandes/403.html', {"email": " "}, status=403)
    else:
        return redirect('authentification')


def creation_utilisateur(request):
    """Views de la création d'un utilisateur (page accessible par l'administrateur uniquement)"""
    # Verifier si l'utilisateur est connecter.
    if verifier_utilisateur_connecter(request):
        email_utilisateur = obtenir_utilisateur_connecter(request)
        if valider_email_existant(email_utilisateur):
            if valider_est_admin(request) is True:

                if request.method == 'POST':
                    # Appelle de la fonction pour valider l'utilisateur.
                    lst_messages = valider_creation_utilisateur(request)

                    if len(lst_messages) > 0:
                        context = {"email": email_utilisateur, "msg_erreur": lst_messages, "creation": True}

                        # On redirige l'usager afin de ne pas envoyer des caractères indésirables à la BD
                        return render(request, 'gestion_commandes/utilisateur.html', context)

                    cree_utilisateur(nom=request.POST['nom'], prenom=request.POST['prenom'],
                                     mdp=request.POST['mdp'], email=request.POST['email'])
                    utilisateur = obtenir_utilisateur(nom_champ='email', valeur=request.POST['email'])
                    # On modifie les privilèges de l'utilisateur si on retrouve la valeur du checkbox dans la requête
                    if "estAdmin" in request.POST:
                        modifier_utilisateur(email=utilisateur.email, nom_champ='est_admin', nouvelle_valeur=True)

                    utilisateur_modifier = obtenir_utilisateur(nom_champ='email', valeur=utilisateur.email)

                    context = {"email": email_utilisateur, "message": "L'utilisateur a bien été créé !",
                               "creation": True, "utilisateur": utilisateur_modifier}

                    return render(request, 'gestion_commandes/utilisateur.html', context)

                context = {"email": email_utilisateur, "creation": True}
                return render(request, 'gestion_commandes/utilisateur.html', context)
            else:
                # status 403 + page template custom 403 | interdit
                return render(request, 'gestion_commandes/403.html', {"email": " "}, status=403)
    else:
        return redirect('authentification')


def deconnexion(request):
    """Views deconnexion (permet de ce déconnecter)"""
    if verifier_utilisateur_connecter(request):
        response = redirect('authentification')
        response.delete_cookie('email_utilisateur')
        response.delete_cookie('mdp_utilisateur')
        return response
    else:
        return redirect('index')


def error_403(request, exception):
    """Erreur 403"""
    context = {"email": " "}
    return render(request, 'gestion_commandes/403.html', context)


def error_404(request, exception):
    """Erreur 404"""
    context = {"email": " "}
    return render(request, 'gestion_commandes/404.html', context)


def error_500(request):
    """Erreur 500"""
    context = {"email": " "}
    return render(request, 'gestion_commandes/500.html', context)

import re
from decimal import Decimal

from gestion_commandes.shema_bd.categorie import obtenir_categories
from gestion_commandes.shema_bd.commande import obtenir_commandes, obtenir_commande
from gestion_commandes.shema_bd.produit import obtenir_produit
from gestion_commandes.shema_bd.utilisateur import obtenir_utilisateur


def valider_email(email):
    """Validation si le email est de 5 caractères et contient un @ et un .
       une liste des problème."""
    # La liste des problème du email.
    messages = []

    # validation si le email est de 5 caractères minimum.
    if len(email) < 5:
        messages.append("L'email doit avoir au moins 5 caractères.")

    # Validation si le email contient un @ et un point.
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    if not re.search(regex, email):
        messages.append("L'email doit contenir un '@' et un '.' et doit"
                        " ressembler à exemple@exemple.com.")

    # Validation que le email contient seulement des caractères autorisés.
    caractere_valide = True
    for char in email:
        # Vérification que le caractère est autorisé.
        if not (48 <= ord(char) <= 57 or ord(char) == 46
                or 64 <= ord(char) <= 90 or 97 <= ord(char) <= 122):
            caractere_valide = False

    if caractere_valide is False:
        messages.append("L'email contient un ou des caractères invalides.")

    # retourne la liste de messages
    return messages


def valider_email_existant(email):
    """Vérifie si le email est déja utilisé. Retourne True ou False."""
    try:
        utilisateur = obtenir_utilisateur(nom_champ='email', valeur=email)

        # Retourne True si l'email est déja utilisé.
        return True
    except:
        # Retourne False si l'email n'est pas utilisé.
        return False


def valider_mdp_identique(mdp1, mdp2):
    """Vérifie si les deux mots de passe sont identiques."""
    if mdp1 == mdp2:
        return True
    return False


def valider_utilisateur_login(email, mdp):
    """Validation si l'utilisateur à le bon identifiant."""
    if valider_email_existant(email):
        utilisateur = obtenir_utilisateur(nom_champ='email', valeur=email)
        if utilisateur.mdp == mdp and utilisateur.email == email:
            # L'email et le mdp sont correcte, retourne l'utilisateur.
            return utilisateur
        # email et mdp ne sont pas les bon, retourne False
        return False
    # L'email n'existe pas, retourne False
    return False


def valider_mdp(mdp):
    """Validation si le mdp est de la bonne forme."""
    messages = []
    # La taille du mot de passe est trop petite
    if len(mdp) < 1 or mdp is None:
        messages.append("Le mot de passe doit contenir au moins 1 caratère.")

    # Validation que le mot de passe contient seulement des caractères autorisés.
    caractere_valide = True
    for char in mdp:
        # Vérification que le caractère est autorisé.
        if not 33 <= ord(char) <= 126:
            caractere_valide = False

    if caractere_valide is False:
        messages.append("Le mot de passe contient un ou des caractères invalides.")

    return messages


def valider_nom(nom):
    """Validation si le nom est du bon format, retourne la liste des problèmes"""
    messages = []
    if not 1 <= len(nom) <= 50:
        messages.append("Le nom doit être entre 1 et 50 caractères.")

    # Validation que le nom contient seulement des caractères autorisés.
    caractere_valide = True
    for char in nom:
        # Vérification que le caractère est autorisé.
        if not (32 <= ord(char) <= 126 or 128 <= ord(char) <= 168 or 181 <= ord(char) <= 183
                or ord(char) == 192 or 198 <= ord(char) <= 201 or 208 <= ord(char) <= 216
                or ord(char) == 226 or ord(char) == 224 or 231 <= ord(char) <= 244):
            caractere_valide = False

    if caractere_valide is False:
        messages.append("Le nom contient un ou des caractères invalides.")

    return messages


def valider_prenom(prenom):
    """Validation si le prénom est du bon format, retourne la liste des problèmes"""
    messages = []
    if not 1 <= len(prenom) <= 50:
        messages.append("Le prénom doit être entre 1 et 50 caractères.")

    # Validation que le prénom contient seulement des caractères autorisés.
    caractere_valide = True
    for char in prenom:
        # Vérification que le caractère est autorisé.
        if not (32 <= ord(char) <= 126 or 128 <= ord(char) <= 168 or 181 <= ord(char) <= 183
                or ord(char) == 192 or 198 <= ord(char) <= 201 or 208 <= ord(char) <= 216
                or ord(char) == 226 or ord(char) == 224 or 231 <= ord(char) <= 244):
            caractere_valide = False

    if caractere_valide is False:
        messages.append("Le prénom contient un ou des caractères invalides.")

    return messages


def verifier_utilisateur_connecter(request):
    """Vérifier si l'utilisateur est connecté, retourne True ou False"""
    if request.COOKIES.get("email_utilisateur"):
        # Vérification que l'email de l'utilisateur connecté existe.
        if valider_email_existant(request.COOKIES.get("email_utilisateur")):
            if request.COOKIES.get("mdp_utilisateur"):
                # valider email et mdp
                if valider_utilisateur_login(request.COOKIES.get("email_utilisateur"),
                                             request.COOKIES.get("mdp_utilisateur")):
                    # Il y a un cookies avec un email et mdp valide donc il est connecter.
                    # Return true.
                    return True
    return False


def valider_est_admin(request):
    """Vérifie si l'utilisateur est admin, retourne True ou False"""
    email_utilisateur = request.COOKIES.get("email_utilisateur")
    utilisateur = obtenir_utilisateur(nom_champ='email', valeur=email_utilisateur)
    if utilisateur.est_admin is True:
        return True
    return False


def valider_nom_commande(nom_commande):
    """Vérification que le nom de la commande respecte bien les conditions."""
    # Vérification que la taille du nom est correct.
    if 1 <= len(nom_commande) <= 50:
        for char in nom_commande:
            # Vérification que le caractère est autorisé.
            if not (32 <= ord(char) <= 126 or 128 <= ord(char) <= 168 or 181 <= ord(char) <= 183
                    or ord(char) == 192 or 198 <= ord(char) <= 201 or 208 <= ord(char) <= 216
                    or ord(char) == 226 or ord(char) == 224 or 231 <= ord(char) <= 244):
                return False
        return True
    return False


def valider_utilisateur_acces_commande(id_commande, email_utilisateur):
    """Vérification si l'utilisateur à accès à la commande"""
    try:
        commande = obtenir_commande(id=id_commande)
        if commande.email_utilisateur == email_utilisateur:
            return True
    except:
        return False


def valider_commande_contient_produit(commande, id_relation_produit):
    """Vérifier si le produit est contenu dans la commande"""
    try:
        iteration = 0
        est_contenu = False
        une_relation = None
        while not est_contenu or iteration < len(commande.relation_produit):
            if str(commande.relation_produit[iteration].id) == id_relation_produit:
                est_contenu = True
                une_relation = commande.relation_produit[iteration]
            iteration += 1
        return une_relation
    except:
        return None


def verifier_produit_existe(nom):
    """Vérifie si le produit existe dans la base de donnée"""
    try:
        produit = obtenir_produit(nom_champ='nom', valeur=nom)

        # Retourne le produit si le produit est existant.
        return produit
    except:
        # Retourne None si le produit n'est pas existant.
        return None


def valider_description(description):
    """Validation si la description est de bon format, retourne la liste des problèmes"""
    messages = []
    if not 1 <= len(description) <= 250:
        messages.append("La description doit être entre 1 et 250 caractères.")

    # Validation que la description n'a que des caractères autorisé.
    caractere_valide = True
    for char in description:

        # Vérification que le caractère est autorisé.
        if not (32 <= ord(char) <= 126 or 128 <= ord(char) <= 168 or 181 <= ord(char) <= 183
                or ord(char) == 192 or 198 <= ord(char) <= 201 or 208 <= ord(char) <= 216
                or ord(char) == 226 or ord(char) == 224 or 231 <= ord(char) <= 244):
            caractere_valide = False

    if caractere_valide is False:
        messages.append("La description contient un ou des caractères non autorisés")

    return messages


def valider_prix(prix):
    """Validation du format du prix"""
    messages = []
    try:
        prix_converti = Decimal(prix)
        if prix_converti < 0:
            messages.append("Le prix ne peut pas être négatif.")
        return messages
    except:
        messages.append("Le format du prix n'est pas valide.")
        return messages


def valider_nom_produit(nom):
    """Validation si le nom du produit est du bon format, retourne la liste des problèmes"""
    messages = []
    if not 1 <= len(nom) <= 50:
        messages.append("Le nom du produit doit être entre 1 et 50 caractères.")

    # Validation que le nom contient seulement des caractères autorisés.
    caractere_valide = True
    for char in nom:
        # Vérification que le caractère est autorisé.
        if not (32 <= ord(char) <= 126 or 128 <= ord(char) <= 168 or 181 <= ord(char) <= 183
                or ord(char) == 192 or 198 <= ord(char) <= 201 or 208 <= ord(char) <= 216
                or ord(char) == 226 or ord(char) == 224 or 231 <= ord(char) <= 244):
            caractere_valide = False

    if caractere_valide is False:
        messages.append("Le nom contient un ou des caractères invalides.")

    return messages


def valider_categorie(categorie):
    """Validation du format de la catégorie, retourne la liste des problèmes"""
    messages = []
    if not 1 <= len(categorie) <= 50:
        messages.append("La catégorie est vide.")
    # On vérifie si la catégorie obtenu est contenu dans la liste des catégories
    categories = obtenir_categories()
    est_inclue = False
    for une_categorie in categories:
        if une_categorie.nom == categorie:
            est_inclue = True
    if not est_inclue:
        messages.append("La catégorie n'est pas une catégorie valide.")
    return messages

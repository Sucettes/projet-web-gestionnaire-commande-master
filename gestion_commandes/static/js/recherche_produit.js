'use strict'
var estCharger = false;
document.addEventListener('DOMContentLoaded', function (event) {
    estCharger = true
})
/**
* Évènment lors que la touche du clavier se releve (Lance la recherche).
*/
$('#recherche').keyup(function () {
    $('#suggestion').empty();
    $('#msg').empty();
    Recherche();
});
/**
* Évènment lors que la catégorie change (Lance la recherche).
*/
$('input[name="categorie"]').change(function () {
    $('#suggestion').empty();
    $('#msg').empty();
    Recherche();
});
/**
* Évènment lors du clique du bouton de la recherche (Lance la recherche).
*/
$('#rechercher').click(function () {
    $('#suggestion').empty();
    $('#msg').empty();
    Recherche();
});
/**
* Évènment lors du clique d'un résultat de la recherche (Ajoute le produit à la commande.).
*/
$("#suggestion").on("click", "a", function (event) {
    ajoutProduitCommande(event);
})
/**
* Message de confirmation de l'ajout.
*/
function messageAjout() {
    let message_ajout_obj = $('#message_ajout');
    let message_erreur_obj = $('#message_erreur');

    //On enleve le contenu des deux div messages
    message_ajout_obj.empty();
    message_erreur_obj.empty();
    // On ajoute la class none pour être sur de ne pas voir les deux messages en même temps.
    message_erreur_obj.addClass('none');
    message_ajout_obj.removeClass('none');

    let p = $("<p></p>").text("Le produit a bien été ajouté à la commande.");
    message_ajout_obj.append(p);

    setTimeout(function () {
        message_ajout_obj.addClass('none');
    }, 5000);
}
/**
* Message d'erreur d'un ajout.
*/
function messageErreur() {
    let message_ajout_obj = $('#message_ajout');
    let message_erreur_obj = $('#message_erreur');

    //On enleve le contenu des deux div messages
    message_ajout_obj.empty();
    message_erreur_obj.empty();
    // On ajoute la class none pour être sur de ne pas voir les deux messages en même temps.
    message_ajout_obj.addClass('none');
    message_erreur_obj.removeClass('none');

    let p = $("<p></p>").text("Le produit n'a pas pu être ajouté ! Une erreur est survenue.");
    message_erreur_obj.append(p);

    setTimeout(function () {
        message_erreur_obj.addClass('none');
    }, 5000);
}
/**
* Ajout d'un produit à la commande.
*/
function ajoutProduitCommande(event) {
    let data = {};
    // Permet de géré l'exception 404 lors du chargement.
    if (event.target.id !== "") {
        data = {'nom_produit': event.target.id}
    } else {
        data = {'nom_produit': event.target.parentElement.id}
    }
    $.ajax({
        type: 'PUT',
        url: window.location.pathname,
        data: data,
        dataType: 'json',
        success: function (status, jqXHR) {
            if (status === 200) {
                messageAjout();
            } else {
                messageErreur();
            }
        },
        error: function (jqXHR, status, error) {
            alert("La commande avec laquelle vous tentez d'interagir a subi une erreur!" +
            "Vous allez être redirigé sur la page principale.");
            location.replace("/");
        }
    })
}
/**
* Recherche des produits.
*/
function Recherche() {
    let categorie = $('input[name="categorie"]:checked').val();
    let champsRechercher = $('#recherche').val();

    if (champsRechercher.length >= 1 && categorie !== undefined && categorie.length >= 1) {
        let data = {'nom': champsRechercher, 'cat': categorie}
        $.ajax({
            type: 'GET',
            url: '/recherche_produits/',
            data: data,
            contentType: "application/json",
            dataType: 'json',
            success: function (produits) {
                if (produits.length === 0) {
                    let a = document.createElement('a');
                    a.className = 'list-group-item list-group-item-action list-group-item-warning';
                    a.innerHTML = "Aucun produit ne correspond à cette recherche!";
                    $('#msg').append(a);
                }
                produits.forEach(produit => {
                    let a = document.createElement('a');
                    let span = document.createElement('span');
                    let p = document.createElement('p');
                    span.className = 'plus';
                    span.innerHTML = '<b>Ajouter</b>';
                    p.innerHTML = '<b>' + produit.nom + '</b> | <b>' + produit.prix + '$</b>  | ' + produit.description;
                    a.className = 'list-group-item list-group-item-info produit produit-ajouter';
                    a.id = produit.nom;
                    a.append(span);
                    a.append(p)
                    $('#suggestion').append(a);
                })
            },
            error: function () {
                alert("Un problème est survenu ! Vous allez être redirigé vers la page principale.");
                location.replace("/");
            }
        });
    }
}
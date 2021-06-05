'use strict'
var nom_produit = $('input[name="nom"]').val();
var prix_produit = $('input[name="prix"]').val();
var description_produit = $('input[name="description"]').val();
var categorie_produit = $('input[name="categorie"]:checked').attr("id");
var en_stock_produit = $('input[name="en_stock"]:checked').val();
/**
* Évènment lors du click du bouton reset.
*/
$('#reset').click(function () {
    $('input[name="nom"]').val(nom_produit);
    $('input[name="prix"]').val(prix_produit);
    $('input[name="description"]').val(description_produit);
    $('#' + categorie_produit).prop('checked', true);
    if (en_stock_produit === undefined) {
        $('input[name="en_stock"]').val(en_stock_produit).prop('checked', false);
    } else {
        $('input[name="en_stock"]').val(en_stock_produit).prop('checked', true);
    }
});
/**
* Évènment lors du click du bouton modifier.
*/
$('#modifier').click(function () {
    $('#msg_error').addClass('none');
    $('#msg_success').addClass('none');
    $('#msg_error').empty();
    $('#msg_success').empty();

    modification_produit();
});
/**
* Modification du produit.
*/
function modification_produit() {
    const categorie = $('input[name="categorie"]:checked');
    const en_stock = $('input[name="en_stock"]:checked').val();
    const prix = $('input[name="prix"]').val();
    const desc = $('input[name="description"]').val();
    const nom = $('input[name="nom"]').val();
    let data = {'nom': nom, 'prix': prix, 'desc': desc, 'en_stock': en_stock, 'categorie': categorie.val()}
    $.ajax({
        type: 'PUT',
        url: window.location.pathname,
        data: data,
        contentType: "application/json",
        dataType: 'json',
        success: function (lstMessages) {
            $('#msg_error').empty();
            $('#msg_success').empty();
            $('#msg_error').addClass('none');
            if (lstMessages.length > 0) {
                $('#msg_error').removeClass('none');
                for (let i = 0; i < lstMessages.length; i++) {
                    let p = $("<p></p>").text(lstMessages[i].message);
                    $('#msg_error').append(p);
                }
                setTimeout(function () {
                    $('#msg_error').addClass('none');
                }, 5000);
            } else {
                nom_produit = data.nom;
                prix_produit = data.prix;
                description_produit = data.desc;
                categorie_produit = categorie.attr("id");
                en_stock_produit = data.en_stock;
                message_modif();
            }
        },
        error: function (jqXHR, status, error) {
            alert("Le produit avec lequel vous tentez d'interagir a subi une erreur!" +
                "\n Vous allez être redirigé sur la page principale.");
            location.replace("/admin/produits/");
        }
    })
}
/**
* Message lorsque la modification fonctionne.
*/
function message_modif() {
    $('#msg_success').empty();
    $('#msg_error').empty();
    $('#msg_success').removeClass('none');
    let p = $("<p></p>").text("Les modifications ont bien été apportées.");
    $('#msg_success').append(p);
    setTimeout(function () {
        $('#msg_success').addClass('none');
    }, 5000);
}
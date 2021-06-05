'use strict'
/**
* Évènement du clique pour supprimer une commande.
*/
$('#supprimer_commande').click(function () {
    let id = {'id': $('#id').val()}
    $.ajax({
        type: 'DELETE',
        url: window.location.pathname,
        data: id,
        contentType: "application/json",
        success: function () {
            retour_success();
        },
        error: function () {
            suppression_erreur();
        }
    })
});
/**
* Message lorsque la suppression fonctionne.
*/
function retour_success() {
    $('#msg_suppression').empty();
    $('#msg_suppression').removeClass('none');
    $('#msg_suppression').addClass('alert-success');
    let p = $("<p></p>").text("La commande a bien été supprimée.\n" +
        "Vous allez être redirigé vers la page d'accueil dans 5 secondes.");
    $('#msg_suppression').append(p);
    setTimeout(function () {
        location.replace("/");
    }, 5000);
}
/**
* Message lorsque la suppression ne fonctionne pas.
*/
function suppression_erreur() {
    $('#msg_suppression').empty();
    $('#msg_suppression').removeClass('none');
    $('#msg_suppression').addClass('alert-danger');
    let p = $("<p></p>").text("La suppression n'a pas fonctionné.");
    $('#msg_suppression').append(p);
}


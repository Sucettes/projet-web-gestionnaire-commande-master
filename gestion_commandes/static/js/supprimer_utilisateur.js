'use strict'
/**
* Évènement du clique bouton de suppression
*/
$('#supprimer_utilisateur').click(function () {
    let email = {'email': $('#email').val()}
    $.ajax({
        type: 'DELETE',
        url: window.location.pathname,
        data: email,
        contentType: "application/json",
        success: function () {
            retour_admin_success();
        },
        error: function () {
            suppression_erreur();
        }
    })
});
/**
* Message lorsque l'utilisateur à bien été supprimé
*/
function retour_admin_success() {
    $('#msg_supprimer').empty();
    $('#msg_supprimer').removeClass('none');
    $('#msg_supprimer').addClass('alert-success');
    let p = $("<p></p>").text("Le compte a bien été supprimé.\n" +
        "Vous allez être redirigé vers la page administrateur dans 5 secondes.");
    $('#msg_supprimer').append(p);
    setTimeout(function () {
        window.location.href = '/admin/';
    }, 5000);
}
/**
* Message lorsque l'utilisateur n'à pas bien été supprimé.
*/
function suppression_erreur() {
    $('#msg_supprimer').empty();
    $('#msg_supprimer').removeClass('none');
    $('#msg_supprimer').addClass('alert-danger');
    let p = $("<p></p>").text("La suppression n'a pas fonctionné! Vous ne pouvez pas vous supprimer vous-même !");
    $('#msg_supprimer').append(p);
    setTimeout(function () {
        $('#msg_supprimer').addClass('none');
    }, 5000);
}



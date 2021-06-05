'use strict'
var nom_utilisateur = $('input[name="nom"]').val();
var prenom_utilisateur = $('input[name="prenom"]').val();
var mdp_utilisateur = $('input[name="mdp"]').val();
var mdp_conf_utilisateur = $('input[name="mdpConf"]').val();
var est_admin_utilisateur = $('input[name="estAdmin"]:checked').val();

/**
* Évènement lors du click du bouton réinitialiser.
*/
$('#reset').click(function () {
    $('input[name="nom"]').val(nom_utilisateur);
    $('input[name="prenom"]').val(prenom_utilisateur);
    $('input[name="mdpConf"]').val(mdp_conf_utilisateur);
    $('input[name="mdp"]').val(mdp_utilisateur);
    if (est_admin_utilisateur == undefined) {
        $('input[name="estAdmin"]').val(est_admin_utilisateur).prop('checked', false);
    } else {
        $('input[name="estAdmin"]').val(est_admin_utilisateur).prop('checked', true);
    }
});
/**
* Évènement lors du click de la modification
*/
$('#modifier').click(function () {
    $('#msg_error').addClass('none');
    $('#msg_success').addClass('none');
    $('#msg_error').empty();
    $('#msg_success').empty();

    modification_utilisateur();
});

/**
* Modification de l'utilisateur.
*/
function modification_utilisateur() {
    const nom = $('input[name="nom"]').val();
    const prenom = $('input[name="prenom"]').val();
    const mdp = $('input[name="mdp"]').val();
    const mdp_conf = $('input[name="mdpConf"]').val();
    const est_admin = $('input[name="estAdmin"]:checked').val();
    let data = {'nom': nom, 'prenom': prenom, 'mdp': mdp, 'mdpConf': mdp_conf, 'estAdmin': est_admin}
    $.ajax({
        type: 'PUT',
        url: window.location.pathname,
        data: data,
        contentType: "application/json",
        dataType: 'json',
        success: function (lstMessages, status, jqXHR) {
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
                nom_utilisateur = data.nom;
                prenom_utilisateur = data.prenom;
                mdp_utilisateur = data.mdp;
                mdp_conf_utilisateur = data.mdpConf
                est_admin_utilisateur = data.estAdmin;
                message_modif();
            }
        },
        error: function (jqXHR, status, error) {
            alert("L'utilisateur avec lequel vous tentez d'interagir a subi une erreur!" +
                "\n Vous allez être redirigé sur la page principale.");
            location.replace("/admin/");
        }
    })
}

/**
* Message lorsque la modification fonctionne.
*/
function message_modif() {
    $('#msg_success').empty();
    $('#msg_success').removeClass('none');
    let p = $("<p></p>").text("Les modifications ont bien été apportées.");
    $('#msg_success').append(p);
    setTimeout(function () {
        $('#msg_success').addClass('none');
    }, 5000);
}
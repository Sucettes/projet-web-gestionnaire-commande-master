'use strict'
var nom_formulaire = $('input[name="nom"]').val();
/**
* Évènment lors du click du bouton reset.
*/
$('#reset').click(function () {
    $('input[name="nom"]').val(nom_formulaire);
});
/**
* Évènment lors du click du bouton modifier.
*/
$('#modifier').click(function () {
    if ($('input[name="nom"]').val() !== nom_formulaire) {
        $('#msg_error').addClass('none');
        $('#msg_success').addClass('none');
        $('#msg_error').empty();
        $('#msg_success').empty();

        modification_commande();
    } else {
        $('#msg_success').empty();
        $('#msg_error').empty();
        $('#msg_error').removeClass('none');
        let p = $("<p></p>").text("Aucune modification détectée dans le nom.");
        $('#msg_error').append(p);

        setTimeout(function () {
            $('#msg_error').addClass('none');
        }, 5000);
    }
});
/**
* Modification de la commande.
*/
function modification_commande() {
    const nom = $('input[name="nom"]').val();
    let data = {'nom': nom}
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
                nom_formulaire = data.nom;
                message_modif();
            }
        },
        error: function () {
            alert("La commande avec laquelle vous tentez d'interagir a subi une erreur!"+
            "/nVous allez être redirigé sur la page principale.");
            window.location.replace("/");
        }
    });
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
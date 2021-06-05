'use strict'
/**
* Évènment lors du click du bouton voir plus de la carte.
*/
$('a#btn_plus_moins').click(function (event) {
    let btn_plus_moins = event.currentTarget;
    let carte = btn_plus_moins.parentElement.parentElement;
    let plus_texte = carte.getElementsByClassName("plus")[0];

    if (btn_plus_moins.innerText === "Voir Moins") {
        btn_plus_moins.innerText = "Voir Plus";
        plus_texte.style.display = "none";
        carte.className = "carte-commande";
    } else {
        btn_plus_moins.innerText = "Voir Moins";
        plus_texte.style.display = "inline";
        carte.className = "carte-commande extend";
    }
});
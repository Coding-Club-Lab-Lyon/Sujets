var argent = 0,
    fours = 1,
    cuistots = 0;

var prix_four = 50,
    prix_cuistot = 1000;

function cuisiner() {
    var score = document.getElementById("score");
    argent += fours
    score.innerText = argent + "$"
}

function acheterFour() {
    var score = document.getElementById("score");
    var button = document.querySelector("#four > button")
    if (argent < prix_four)
        return;
    argent -= prix_four;
    fours++;
    prix_four *= 1.5
    prix_four = parseInt(prix_four)
    score.innerText = argent + "$"
    button.innerText = "Acheter un four (" + prix_four + "$)"
}

function acheterCuistot() {
    var score = document.getElementById("score");
    var button = document.querySelector("#cuistot > button")
    if (argent < prix_cuistot)
        return;
    argent -= prix_cuistot;
    cuistots++;
    prix_cuistot *= 1.5
    prix_cuistot = parseInt(prix_cuistot)
    score.innerText = argent + "$"
    button.innerText = "Acheter un cuistot (" + prix_cuistot + "$)"
}


setInterval(function () {
    var score = document.getElementById("score");
    argent += cuistots
    score.innerText = argent + "$"
}, 1000)

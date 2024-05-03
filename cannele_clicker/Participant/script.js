var argent = 0;
var fours = 0;

function cuisiner() {
    var score = document.getElementById("score");

    argent += fours;

    score.innerText = argent + "€";
}

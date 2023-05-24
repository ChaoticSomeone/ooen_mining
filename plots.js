function clamp(val, min, max){
    if (val < min){return min;}
    if (val > max){return max;}
    return val;
}

function main(){
    let imgConatiner = document.getElementById("imgContainer");
    let buttonNext = document.getElementById("next");
    let buttonPrev = document.getElementById("prev");
    let plot = imgConatiner.querySelector("#plot")
    let i = 0;
    let plots = [
        ["../img/releases.png", "Grafik zu Erscheinungszeiten"],
        ["../img/dt.png", "Grafik zu Zeitdifferenz"],
        ["../img/ressorts.png", "Grafik zu Ressorts"],
        ["../img/ressort_t.png", "Grafik zu Ressorts pro Zeit"],
        ["../img/comments.png", "Grafik zu Kommentaren pro Zeit"]
    ]

    buttonNext.addEventListener("click", function (){
        i = clamp(i + 1, 0, 4);
        plot.setAttribute("src", plots[i][0]);
        plot.setAttribute("alt", plots[i][1]);
    });
    buttonPrev.addEventListener("click", function (){
        i = clamp(i - 1, 0, 4);
        plot.setAttribute("src", plots[i][0]);
        plot.setAttribute("alt", plots[i][1]);
    });
}

window.onload = main;
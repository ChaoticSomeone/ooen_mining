
// Loads the content of a json-file from the file system
async function loadJSON(path) {
    const res = await fetch(path)
    return await res.json();
}

// Function for clamping numbers
function clamp(val, min, max){
    if (val < min){return min;}
    if (val > max){return max;}
    return val;
}

// Returns a string formatted with the data of given article
function fmtArticle(art, iter){
    let text =
        `<b style="color:#BB86FC;">${art}</b><br>` +
        `<span>Erschienen am ${iter[art]["date"] === "unknown" ? "???" : iter[art]["date"]} um ${iter[art]["time"]} im Ressort '${iter[art]["ressort"] === "keine Angabe" ? "???" : iter[art]["ressort"]}'.</span><br>`+
        `<span>Der Artikel wurde von ${iter[art]["author"].includes("Mai") || iter[art]["author"] === "unknown" ? "???" : iter[art]["author"]} verfasst und ist ${iter[art]["isPremium"] ? "kostenpflichtig" : "kostenlos"}.</span><br>`+
        `<span>Der Artikel wurde ${iter[art]["comments"]}-mal kommentiert.</span>`;
    return text;
}

// Show data of the current article
function showArticles(obj){
    let i = 1;
    let articles = Object.keys(obj);
    let container = document.getElementById("article-section").querySelector("#container");
    let buttonNext = document.getElementById("article-section").querySelector("#next");
    let buttonPrev = document.getElementById("article-section").querySelector("#prev");
    let buttonRand = document.getElementById("article-section").querySelector("#rand");
    let buttonRst = document.getElementById("article-section").querySelector("#rst");
    container.innerHTML = fmtArticle(articles[0], obj);

    let amount = articles.length;
    buttonNext.addEventListener("click", function (){
        i = clamp(i + 1, 0, amount);
        container.innerHTML = fmtArticle(articles[i], obj);
    });

    buttonPrev.addEventListener("click", function (){
        i = clamp(i - 1, 0, amount);
        container.innerHTML = fmtArticle(articles[i], obj);
    });

    buttonRand.addEventListener("click", function (){
        i = Math.floor(Math.random() * (amount+1));
        container.innerHTML = fmtArticle(articles[i], obj);
    });

    buttonRst.addEventListener("click", function (){
       i = 0;
       container.innerHTML = fmtArticle(articles[i], obj);
    });
}

// Main (also: isn't this comment quite pointless?)
function main(){
    let data = loadJSON("../data.json");
    data.then(
        function (value) {showArticles(value)},
        function (error) {
            document.getElementById("article-section").querySelector("#container").innerText = "Irgendwas ist schiefgelaufen!";
        }
    );
}

window.onload = main;
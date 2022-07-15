import Timer from "./timer.js";
import Mindfulness from "./mindfulness.js";


let reverseTimer = true;

const timerButton = document.getElementById("timerButton");

if (timerButton.addEventListener)
    timerButton.addEventListener("click", buildTimer, false);
else if (timerButton.attatchEvent)
    timerButton.attachEvent("onclick", buildTimer);


function buildTimer() {

    if (reverseTimer) {
        new Timer(document.querySelector(".module__timer"));
    } else {
        document.querySelector(".module__timer").textContent = "";
    }

    reverseTimer = !reverseTimer;
}

let reverseMindful = true;

const mindfulButton = document.getElementById("mindfulButton");

if (mindfulButton.addEventListener)
    mindfulButton.addEventListener("click", buildMindfulness, false);
else if (mindfulButton.attatchEvent)
    mindfulButton.attachEvent("onclick", buildMindfulness);


function buildMindfulness() {

    if (reverseMindful) {
        new Mindfulness(document.querySelector(".module__mindfulness"));
    } else {
        document.querySelector(".mindfulness__container").textContent = "";
        document.querySelector(".module__mindfulness").textContent = "";
    }

    reverseMindful = !reverseMindful;
}





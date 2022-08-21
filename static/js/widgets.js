// Time and Date Widget

const dateTime = document.getElementById("dateTime")

const event = new Date();
const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };

dateTime.innerHTML = event.toLocaleDateString(undefined, options);

// Widget Buttons

const widgetBtn = document.querySelector(".widget__btn")
const widgetBar = document.querySelector(".widget__bar")
const widgetSelection = document.querySelector(".widget__extender")

widgetBtn.addEventListener("click", () => {
    if (widgetSelection.style.display === "none") {
        widgetSelection.style.display = "flex"
        widgetBar.style.height = "12rem"
    } else {
        widgetSelection.style.display = "none"
        widgetBar.style.height = "4rem"
    }
})

// import Timer from "./timer.js";
import Mindfulness from "./mindfulness.js";
import Timer from "./timer.js";
import Todo from "./todo.js";

new Timer(document.body)
new Mindfulness(document.body)
new Todo(document.body)

const timerContainer = document.querySelector(".timer__container")
const mindfulnessContainer = document.querySelector(".mindfulness__container")
const todoContainer = document.querySelector(".todo__container")


document.getElementById('timerBtn').addEventListener('click', () => {

    timerContainer.style.display = "flex"

})
document.getElementById('mindfulnessBtn').addEventListener('click', () => {

    mindfulnessContainer.style.display = "flex"
})
document.getElementById('todoBtn').addEventListener('click', () => {

    if (todoContainer.style.display === "none") {
        todoContainer.style.display === "inline"
    } else {
        todoContainer.style.display === "none"
    }

})
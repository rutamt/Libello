// Time and Date Widget

const dateTime = document.getElementById("dateTime")

const event = new Date();
const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };

dateTime.innerHTML = event.toLocaleDateString(undefined, options);

// Widget Buttons

const widgetBtn = document.querySelector(".widget__btn")
const widgetPlus = document.querySelector(".plus")
const widgetBar = document.querySelector(".widget__bar")
const widgetSelection = document.querySelector(".widget__extender")

let isOpen = false

widgetBtn.addEventListener("click", () => {
    widgetPlus.classList.toggle("spin")
    if (isOpen) {
        widgetBar.classList.remove("widget__bar--extend")
        widgetBar.classList.add("widget__bar--retract")
        isOpen = !isOpen
    } else {
        widgetBar.classList.remove("widget__bar--retract")
        widgetBar.classList.add("widget__bar--extend")
        isOpen = !isOpen
    }
})

// import Widget Modules
import Mindfulness from "./mindfulness.js";
import Timer from "./timer.js";
import Todo from "./todo.js";

// Create widgets from those modules
new Timer(document.body)
new Mindfulness(document.body)
new Todo(document.body)

// Define the base of those widgets
const timerContainer = document.querySelector(".timer__container")
const mindfulnessContainer = document.querySelector(".mindfulness__container")
const todoContainer = document.querySelector(".todo__container")

// Add buttons to flick them visible and invisible

// Timer
document.getElementById('timerBtn').addEventListener('click', () => {

    timerContainer.style.display = "flex"

})

// Mindfulness
document.getElementById('mindfulnessBtn').addEventListener('click', () => {

    mindfulnessContainer.style.display = "flex"
})

// Todo List
let openTodo = false;

document.getElementById('todoBtn').addEventListener('click', () => {

    if (openTodo) {
        todoContainer.style.display = "none"
    } else {
        todoContainer.style.display = "inline"
    }
    openTodo = !openTodo
})
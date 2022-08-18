// Time and Date Widget

const dateTime = document.getElementById("dateTime")

const event = new Date();
const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };

dateTime.innerHTML = event.toLocaleDateString(undefined, options);

// import Timer from "./timer.js";
import Mindfulness from "./mindfulness.js";
import Timer from "./timer.js";
import Todo from "./todo.js";

// new Timer(document.body)
// new Mindfulness(document.body)
// new Todo(document.body)

let timerIsHere = false;
let mindfulnessIsHere = false;
let todoIsHere = false;

// document.getElementById('timerBtn').addEventListener('click', () => {

//     if (timerIsHere) {
//         document.remove()
//         timerIsHere = false
//     } else {
//         new Timer(document.querySelector('#widgetBar'))
//         timerIsHere = true
//     }

// })
// document.getElementById('mindfulnessBtn').addEventListener('click', () => {

//     if (mindfulnessIsHere) {
//         document.remove()
//         mindfulnessIsHere = false
//     } else {
//         new Mindfulness(document.querySelector('#widgetBar'))
//         mindfulnessIsHere = true
//     }

// })
// document.getElementById('todoBtn').addEventListener('click', () => {

//     if (todoIsHere) {
//         document.remove()
//         todoIsHere = false
//     } else {
//         new Todo(document.querySelector('#widgetBar'))
//         todoIsHere = true
//     }

// })
const class__container = document.getElementById("assignment-menu");

function saveData() {

}

function addClassElement(id, header, children) {
    const element = document.createElement("div");
    element.classList.add("card", "flex-fill");

    const cardHeader = element.createElement("div");
    cardHeader.classList.add("card-header", "container-card__header");

    const headerText = cardHeader.createElement("textarea")
    headerText.classList.add("header-text", "card-text", "container-card__header--text", "header-text--primary");
    headerText.value = header;
    headerText.placeholder = "Class Name";

    const cardBody = element.createElement("div");



}
function updateClass() {

}
function removeClass() {

}

function addAssignment() {

}
function updateAssignment() {

}
function removeAssignment() {

}
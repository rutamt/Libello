// Add Class Button
const form = document.querySelector(".input__wrapper");
let interval = 1


document.querySelector(".btn__control--add").addEventListener("click", () => {
    addParameter()
})
document.querySelector(".btn__control--remove").addEventListener("click", () => {
    removeParameter()
})

function addParameter() {
    interval++
    var input = document.createElement('input');
    input.type = "number";
    input.className = "form-control";
    input.placeholder = "Type in Class ID";
    input.required = true;
    input.name = "classes";
    form.appendChild(input);
}

function removeParameter() {
    if (interval > 0) {
        form.removeChild(form.lastElementChild)
        interval--
    }
}

// Guide Btn

const guideBtn = document.querySelector(".guide__Btn")
const guide = document.querySelector(".guide")

let isOpen = false

guideBtn.addEventListener("click", () => {
    if (isOpen) {
        guide.style.display = "none"
    } else {
        guide.style.display = "inline"
    }
    isOpen = !isOpen
})
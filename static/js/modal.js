const modals = document.querySelectorAll(".modal")
const btn = document.querySelectorAll(".modal__Btn")
const spans = document.getElementsByClassName("close")

for (var i = 0; i < btn.length; i++) {
    btn[i].addEventListener("click", (e) => {
        e.preventDefault()
        modal = document.querySelector(e.target.getAttribute("href"))
        console.log(modal)
        modal.style.display = "block"
    })
}

for (var i = 0; i < spans.length; i++) {
    spans[i].addEventListener("click", () => {
        for (var index in modals) {
            if (typeof modals[index].style !== 'undefined') modals[index].style.display = "none"
        }
    })
}

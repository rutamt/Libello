const modal = document.querySelector(".modal");
const btn = document.querySelector(".modal__Btn");
const span = document.querySelector(".close");

span.addEventListener("click", () => {
    modal.style.display = "none";
    modalOL.style.display = "none";
})

window.addEventListener("click", (event) => {
    if (event.target == modal) {
        modal.style.display = "none";
        modalOL.style.display = "none";
    }
})

btn.addEventListener("click", () => {
    modal.style.display = "initial";
    modalOL.style.display = "initial";
})

modalOL.style.display = "none";
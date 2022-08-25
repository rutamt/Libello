// Navbar Functions
// https://stackoverflow.com/questions/19900953/trying-to-trigger-event-on-certain-scroll-height-using-javascript

const navbar = document.querySelector(".navbar")
const navBrand = document.querySelector(".navbar-brand")
const navText = document.querySelector(".nav-link")
const collapse = document.querySelector(".collapse")

let isActive = false


scrollCheck()

window.addEventListener("scroll", () => scrollCheck())

document.querySelector(".navbar-toggler").addEventListener("click", () => {
    navbar.style.backgroundColor = '#FAF9F6'
    navBrand.classList.add("gradient-text")
    navText.style.color = '#4878D4'
    isActive = !isActive
})

// CHANGE THE COLORSS !!!(!(!)(!(!)(!())(!)))
function scrollCheck() {
    if (window.scrollY > 0) {
        navbar.style.backgroundColor = '#FAF9F6'
        navBrand.classList.add("gradient-text")
        navText.style.color = '#4878D4'
    } else if (window.scrollY === 0 && isActive === false) {
        navbar.style.background = 'transparent'
        navBrand.classList.remove("gradient-text")
        navBrand.style.color = '#FAF9F6'
        navText.style.color = '#FAF9F6'
    }
}
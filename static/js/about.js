// Spinning Gradient

const body = document.body

window.addEventListener("scroll", () => scrollDifference())

function scrollDifference() {
    let winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    let height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    let scrolled = (winScroll / height) * 360;

    body.style.background = `linear-gradient(${scrolled}deg, #594AFF 0%, #3377FD 100%)`
}

// Parallax

const header = document.querySelector(".header-wrapper .spec-text")

window.addEventListener("scroll", () => scrollMove())

function scrollMove() {
    header.style.transform = `translateY(-${window.scrollY / 1.25}px)`
}
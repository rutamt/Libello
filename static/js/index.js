const containerHide = document.querySelector(".title-wrapper .row")

scrollMove()

window.addEventListener("scroll", () => scrollMove())

function scrollMove() {
  containerHide.style.transform = `translateY(${window.scrollY/1.25}px)`
}

// https://www.w3schools.com/howto/howto_js_scroll_indicator.asp
window.onscroll = () => progressBar();

function progressBar() {
  var winScroll = document.body.scrollTop || document.documentElement.scrollTop;
  var height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
  var scrolled = (winScroll / height) * 100;
  document.getElementById("myBar").style.width = `${scrolled}%`;
}
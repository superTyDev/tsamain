// DEFINITIONS AND ELEMENTS
var header = document.getElementsByTagName("header")[0];

var slideIndex = 1;
var slideInterval = setInterval(nextSlide, 1000);
showSlides(slideIndex);

window.addEventListener("resize", placeNav);
navbar.onload = setTimeout(placeNav, 300);

// NAVBAR
function placeNav() {
    header.style.minHeight =
        (window.innerHeight - navbar.offsetHeight).toString() + "px";
    sticky = window.innerHeight - navbar.offsetHeight - 5;
}

// SLIDESHOW
function nextSlide() {
    showSlides((slideIndex += 1));
}

function showSlides(n) {
    var i;
    var slides = document.getElementsByClassName("slide");
    var slideCards = document.getElementsByClassName("slide-card-inner");
    if (n > slides.length) {
        slideIndex = 1;
    }
    if (n < 1) {
        slideIndex = slides.length;
    }
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
        slideCards[i].style.display = "none";
    }
    slides[slideIndex - 1].style.display = "block";
    slideCards[slideIndex - 1].style.display = "block";

    clearInterval(slideInterval);
    slideInterval = setInterval(nextSlide, 5000);
}

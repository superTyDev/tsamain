// Get the navbar
var navbar = document.getElementsByTagName("nav")[0];
var header = document.getElementsByTagName("header")[0];
var theme = document.getElementById("theme");
var sticky = navbar.offsetTop;

var slideIndex = 1;
var slideInterval = setInterval(nextSlide, 1000);

window.onscroll = function () {
	stickyNav();
};
window.addEventListener("resize", placeNav);
window.onload = setTimeout(placeNav, 300);

// Get the offset position of the navbar
function placeNav(event) {
	header.style.height =
		(window.innerHeight - navbar.offsetHeight).toString() + "px";
	sticky = window.innerHeight - navbar.offsetHeight - 5;
}

// Add the sticky class to the navbar when you reach its scroll position. Remove "sticky" when you leave the scroll position
function stickyNav() {
	if (window.pageYOffset >= sticky) {
		navbar.classList.add("sticky");
	} else {
		navbar.classList.remove("sticky");
	}

	if (window.pageYOffset == 0) {
		navbar.classList.remove("shrink");
	} else {
		navbar.classList.add("shrink");
	}
	if (window.pageYOffset <= 200) {
		navbar.classList.add("reverse");
	} else {
		navbar.classList.remove("reverse");
	}
}

function responsiveNavbar() {
	if (navbar.classList.contains("responsive")) {
		navbar.classList.remove("responsive");
	} else {
		navbar.classList.add("responsive");
	}
}

showSlides(slideIndex);

function nextSlide() {
	showSlides((slideIndex += 1));
}

function showSlides(n) {
	var i;
	var slides = document.getElementsByClassName("slide");
	if (n > slides.length) {
		slideIndex = 1;
	}
	if (n < 1) {
		slideIndex = slides.length;
	}
	for (i = 0; i < slides.length; i++) {
		slides[i].style.display = "none";
	}
	slides[slideIndex - 1].style.display = "block";

	clearInterval(slideInterval);
	slideInterval = setInterval(nextSlide, 5000);
}

// function to set a given theme/color-scheme
function setTheme(themeName) {
	localStorage.setItem("theme", themeName);
	document.documentElement.className = themeName;
	theme.value = themeName;
}

(function () {
	if (localStorage.getItem("theme") === "theme-light") {
		setTheme("theme-light");
	} else if (localStorage.getItem("theme") === "theme-contrast") {
		setTheme("theme-contrast");
	} else {
		setTheme("theme-dark");
	}
})();

function validateForm() {
	var x = document.forms["myForm"]["fname"].value;
	if (x == "") {
		alert("Name must be filled out");
		return false;
	}
}

// Get the navbar
var navbar = document.getElementsByTagName("nav")[0];
var theme = document.getElementById("theme");
var sticky = navbar.offsetTop;

window.onscroll = function () {
	stickyNav();
};

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

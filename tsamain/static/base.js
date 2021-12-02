// DEFINITIONS AND ELEMENTS
var navbar = document.getElementsByTagName("nav")[0];
var theme = document.getElementById("theme");
var sticky = navbar.offsetTop;

window.onscroll = function () {
	stickyNav();
};

// NAVBAR
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
	if (window.pageYOffset <= 200 && navbar.getBoundingClientRect().top != 0) {
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

// THEME
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

// FORM
function validateForm() {
	var x = document.forms["myForm"]["fname"].value;
	if (x == "") {
		alert("Name must be filled out");
		return false;
	}
}

// DEFINITIONS AND ELEMENTS
var navbar = document.getElementsByTagName("nav")[0];
var main = document.getElementsByTagName("main")[0];
var theme = document.getElementById("theme");
var sticky = navbar.offsetTop;
var footer = document.getElementsByTagName("footer")[0];

window.onload = function () {
	placeFooter();
	stickyNav();
};
window.onscroll = stickyNav;
setTimeout(stickyNav, 500);

// NAVBAR
function stickyNav() {
	if (window.pageYOffset >= sticky) {
		navbar.classList.add("sticky");
		main.classList.add("extra");
	} else {
		navbar.classList.remove("sticky");
		main.classList.remove("extra");
	}

	if (
		window.pageYOffset == 0 &&
		document.getElementsByTagName("header").length != 0
	) {
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

// PUSH TO MESSAGES
function pushMessage(message) {
	document.getElementsByClassName(
		"messages"
	)[0].innerHTML += `<div class="flash" onclick="this.style.display='none'">${message}</div >`;
}

// FOOTER
function placeFooter() {
	main.style.minHeight = window.innerHeight - footer.offsetHeight + "px";
}

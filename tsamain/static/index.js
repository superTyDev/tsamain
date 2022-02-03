<<<<<<< HEAD
// DEFINITIONS AND ELEMENTS
var header = document.getElementsByTagName("header")[0];
var slides = document.getElementsByClassName("slide");
var slideCards = document.getElementsByClassName("slide-card-inner");

var slideIndex = 1;
var slideInterval = setInterval(nextSlide, 1000);
showSlides(slideIndex);

window.addEventListener("resize", placeNav);
document.body.onload = function () {
	for (var i = 0; i < slideCards.length; i++) {
		startTimer(slideCards[i].getElementsByClassName("slide-time")[0]);
	}
	setTimeout(placeNav, 300);
	animateHTML().init();
};

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
	if (slideCards.length) {
		if (n > slideCards.length) {
			slideIndex = 1;
		}
		if (n < 1) {
			slideIndex = slideCards.length;
		}
		for (var i = 0; i < slideCards.length; i++) {
			slides[i].style.display = "none";
			slideCards[i].style.display = "none";
		}
		slides[slideIndex - 1].style.display = "block";
		slideCards[slideIndex - 1].style.display = "block";

		clearInterval(slideInterval);
		slideInterval = setInterval(nextSlide, 5000);
	}
}

// COUNTDOWN TIMER
function startTimer(display) {
	var timer =
		new Date(display.innerHTML.replace("UPCOMMING - ", "")) - new Date();

	timer = new Date(timer - 1000);

	display.textContent =
		timer.getDay() +
		" Days " +
		timer.getHours() +
		" Hours " +
		timer.getMinutes() +
		" Minutes " +
		timer.getSeconds() +
		" Seconds";

	if (--timer < 0) {
		display.textContent = "LIVE";
	}

	setInterval(function () {
		timer = new Date(timer - 1000);

		display.textContent =
			timer.getDay() +
			" Days " +
			timer.getHours() +
			" Hours " +
			timer.getMinutes() +
			" Minutes " +
			timer.getSeconds() +
			" Seconds";

		if (--timer < 0) {
			display.textContent = "LIVE";
		}
	}, 1000);
}

var animateHTML = function () {
	var elems;
	var windowHeight;

	function init() {
		elems = document.querySelectorAll(".pre-slide-in");
		windowHeight = window.innerHeight;
		addEventHandlers();
		checkPosition();
	}

	function addEventHandlers() {
		window.addEventListener("scroll", checkPosition);
		window.addEventListener("resize", init);
	}

	function checkPosition() {
		for (var i = 0; i < elems.length; i++) {
			var positionFromTop = elems[i].getBoundingClientRect().top;
			if (positionFromTop - windowHeight <= 0) {
				if (elems[i].className.find("pre-animate")) {
				}
				elems[i].className = elems[i].className.replace(
					"pre-animate__flipInY",
					"animate__flipInY"
				);
			}

			if (positionFromTop - windowHeight > 1 || positionFromTop < 0) {
				elems[i].className = elems[i].className.replace(
					"animate__flipInY",
					"pre-animate__flipInY"
				);
			}
		}
	}

	return {
		init: init,
	};
};
=======
// DEFINITIONS AND ELEMENTS
var header = document.getElementsByTagName("header")[0];
var slides = document.getElementsByClassName("slide");
var slideCards = document.getElementsByClassName("slide-card-inner");

var slideIndex = 1;
var slideInterval = setInterval(nextSlide, 1000);
showSlides(slideIndex);

window.addEventListener("resize", placeNav);
document.body.onload = function () {
	for (var i = 0; i < slideCards.length; i++) {
		startTimer(slideCards[i].getElementsByClassName("slide-time")[0]);
	}
	setTimeout(placeNav, 300);
};

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
	if (slideCards.length) {
		if (n > slideCards.length) {
			slideIndex = 1;
		}
		if (n < 1) {
			slideIndex = slideCards.length;
		}
		for (var i = 0; i < slideCards.length; i++) {
			slides[i].style.display = "none";
			slideCards[i].style.display = "none";
		}
		slides[slideIndex - 1].style.display = "block";
		slideCards[slideIndex - 1].style.display = "block";

		clearInterval(slideInterval);
		slideInterval = setInterval(nextSlide, 5000);
	}
}

// COUNTDOWN TIMER
function startTimer(display) {
	var timer =
		new Date(display.innerHTML.replace("UPCOMMING - ", "")) - new Date();

	timer = new Date(timer - 1000);

	display.textContent =
		timer.getDay() +
		" Days " +
		timer.getHours() +
		" Hours " +
		timer.getMinutes() +
		" Minutes " +
		timer.getSeconds() +
		" Seconds";

	if (--timer < 0) {
		display.textContent = "LIVE";
	}

	setInterval(function () {
		timer = new Date(timer - 1000);

		display.textContent =
			timer.getDay() +
			" Days " +
			timer.getHours() +
			" Hours " +
			timer.getMinutes() +
			" Minutes " +
			timer.getSeconds() +
			" Seconds";

		if (--timer < 0) {
			display.textContent = "LIVE";
		}
	}, 1000);
}

const observer = new IntersectionObserver(entries => {

	entries.forEach(entry => {

		if (entry.isIntersecting) {
			console.log(entry.target.className);

			entry.target.className.replace("pre-animate__", "animate__");

			return; // if we added the class, exit the function
		}

		// We're not intersecting, so remove the class!
		entry.target.className.replace("animate__", "pre-animate__");
		console.log(3);
	});
});

observer.observe(document.querySelector('.animate__animated'));
>>>>>>> bcc21a1a0f95ad0d6bc859db173bb26bc0ed8b23

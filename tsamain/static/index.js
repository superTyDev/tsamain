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

const observer = new IntersectionObserver((entries) => {
	entries.forEach((entry) => {
		if (entry.isIntersecting) {
			entry.target.className.replace("pre-animate__", "animate__");

			return; // if we added the class, exit the function
		}

		// We're not intersecting, so remove the class!
		entry.target.className.replace("animate__", "pre-animate__");
	});
});

observer.observe(document.querySelector(".animate__animated"));

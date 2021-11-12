// Write scroll position to <html> for shadow on scroll
// Gets original position and triggers on page scroll
document.documentElement.dataset.scroll = window.scrollY;
document.addEventListener("scroll", () => {
	document.documentElement.dataset.scroll = window.scrollY;
});

// Coverts the nav bar to responsive
function responsiveNavbar() {
	[...document.getElementsByTagName("nav")].forEach((x) => {
		if (x.className === "nav") {
			x.className += " responsive";
		} else {
			x.className = "nav";
		}
	});
}

var slideIndex = 1;
var slideInterval = setInterval(function () {
	plusSlides(1);
}, 10000);
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
	showSlides((slideIndex += n));
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
	slideInterval = setInterval(function () {
		plusSlides(1);
	}, 10000);
}

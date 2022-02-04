var expandLastHeight = 0;
function expandUpcoming(elem) {
	var upcoming = document.getElementById("upcoming-expand");

	if (parseInt(expandLastHeight) - parseInt(upcoming.offsetHeight) < 800) {
		upcoming.style.maxHeight = expandLastHeight =
			(parseInt(upcoming.offsetHeight) + 800).toString() + "px";
	} else {
		elem.style.display = "none";
	}
}

var coll = document.getElementsByClassName("collapsible");

for (var i = 0; i < coll.length; i++) {
	coll[i].dataset.index = i;
	coll[i].addEventListener("click", function () {
		this.classList.toggle("active");
		var content = document.getElementsByClassName("collapsible-content")[
			this.dataset.index
		];
		if (content.style.display === "block") {
			content.style.display = "none";
		} else {
			content.style.display = "block";
		}
	});
}
var expandLastHeight = 0;
function expandUpcoming(elem) {
	var upcoming = document.getElementById("upcoming-expand");

	if (parseInt(expandLastHeight) - parseInt(upcoming.offsetHeight) < 800) {
		upcoming.style.maxHeight = expandLastHeight =
			(parseInt(upcoming.offsetHeight) + 800).toString() + "px";
	} else {
		elem.style.display = "none";
	}
}

var coll = document.getElementsByClassName("collapsible");

for (var i = 0; i < coll.length; i++) {
	coll[i].dataset.index = i;
	coll[i].addEventListener("click", function () {
		this.classList.toggle("active");
		var content = document.getElementsByClassName("collapsible-content")[
			this.dataset.index
		];
		if (content.style.display === "block") {
			content.style.display = "none";
		} else {
			content.style.display = "block";
		}
	});
}

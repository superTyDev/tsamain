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

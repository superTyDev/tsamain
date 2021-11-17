function expandUpcoming(elem) {
	var upcoming = document.getElementById('upcoming-expand');
	console.log(upcoming.childNodes.length);
	if (upcoming.offsetHeight < 4800) {
		upcoming.style.height = (parseInt(upcoming.offsetHeight) + 800).toString() + 'px';
	} else {
		elem.style.display = "none";
	}
}

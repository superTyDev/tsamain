function expandUpcoming(elem) {
    var upcoming = document.getElementById("upcoming-expand");
    if (upcoming.offsetHeight < 4800) {
        upcoming.style.maxHeight =
            (parseInt(upcoming.offsetHeight) + 800).toString() + "px";
    } else {
        elem.style.display = "none";
    }
}

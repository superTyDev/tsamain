function expandUpcoming(elem) {
        var upcoming = document.getElementById('upcoming-expand');

        document.body.innerHTML += `-${upcoming.offsetHeight}of-${upcoming.style.maxHeight}mh-${(parseInt(upcoming.offsetHeight) + 800).toString() + 'px'}-`;

        if (!upcoming.style.maxHeight t) {
           upcoming.style.maxHeight = (parseInt(upcoming.offsetHeight) + 800).toString() + 'px';     
        } else {
            elem.style.display = "none";    
        }
}
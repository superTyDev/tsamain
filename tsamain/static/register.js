openPay(document.getElementsByClassName("tablinks")[0]);
function openPay(elem) {
	var i, tabcontent, tablinks;
	var buttonIndex = Array.from(elem.parentElement.getElementsByTagName("button")).indexOf(elem)

	tabcontent = document.getElementsByClassName("tabcontent");
	for (i = 0; i < tabcontent.length; i++) {
		tabcontent[i].style.display = "none";
	}
	tablinks = document.getElementsByClassName("tablinks");
	for (i = 0; i < tablinks.length; i++) {
		tablinks[i].classList.remove("active");
	}

	document.getElementsByClassName("tabcontent")[buttonIndex].style.display = "block";
	elem.classList.add("active");
}
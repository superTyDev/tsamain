Date.prototype.toDateInputValue = (function () {
	var local = new Date(this);
	local.setMinutes(this.getMinutes() - this.getTimezoneOffset());
	return local.toJSON().slice(0, 10);
});
document.getElementById('datePicker').value = new Date().toDateInputValue();

var formatter = new Intl.NumberFormat('en-US', {
	style: 'currency',
	currency: 'USD',
});

var es = document.querySelectorAll('.input-categories');
for (var i = 0; i < es.length; i++) {
	es[i]._list = es[i].querySelector('ul');
	es[i]._input = es[i].querySelector('input');
	es[i]._input._icategories = es[i];
	es[i].onkeydown = function (e) {
		var e = event || e;
		if (e.keyCode == 13) {
			var c = e.target._icategories;
			var li = document.createElement('li');
			li.innerHTML = c._input.value;
			c._list.appendChild(li);
			c._input.value = '';
			e.preventDefault();
		}
	}
}
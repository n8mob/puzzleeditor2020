(() => {
	let lineLength = 0;

	document.addEventListener('DOMContentLoaded', () => {
		lineLength = getLineLengthInput().value;

		const inputs = document.querySelectorAll('.char-counter-text-input')

		inputs.forEach((input) => {
			input.addEventListener('input', e => updateCharCountLabel(e.target));
		});

		getLineLengthInput().addEventListener('change', e => onLineLengthChange(e.target, inputs));
	});

	function getLineLengthInput() {
		return document.querySelector('#id_line_length');
	}

	function updateCharCountLabel(input) {
		const label = findLabel(input);
		const valueLength = input.value.length;

		if (valueLength > lineLength) {
			addClass(label, 'long');
		} else {
			removeClass(label, 'long');
		}

		label.textContent = `${valueLength} chars`;
	}

	function onLineLengthChange(target, inputs) {
		lineLength = target.value;

		inputs.forEach(input => {
			updateCharCountLabel(input);
		});
	}

	function findLabel(eventTarget) {
		return eventTarget.parentNode.querySelector('.char-counter-text-input + .counter');
	}

	function addClass(el, className) {
		if (!el.classList.contains(className)) {
			el.classList.add(className);
		}
	}

	function removeClass(el, className) {
		if (el.classList.contains(className)) {
			el.classList.remove(className);
		}
	}

})();


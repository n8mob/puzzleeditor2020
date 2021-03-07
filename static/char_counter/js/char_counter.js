let LineLengthSettingSingleton = 0;

document.addEventListener('DOMContentLoaded', () => {
	LineLengthSettingSingleton = getLineLength();

	const inputs = document.querySelectorAll('.char-counter-text-input')

	inputs.forEach((input) => {
		input.addEventListener('input', e => updateCharCountLabel(e.target));
	});

	document.querySelector('#id_line_length').addEventListener('change', (e) => {
		LineLengthSettingSingleton = e.target.value;

		inputs.forEach(input => {
			updateCharCountLabel(input)
		})
	});
})

function updateCharCountLabel(input) {
	const label = findLabel(input);
	const valueLength = input.value.length;

	if (valueLength > LineLengthSettingSingleton) {
		addClass(label, 'long');
	} else {
		removeClass(label, 'long');
	}

	label.textContent = `${valueLength} chars`;
}

function findLabel(eventTarget) {
	return eventTarget.parentNode.querySelector('.char-counter-text-input + .counter');
}

function getLineLength() {
	return document.querySelector('#id_line_length').value;
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

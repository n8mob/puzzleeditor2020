class CharCounter {
	constructor({inputSelector, lineLengthSelector}) {
		this.inputSelector = inputSelector;
		this.lineLengthSelector = lineLengthSelector;
		this.lineLength = 0;
	}

	onDomLoaded() {
		this.selectLineInputs();
		this.selectLineLengthInput();

		this.listenForLineChanges();
		this.listenForLineLengthChanges();

		this.lineLength = this.lineLengthInput.value;
		this.updateLineLabels();
	}

	selectLineInputs() {
		this.lineInputs = document.querySelectorAll(this.inputSelector);
	}

	selectLineLengthInput() {
		this.lineLengthInput = document.querySelector(this.lineLengthSelector);
	}

	listenForLineChanges() {
		this.lineInputs.forEach(input => {
			input.addEventListener('input', e => this.updateCharCountLabel(e.target));
		})
	}

	listenForLineLengthChanges() {
		this.lineLengthInput.addEventListener('change', e => this.onLineLengthChange(e.target));
	}

	updateCharCountLabel(input) {
		const label = this.findLabel(input);
		const valueLength = input.value.length;

		if (valueLength > this.lineLength) {
			this.addClass(label, 'long');
		} else {
			this.removeClass(label, 'long');
		}

		label.textContent = `${valueLength} chars`;
	}

	onLineLengthChange(target) {
		this.lineLength = target.value;

		this.updateLineLabels()
	}

	updateLineLabels() {
		this.lineInputs.forEach(input => {
			this.updateCharCountLabel(input);
		});
	}

	findLabel(eventTarget) {
		return eventTarget.parentNode.querySelector('.char-counter-text-input + .counter');
	}

	addClass(el, className) {
		if (!el.classList.contains(className)) {
			el.classList.add(className);
		}
	}

	removeClass(el, className) {
		if (el.classList.contains(className)) {
			el.classList.remove(className);
		}
	}
}

(() => {
	let charCounter = new CharCounter({
		inputSelector: '.char-counter-text-input',
		lineLengthSelector: '#id_line_length',
	});

	document.addEventListener('DOMContentLoaded', () => {
		charCounter.onDomLoaded();
	});
})();

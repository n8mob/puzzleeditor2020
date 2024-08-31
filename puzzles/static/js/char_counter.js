class CharCounter {
	constructor({inputSelector, lineLengthSelector, charCountLabelSelector}) {
		this.inputSelector = inputSelector;
		this.lineLengthSelector = lineLengthSelector;
		this.charCountLabelSelector = charCountLabelSelector;
		this.lineLength = 20;
	}

	onDomLoaded() {
		this.lineInputs = this.selectLineInputs();
		this.lineLengthInput = this.selectLineLengthInput();

		this.listenForLineChanges();
		this.listenForLineLengthChanges();

		this.lineLength = this.lineLengthInput.value;
		this.updateLineLabels();
	}

	selectLineInputs() {
		return document.querySelectorAll(this.inputSelector);
	}

	selectLineLengthInput() {
		return document.querySelector(this.lineLengthSelector);
	}

	selectLabel(eventTarget) {
		return eventTarget.parentNode.querySelector(this.charCountLabelSelector);
	}

	listenForLineChanges() {
		this.lineInputs.forEach(input => {
			input.addEventListener('input', this.onLineChange.bind(this));
		})
	}

	listenForLineLengthChanges() {
		this.lineLengthInput.addEventListener('change', this.onLineLengthChange.bind(this));
	}

	onLineChange(e) {
		this.updateCharCountLabel(e.target);
	}

	onLineLengthChange(e) {
		this.lineLength = e.target.value;

		this.updateLineLabels()
	}

	updateLineLabels() {
		this.lineInputs.forEach(input => {
			this.updateCharCountLabel(input);
		});
	}

	updateCharCountLabel(input) {
		const label = this.selectLabel(input);
		const valueLength = input.value.length;

		if (valueLength > this.lineLength) {
			this.addClass(label, 'long');
		} else {
			this.removeClass(label, 'long');
		}

		label.textContent = `${valueLength} chars`;
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

/**
 * Listen for line changes & mark once it becomes too long
 * Listen for line changes & remove mark when no longer too long
 * Listen for line length setting change, update labels with new value
 * Mark any too-long inputs once dom is ready
 */
(() => {
	let charCounter = new CharCounter({
		inputSelector: '.char-counter-text-input',
		lineLengthSelector: '#id_line_length',
		charCountLabelSelector: '.char-counter-text-input + .counter',
	});

	document.addEventListener('DOMContentLoaded', () => {
		charCounter.onDomLoaded();
	});
})();

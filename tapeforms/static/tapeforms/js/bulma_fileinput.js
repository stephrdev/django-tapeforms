window.addEventListener('DOMContentLoaded', function() {
	// Iterate over file inputs which don't have yet a placeholder for the
	// selected file name. It will be created and updated when the value changes.
	document.querySelectorAll('.control > .file:not(.has-name)')
		.forEach(function(control) {
			const label = control.querySelector('label.file-label');
			const input = control.querySelector('input.file-input');

			const filename = document.createElement('span');
			filename.className = 'file-name is-hidden';
			label.appendChild(filename);

			input.onchange = function() {
				if (!input.files.length) {
					filename.classList.add('is-hidden');
					control.classList.remove('has-name');
				} else {
					filename.textContent = input.files[0].name;

					filename.classList.remove('is-hidden');
					control.classList.add('has-name');
				}
			}
		});
});

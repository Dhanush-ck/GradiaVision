const fileInput = document.getElementById('file');
const label = document.querySelector('.file-upload');
const nameEl = document.getElementById('filename');

// Show filename on selection
fileInput.addEventListener('change', function () {
  if (this.files.length) {
    nameEl.textContent = '📄 ' + this.files[0].name;
    nameEl.classList.add('visible');
    label.classList.add('has-file');
  }
});

// Drag over — highlight the zone
label.addEventListener('dragover', function (e) {
  e.preventDefault();
  e.stopPropagation();
  label.classList.add('has-file');
});

// Drag leave — remove highlight
label.addEventListener('dragleave', function (e) {
  e.preventDefault();
  e.stopPropagation();
  label.classList.remove('has-file');
});

// Drop — assign file to the input
label.addEventListener('drop', function (e) {
  e.preventDefault();
  e.stopPropagation();

  const files = e.dataTransfer.files;
  if (!files.length) return;

  const file = files[0];

  // Validate PDF
  if (file.type !== 'application/pdf') {
    alert('Only PDF files are allowed.');
    label.classList.remove('has-file');
    return;
  }

  // Assign to the real input so the form submits it
  const dataTransfer = new DataTransfer();
  dataTransfer.items.add(file);
  fileInput.files = dataTransfer.files;

  nameEl.textContent = '📄 ' + file.name;
  nameEl.classList.add('visible');
  label.classList.add('has-file');
});
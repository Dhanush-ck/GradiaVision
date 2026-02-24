const fileInput = document.getElementById('file');
const label = document.querySelector('.file-upload');
const nameEl = document.getElementById('filename');

function setFile(file) {
  if (!file) return;

  // Validate PDF
  if (file.type !== 'application/pdf') {
    alert('Only PDF files are allowed.');
    clearFile();
    return;
  }

  // Assign to the hidden input so the form submits it
  const dataTransfer = new DataTransfer();
  dataTransfer.items.add(file);
  fileInput.files = dataTransfer.files;

  // Update UI
  nameEl.textContent = '📄 ' + file.name;
  nameEl.classList.add('visible');
  label.classList.add('has-file');
}

function clearFile() {
  fileInput.value = '';
  nameEl.textContent = '';
  nameEl.classList.remove('visible');
  label.classList.remove('has-file');
}

// ── Click to browse (native, handled by <label for="file">) ──

fileInput.addEventListener('change', function () {
  if (this.files.length) {
    setFile(this.files[0]);
  }
});

// ── Drag over: highlight drop zone ──

label.addEventListener('dragenter', function (e) {
  e.preventDefault();
  e.stopPropagation();
  label.classList.add('has-file');
});

label.addEventListener('dragover', function (e) {
  e.preventDefault();
  e.stopPropagation();
  e.dataTransfer.dropEffect = 'copy';
  label.classList.add('has-file');
});

// ── Drag leave: remove highlight ──

label.addEventListener('dragleave', function (e) {
  e.preventDefault();
  e.stopPropagation();
  // Only remove if actually leaving the label (not a child element)
  if (!label.contains(e.relatedTarget)) {
    if (!fileInput.files.length) {
      label.classList.remove('has-file');
    }
  }
});

// ── Drop: assign file ──

label.addEventListener('drop', function (e) {
  e.preventDefault();
  e.stopPropagation();

  const files = e.dataTransfer.files;
  if (!files.length) {
    label.classList.remove('has-file');
    return;
  }

  setFile(files[0]);
});
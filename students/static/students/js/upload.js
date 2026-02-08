const file = document.getElementById('file');
const filename = document.getElementById('filename');

file.addEventListener("change", () => {
  filename.textContent = file.files[0]?.name || "";
});
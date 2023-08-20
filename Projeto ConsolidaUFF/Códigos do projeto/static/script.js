const uploadForm = document.getElementById('upload-form');

uploadForm.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadForm.classList.add('highlight');
});

uploadForm.addEventListener('dragleave', () => {
    uploadForm.classList.remove('highlight');
});

uploadForm.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadForm.classList.remove('highlight');

    const files = e.dataTransfer.files;
    handleFiles(files);
});

uploadForm.addEventListener('change', (e) => {
    const files = e.target.files;
    handleFiles(files);
});

function handleFiles(files) {
    for (const file of files) {
        // You can handle each file here
        console.log('File:', file.name);
    }
}


uploadForm.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadForm.classList.remove('highlight');

    const files = e.dataTransfer.files;
    handleFiles(files);

    // Adicione os arquivos ao input de arquivo
    const fileInput = document.getElementById('pdf_file');
    fileInput.files = files;
});


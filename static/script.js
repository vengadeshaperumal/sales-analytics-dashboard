document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const csvFile = document.getElementById('csvFile');
    const fileInfo = document.getElementById('fileInfo');
    const uploadStatus = document.getElementById('uploadStatus');
    const fileLabel = document.querySelector('.file-upload-label');
    const fileNameEl = document.getElementById('fileName');
    const fileSizeEl = document.getElementById('fileSize');
    const uploadBtn = document.getElementById('uploadBtn');

    const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB

    // File selection handling with enhanced feedback
    csvFile.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            const file = this.files[0];
            
            // Validate file
            if (!validateFile(file)) {
                csvFile.value = '';
                fileInfo.classList.remove('show');
                return;
            }
            
            updateFileDisplay(file);
        }
    });

    function validateFile(file) {
        // Check file extension
        if (!file.name.toLowerCase().endsWith('.csv')) {
            showStatus('Please select a valid CSV file (.csv extension required)', 'error');
            return false;
        }

        // Check file size
        if (file.size > MAX_FILE_SIZE) {
            showStatus(`File size exceeds 10MB limit. Selected file is ${(file.size / (1024 * 1024)).toFixed(2)}MB`, 'error');
            return false;
        }

        return true;
    }

    function updateFileDisplay(file) {
        const fileSizeMB = (file.size / (1024 * 1024)).toFixed(2);
        fileNameEl.textContent = file.name;
        fileSizeEl.textContent = `${fileSizeMB} MB`;
        fileInfo.classList.add('show');
    }

    // Drag and drop handling with CSS classes
    fileLabel.addEventListener('dragover', function(e) {
        e.preventDefault();
        e.stopPropagation();
        fileLabel.classList.add('dragover');
    });

    fileLabel.addEventListener('dragleave', function(e) {
        e.preventDefault();
        e.stopPropagation();
        fileLabel.classList.remove('dragover');
    });

    fileLabel.addEventListener('drop', function(e) {
        e.preventDefault();
        e.stopPropagation();
        fileLabel.classList.remove('dragover');

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            csvFile.files = e.dataTransfer.files;
            const event = new Event('change', { bubbles: true });
            csvFile.dispatchEvent(event);
        }
    });

    // Form submission with comprehensive validation
    uploadForm.addEventListener('submit', function(e) {
        e.preventDefault();

        // Validate file selection
        if (!csvFile.files || csvFile.files.length === 0) {
            showStatus('Please select a CSV file before uploading', 'error');
            return;
        }

        const file = csvFile.files[0];

        // Re-validate file
        if (!validateFile(file)) {
            return;
        }

        // Prepare and upload
        const formData = new FormData();
        formData.append('file', file);

        // Disable button during upload
        uploadBtn.disabled = true;
        uploadBtn.innerHTML = '<span class="btn-icon">⏳</span> <span>Processing...</span>';

        showStatus('⏳ Uploading and processing your file...', 'loading');

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showStatus('✓ File processed successfully! Redirecting to dashboard...', 'success');
                setTimeout(() => {
                    window.location.href = '/dashboard';
                }, 1500);
            } else {
                showStatus(`✗ Error: ${data.message || 'Unknown error occurred'}`, 'error');
                resetUploadBtn();
            }
        })
        .catch(error => {
            console.error('Upload error:', error);
            showStatus(`✗ Error: ${error.message || 'Network error, please try again'}`, 'error');
            resetUploadBtn();
        });
    });

    function resetUploadBtn() {
        uploadBtn.disabled = false;
        uploadBtn.innerHTML = '<span class="btn-icon">⚡</span> <span>Upload & Analyze</span>';
    }

    function showStatus(message, type) {
        uploadStatus.innerHTML = message;
        uploadStatus.className = `status-message show ${type}`;
    }
});


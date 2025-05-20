// Initialize Chart.js radar chart
document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('radarChart')?.getContext('2d');
    if(ctx) {
        // Chart initialization code from previous answer
    }
});
document.querySelectorAll('input[type="file"]').forEach(input => {
    input.addEventListener('change', function(e) {
        const fileName = this.files[0] ? this.files[0].name : 'No file selected';
        const displayElement = this.parentElement.querySelector('.file-name');
        
        displayElement.textContent = fileName;
        displayElement.classList.add('file-selected');
        
        // Add visual feedback to upload box
        const uploadBox = this.parentElement.querySelector('.upload-box');
        uploadBox.classList.add('has-file');
    });
});
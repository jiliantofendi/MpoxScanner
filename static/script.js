// Toggle class active
const navbarNav = document.querySelector('.navbar-nav');

// Ketika menu diklik
document.querySelector('#menu').onclick = () => {
    navbarNav.classList.toggle('active');
};

// Klik di luar sidebar untuk menghilangkan menu
const menu = document.querySelector('#menu');

document.addEventListener('click', function(e) {
    if (!menu.contains(e.target) && !navbarNav.contains(e.target)){
        navbarNav.classList.remove('active');
    }
});

// Klik upload gambar
document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.getElementById('fileInput');
    const selectedImage = document.getElementById('selectedImage');
    const uploadButton = document.querySelector('.upload-button');
    const uploadText = document.querySelector('.upload-text');
    const imagePreview = document.getElementById('imagePreview');
    const uploadBox = document.querySelector('.upload-box');
    // Ketika tombol upload diklik, buka file input
    uploadButton.addEventListener('click', function () {
        fileInput.click();
    });

    // Saat gambar dipilih
    fileInput.addEventListener('change', function () {
        const file = fileInput.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                selectedImage.src = e.target.result;
                selectedImage.style.display = 'block';
                uploadButton.style.display = 'none';
                uploadText.style.display = 'none';
                uploadBox.style.cursor = 'pointer';
            };
            reader.readAsDataURL(file);
        }
    });

    // Klik pada gambar akan membuka file input untuk memilih ulang
    selectedImage.addEventListener('click', function () {
        fileInput.click();
    });
});

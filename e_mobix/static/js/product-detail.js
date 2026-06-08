const variants = JSON.parse(document.getElementById('variants-data').textContent);
const colorSelect = document.getElementById('color-select');
const storageSelect = document.getElementById('storage-select');
const variantInput = document.getElementById('variant-id-input');
const productImage = document.getElementById('product-image');

// Get unique colors
const colors = [...new Set(variants.map(v => v.color))];
colors.forEach(color => {
    const opt = document.createElement('option');
    opt.value = color;
    opt.textContent = color;
    colorSelect.appendChild(opt);
});

function updateStorage() {
    const selectedColor = colorSelect.value;
    const filtered = variants.filter(v => v.color === selectedColor);

    storageSelect.innerHTML = '';
    filtered.forEach(v => {
        const opt = document.createElement('option');
        opt.value = v.storage;
        opt.textContent = v.storage;
        storageSelect.appendChild(opt);
    });

    updateVariant();
}

function updateVariant() {
    const selectedColor = colorSelect.value;
    const selectedStorage = storageSelect.value;
    const match = variants.find(v => v.color === selectedColor && v.storage === selectedStorage);

    if (match) {
        variantInput.value = match.id;

        // Update image with fade effect
        if (match.image && productImage) {
            productImage.style.opacity = '0';
            setTimeout(() => {
                productImage.src = match.image;
                productImage.style.opacity = '1';
            }, 300);
        }
    }
}

colorSelect.addEventListener('change', updateStorage);
storageSelect.addEventListener('change', updateVariant);

updateStorage();
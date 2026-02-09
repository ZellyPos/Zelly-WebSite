// Confirm delete actions
function confirmDelete(message) {
    return confirm(message || 'Rostdan ham o\'chirmoqchimisiz?');
}

// Auto-hide messages after 5 seconds
document.addEventListener('DOMContentLoaded', function () {
    const messages = document.querySelectorAll('.alert');
    messages.forEach(function (message) {
        setTimeout(function () {
            message.style.opacity = '0';
            message.style.transform = 'translateY(-20px)';
            setTimeout(function () {
                message.remove();
            }, 300);
        }, 5000);
    });
});

// Dynamic feature fields for pricing form
function addFeatureField() {
    const container = document.getElementById('features-container');
    if (!container) return;

    const fieldGroup = document.createElement('div');
    fieldGroup.className = 'feature-field-group';
    fieldGroup.innerHTML = `
        <input type="text" name="features[]" class="form-control" placeholder="Xususiyat matni">
        <button type="button" class="btn-remove-feature" onclick="removeFeatureField(this)">×</button>
    `;
    container.appendChild(fieldGroup);
}

function removeFeatureField(button) {
    button.parentElement.remove();
}

// Image preview
function previewImage(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function (e) {
            const preview = document.getElementById('image-preview');
            if (preview) {
                preview.src = e.target.result;
                preview.style.display = 'block';
            }
        };
        reader.readAsDataURL(input.files[0]);
    }
}

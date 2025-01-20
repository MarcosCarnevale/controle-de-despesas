document.getElementById('selectAll').addEventListener('click', function(event) {
    const checkboxes = document.querySelectorAll('.select-item');
    checkboxes.forEach(checkbox => {
        checkbox.checked = event.target.checked;
    });
});
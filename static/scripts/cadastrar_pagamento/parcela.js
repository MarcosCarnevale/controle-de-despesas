function toggleParcelaFields(show) {
    const parcelaFields = document.getElementById('parcelaFields');
    if (show) {
        parcelaFields.style.display = 'block';
    } else {
        parcelaFields.style.display = 'none';
    }
}
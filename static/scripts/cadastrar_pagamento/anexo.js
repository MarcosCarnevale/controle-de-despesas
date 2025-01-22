function openAnexoModal(pagamentoId) {
    document.getElementById('pagamentoId').value = pagamentoId;
    $('#anexoModal').modal('show');
}

document.getElementById('formSalvarAnexo').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    fetch('/salvar_anexo', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Anexo salvo com sucesso!');
            location.reload();
        } else {
            alert('Erro ao salvar anexo: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao salvar anexo: ' + error.message);
    });
});
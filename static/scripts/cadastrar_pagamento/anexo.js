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

function excluirAnexo(pagamentoId) {
    if (confirm('Tem certeza que deseja excluir este anexo?')) {
        fetch('/apagar_anexo/' + pagamentoId, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Anexo excluído com sucesso!');
                location.reload();
            } else {
                alert('Erro ao excluir anexo: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao excluir anexo: ' + error.message);
        });
    }
}

function downloadAnexo(pagamentoId) {
    fetch(`/download_anexo/${pagamentoId}`)
        .then(response => {
            if (response.ok) {
                alert('Download iniciado.');
            }
            else {
                alert('Erro ao iniciar download: ' + response.statusText);
            }
        })
}
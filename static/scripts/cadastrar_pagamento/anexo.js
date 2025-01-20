function salvarAnexo(event, pagamentoId) {
    const arquivoInput = event.target;
    const arquivo = arquivoInput.files[0];
    if (!arquivo) {
        return;
    }

    const formData = new FormData();
    formData.append('pagamento_id', pagamentoId);
    formData.append('arquivo', arquivo);

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
            alert('Erro ao salvar anexo');
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao salvar anexo');
    });
}
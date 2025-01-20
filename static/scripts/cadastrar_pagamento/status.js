function atualizarStatus(id, status) {
    const banco = document.querySelector(`tr[data-id="${id}"] .banco`).textContent.trim();
    if (status === 'Pago' && !banco) {
        alert('Para pagar a conta, é necessário preencher o campo Banco.');
        return;
    }

    fetch(`/atualizar_status/${id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ status: status })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            alert('Erro ao atualizar status');
        }
    });
}
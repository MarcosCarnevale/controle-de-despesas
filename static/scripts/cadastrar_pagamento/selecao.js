function apagarSelecao() {
    const selectedIds = Array.from(document.querySelectorAll('.select-item:checked')).map(checkbox => checkbox.value);
    if (selectedIds.length === 0) {
        alert('Nenhum pagamento selecionado');
        return;
    }

    fetch('/apagar_selecao', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ ids: selectedIds })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            alert(data.message || 'Erro ao apagar seleção');
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao apagar seleção');
    });
}

function pagarSelecao() {
    const selectedIds = Array.from(document.querySelectorAll('.select-item:checked')).map(checkbox => checkbox.value);
    if (selectedIds.length === 0) {
        alert('Nenhum pagamento selecionado');
        return;
    }

    fetch('/pagar_selecao', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ ids: selectedIds })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            alert(data.message || 'Erro ao pagar seleção');
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao pagar seleção');
    });
}

function abrirSelecao() {
    const selectedIds = Array.from(document.querySelectorAll('.select-item:checked')).map(checkbox => checkbox.value);
    if (selectedIds.length === 0) {
        alert('Nenhum pagamento selecionado');
        return;
    }

    fetch('/abrir_selecao', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ ids: selectedIds })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            alert(data.message || 'Erro ao abrir seleção');
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao abrir seleção');
    });
}

function apagarSelecaoAnexo() {
    const selectedIds = Array.from(document.querySelectorAll('.select-item:checked')).map(checkbox => checkbox.value);
    if (selectedIds.length === 0) {
        alert('Nenhum pagamento selecionado');
        return;
    }

    fetch('/apagar_selecao_anexo', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ ids: selectedIds })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload();
        } else {
            alert(data.message || 'Erro ao apagar seleção de anexos');
        }
    })
    .catch(error => {
        console.error('Erro:', error);
        alert('Erro ao apagar seleção de anexos');
    });
}
function getSelectedItems() {
    let selectedItems = [];
    let checkboxes = document.querySelectorAll('.selectItem:checked');
    checkboxes.forEach((checkbox) => {
        selectedItems.push(checkbox.value);
    });
    return selectedItems;
}

function pagarSelecao() {
    let selectedIds = getSelectedItems();
    if (selectedIds.length > 0) {
        if (confirm('Tem certeza que deseja marcar os pagamentos selecionados como pagos?')) {
            fetch('/pagar_pagamentos', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ ids: selectedIds })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Pagamentos marcados como pagos com sucesso.');
                    location.reload();
                } else {
                    alert(
                        'Erro ao marcar como pagos:\n' 
                        + data.message
                        + '\n\nIDs dos pagamentos que não possuem banco associado:\n'
                        + data.invalid_ids.join(', '))

                }
            })
            .catch(error => {
                console.error('Erro:', error);
                alert('Erro ao marcar pagamentos como pagos: ' + error.message);
            });
        }
    } else {
        alert('Nenhum pagamento selecionado.');
    }
}

function apagarSelecao() {
    let selectedItems = getSelectedItems();
    if (selectedItems.length > 0) {
        if (confirm('Tem certeza que deseja excluir os pagamentos selecionados?')) {
            fetch('/excluir_pagamentos', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ ids: selectedItems })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Pagamentos excluídos com sucesso.');
                    location.reload();
                } else {
                    alert('Erro ao excluir pagamentos: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Erro:', error);
                alert('Erro ao excluir pagamentos: ' + JSON.stringify(error));
            });
        }
    } else {
        alert('Nenhum pagamento selecionado.');
    }
}

function abrirSelecao() {
    let selectedItems = getSelectedItems();
    if (selectedItems.length > 0) {
        // Implementar a lógica para abrir os itens selecionados
        console.log('Abrir:', selectedItems);
        // Aqui você pode fazer uma chamada AJAX para abrir os itens selecionados
    } else {
        alert('Nenhum pagamento selecionado.');
    }
}

function apagarSelecaoAnexo() {
    let selectedItems = getSelectedItems();
    if (selectedItems.length > 0) {
        if (confirm('Tem certeza que deseja excluir os anexos dos pagamentos selecionados?')) {
            fetch('/excluir_anexos', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ ids: selectedItems })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Anexos excluídos com sucesso.');
                    location.reload();
                } else {
                    alert('Erro ao excluir anexos: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Erro:', error);
                alert('Erro ao excluir anexos: ' + JSON.stringify(error));
            });
        }
    } else {
        alert('Nenhum pagamento selecionado.');
    }
}
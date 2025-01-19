document.getElementById('selectAll').addEventListener('click', function(event) {
    const checkboxes = document.querySelectorAll('.select-item');
    checkboxes.forEach(checkbox => {
        checkbox.checked = event.target.checked;
    });
});

function openModal() {
    $('#modal').modal('show');
}

function closeModal() {
    $('#modal').modal('hide');
}

function toggleParcelaFields(show) {
    const parcelaFields = document.getElementById('parcelaFields');
    if (show) {
        parcelaFields.style.display = 'block';
    } else {
        parcelaFields.style.display = 'none';
    }
}

function updateSubcategorias() {
    const categoria = document.getElementById('categoria').value;
    fetch(`/subcategorias/${categoria}`)
        .then(response => response.json())
        .then(data => {
            const subcategoriaSelect = document.getElementById('subcategoria');
            subcategoriaSelect.innerHTML = '<option value="">Selecione uma subcategoria</option>';
            data.subcategorias.forEach(subcategoria => {
                const option = document.createElement('option');
                option.value = subcategoria;
                option.textContent = subcategoria;
                subcategoriaSelect.appendChild(option);
            });
        });
}

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

function sortTable(n) {
    const table = document.querySelector('.table');
    let rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    switching = true;
    dir = "asc";
    while (switching) {
        switching = false;
        rows = table.rows;
        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;
            x = rows[i].getElementsByTagName("TD")[n];
            y = rows[i + 1].getElementsByTagName("TD")[n];
            if (dir == "asc") {
                if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                    shouldSwitch = true;
                    break;
                }
            } else if (dir == "desc") {
                if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                    shouldSwitch = true;
                    break;
                }
            }
        }
        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            switchcount++;
        } else {
            if (switchcount == 0 && dir == "asc") {
                dir = "desc";
                switching = true;
            }
        }
    }
    updateSortIcons(table, n, dir);
}

function updateSortIcons(table, columnIndex, direction) {
    const headers = table.querySelectorAll('th');
    headers.forEach((header, index) => {
        const icon = header.querySelector('i');
        if (icon) {
            if (index === columnIndex) {
                icon.className = direction === 'asc' ? 'fas fa-sort-up' : 'fas fa-sort-down';
            } else {
                icon.className = 'fas fa-sort';
            }
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const hoje = new Date().toISOString().split('T')[0]; // Data de hoje no formato 'YYYY-MM-DD'

    document.querySelectorAll('tr[data-id]').forEach(row => {
        const status = row.querySelector('td:nth-child(12)').textContent.trim();
        const dataPagamento = row.querySelector('td:nth-child(5)').textContent.trim();

        if (status === 'Em Aberto') {
            const dataPagamentoDate = new Date(dataPagamento);
            const hojeDate = new Date(hoje);

            if (dataPagamentoDate.toISOString().split('T')[0] === hoje) {
                row.querySelector('td:nth-child(12)').innerHTML += ' <i class="fas fa-exclamation-triangle text-warning" title="Pagamento vence hoje"></i>';
            } else if (dataPagamentoDate < hojeDate) {
                row.querySelector('td:nth-child(12)').innerHTML += ' <i class="fas fa-exclamation-triangle text-danger" title="Pagamento atrasado"></i>';
            }
        }
    });
});
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
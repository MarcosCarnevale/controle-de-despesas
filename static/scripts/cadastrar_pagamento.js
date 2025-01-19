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

function downloadAnexo(pagamentoId) {
    fetch(`/download_anexo/${pagamentoId}`)
        .then(response => {
            if (response.ok) {
                return response.blob();
            } else {
                throw new Error('Erro ao baixar anexo');
            }
        })
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = `anexo_${pagamentoId}.pdf`; // Ajuste o nome do arquivo conforme necessário
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Erro ao baixar anexo');
        });
}
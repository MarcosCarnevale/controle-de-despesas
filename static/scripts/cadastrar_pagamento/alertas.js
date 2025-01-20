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
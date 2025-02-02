document.addEventListener('DOMContentLoaded', function () {
    var editarCartaoModal = document.getElementById('editarCartaoModal');
    editarCartaoModal.addEventListener('show.bs.modal', function (event) {
        var button = event.relatedTarget;
        var id = button.getAttribute('data-id');
        var nome = button.getAttribute('data-nome');
        var numero = button.getAttribute('data-numero');
        var dataFechamento = button.getAttribute('data-data_fechamento');
        var dataVencimento = button.getAttribute('data-data_vencimento');

        var modal = this;
        modal.querySelector('#edit_nome').value = nome;
        modal.querySelector('#edit_numero').value = numero;
        modal.querySelector('#edit_data_fechamento').value = dataFechamento;
        modal.querySelector('#edit_data_vencimento').value = dataVencimento;
        modal.querySelector('#editarCartaoForm').setAttribute('action', '/editar_cartao/' + id);
    });
});
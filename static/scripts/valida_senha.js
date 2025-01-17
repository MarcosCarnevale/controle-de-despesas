// Seleciona o formulário e os campos de senha
const form = document.getElementById('cadastroForm');
const senha = document.getElementById('senha');
const confirmarSenha = document.getElementById('confirmar-senha');
const errorMessage = document.getElementById('error-message');

// Adiciona o evento de validação no envio do formulário
form.addEventListener('submit', function (e) {
    // Verifica se a senha tem no mínimo 6 caracteres
    if (senha.value.length < 6) {
        e.preventDefault(); // Impede o envio do formulário
        errorMessage.textContent = 'A senha deve ter no mínimo 6 caracteres.'; // Define a mensagem de erro
        errorMessage.style.display = 'block'; // Exibe a mensagem de erro
    // Verifica se as senhas são iguais
    } else if (senha.value !== confirmarSenha.value) {
        e.preventDefault(); // Impede o envio do formulário
        errorMessage.textContent = 'As senhas não coincidem.'; // Define a mensagem de erro
        errorMessage.style.display = 'block'; // Exibe a mensagem de erro
    } else {
        errorMessage.style.display = 'none'; // Oculta a mensagem de erro
    }
});
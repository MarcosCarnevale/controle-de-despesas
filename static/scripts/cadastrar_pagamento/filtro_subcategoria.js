function updateFiltroSubcategorias() {
    const categoria = document.getElementById('filtro_categoria').value;
    fetch(`/subcategorias/${categoria}`)
        .then(response => response.json())
        .then(data => {
            const subcategoriaSelect = document.getElementById('filtro_subcategoria');
            subcategoriaSelect.innerHTML = '<option value="">Selecione uma subcategoria</option>';
            data.subcategorias.forEach(subcategoria => {
                const option = document.createElement('option');
                option.value = subcategoria;
                option.textContent = subcategoria;
                subcategoriaSelect.appendChild(option);
            });
        });
}
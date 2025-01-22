function toggleSelectAll(source) {
    let checkboxes = document.getElementsByClassName('selectItem');
    for (let i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = source.checked;
    }
}

function getSelectedItems() {
    let selectedItems = [];
    let checkboxes = document.getElementsByClassName('selectItem');
    for (let i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            selectedItems.push(checkboxes[i].value);
        }
    }
    return selectedItems;
}

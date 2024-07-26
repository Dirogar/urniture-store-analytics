function makeEditable(td) {
    if (td.getElementsByTagName('input').length === 0) {
        let currentValue = td.innerText;
        td.innerHTML = `<input type="text" value="${currentValue}" onblur="updateData(this)" />`;
        td.getElementsByTagName('input')[0].focus();
    }
}

function updateData(input) {
    let td = input.parentElement;
    let newValue = input.value;
    let product = td.getAttribute('data-product');
    let store = td.getAttribute('data-store');
    let field = td.getAttribute('data-field');

    // Отправка данных на сервер через AJAX
    fetch(updateStoreProductUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            product: product,
            store: store,
            field: field,
            value: newValue
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            td.innerText = newValue;
        } else {
            alert('Ошибка обновления данных');
            td.innerText = currentValue;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Ошибка обновления данных');
        td.innerText = currentValue;
    });
}
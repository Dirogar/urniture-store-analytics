function makeEditable(td) {
    if (td.getElementsByTagName('input').length === 0) {
        let currentValue = td.innerText;
        td.innerHTML = `<input type="text" value="${currentValue}" onblur="updateData(this)" />`;
        td.getElementsByTagName('input')[0].focus();
    }
}

function updateData(input) {
    let td = input.parentElement;
    let originalValue = td.innerText;
    let newValue = input.value;
    let product = td.getAttribute('data-product');
    let store = td.getAttribute('data-store');
    let field = td.getAttribute('data-field');

    let utl, body;

    if (field == 'room_class') {
        method = 'PATCH'
        url = "/api/product/" + product + "/";
        body = JSON.stringify({
            [field]: newValue,
            product_article: product
        })
    } else {
        method = 'POST';
        url = "/api/storeproduct/";
        body = JSON.stringify({
            [field]: newValue,
            store: store,
            product_article: product
        })
    }
    fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: body
    })
    .then(response => {
        if (response.ok) {
            td.innerHTML = newValue;
        } else {
            throw new Error('Ошибка при обновлении данных');
        }
    })
    .then(data => {
        td.innerHTML = newValue;
    })
    .catch(error => {
        console.error('Ошибка', error);
        td.innerHTML = originalValue;
        alert('Не удалось сохранить изменения');
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

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

    fetch("/api/products/" + product + "/", {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            [field]: newValue
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.id) {
            td.innerText = newValue;
        } else {
            alert('Ошибка обновления данных');
            td.innerText = currentValue;
        }
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

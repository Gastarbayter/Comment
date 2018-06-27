const fillSelect = (selectRef, data) => {
    const options = selectRef.querySelectorAll('options:not(:disabled)');
    options.forEach((el) => {
        el.parentNode.removeChild(el);
    });

    Object.keys(data).forEach((key) => {
        const option = document.createElement('option');
        option.innerHTML = data[key];
        option.value = key;

        selectRef.append(option)
    })
};

const fillFrom = (url, selectRef) => {
    selectRef.disabled = true;
    return fetch(url)
        .then((response) => response.json())
        .then((data) => {
            fillSelect(selectRef, data);
            selectRef.disabled = false;
        });
};

const addComment = (form) => {
    const obj = {};
    const elements = form.querySelectorAll("input, select, textarea");
    elements.forEach((element) => {
        obj[element.name] = element.value;
    });
    return fetch('/comment', {
        method: 'POST',
        body: JSON.stringify(obj)
    }).then((response) => {
        if (response.status === 201) {

            alert('Ваш коментарий добавлен');
        }
        else {
            throw new Error(`Ошибка. Статус код: ${response.status}`)
        }
    }).catch((err) => {
        alert(err.message);
    });
};


document.addEventListener('DOMContentLoaded', () => {
    const regionsSelect = document.querySelector('#regionsSelect');
    const citySelect = document.querySelector('#citySelect');


    regionsSelect.addEventListener('change', () => {
        const value = regionsSelect.value;
        fillFrom(`/get_all_regions/${value}`, citySelect)
    });

    fillFrom('/get_all_regions', regionsSelect);

    const commentForm = document.querySelector('#commentForm');
    commentForm.addEventListener("submit", function (e) {
        e.preventDefault();
        addComment(this);
    }, false);
});



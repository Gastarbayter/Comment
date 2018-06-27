function delRow() {
    deleteComment(this.getAttribute('data-id'));
    const row = this.parentElement.parentElement;
    const table = row.parentElement;
    table.removeChild(row);
}


const fillTable = ((tableRef, data) => {
    data.forEach((rowData, index) => {

        const newRow = tableRef.insertRow(index + 1);

        rowData.forEach((cellData, cellIndex) => {
            const cell = newRow.insertCell(cellIndex);
            cell.innerText = cellData;

        });
        const controlCell = newRow.insertCell(rowData.length);

        const control = document.createElement('input');
        control.type = "button";
        control.setAttribute('data-id', rowData[0]);
        control.value = "Удалить";
        control.onclick = delRow;
        controlCell.appendChild(control);

    })
});

const deleteComment = (index) => {
    return fetch(`/comments/${index}`, {
        method: 'delete'
    }).then((response) => {
        if (response.status !== 201) {
            throw new Error(`Ошибка. Статус код: ${response.status}`)
        }
        else {
            alert('Коментарий удален');
        }
    }).catch((err) => {
        alert(err.message);
    });
};

const fetchTable = (url, tableRef) => {
    return fetch(url)
        .then((response) => response.json())
        .then((data) => {
            fillTable(tableRef, data);
        });
};



document.addEventListener('DOMContentLoaded', () => {
    const commentsTable = document.querySelector('#commentsTable');

    fetchTable('/get_all_comments', commentsTable);
});




function hidenClick() {
    const infoDiv = document.querySelector('#infoDiv');
    infoDiv.style.display = 'none';
}


function info() {

    const row = this.parentElement.parentElement;
    const region = row.childNodes[1].innerHTML;
    getInfo(this.getAttribute('data-id'), region);
}

const getInfo = (index, region) => {
    return fetch(`/get_city_statistic/${index}`)
        .then((response) => {
            if (response.status !== 200) {
                throw new Error(`Ошибка. Статус код: ${response.status}`)
            }
            else {
                return response.json();
            }
        })
        .then((data) => {

            const infoDiv = document.querySelector('#infoDiv');

            infoDiv.style.display = 'table';

            const statisticCityTable = document.querySelector('#statisticCityTable');

            for (let i = statisticCityTable.rows.length - 1; i > 0; i--) {
                statisticCityTable.deleteRow(i);
            }

            const caption = statisticCityTable.createCaption();
            caption.innerHTML = `Дополнительная информация по региону: ${region}`
            fillTableInfo(statisticCityTable, data);
        })
        .catch((err) => {
            alert(err.message);
        });
};


const fillTableInfo = ((tableRef, data) => {

    Object.keys(data).forEach((key, index) => {
        const newRow = tableRef.insertRow(index + 1);


        const cellCity = newRow.insertCell(0);
        cellCity.innerText = key;
        const cellCount = newRow.insertCell(1);
        cellCount.innerText = data[key];

    });
});

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
        control.value = "Подробнее";
        control.setAttribute('data-id', rowData[0]);
        control.onclick = info;
        controlCell.appendChild(control);
    })
});

const fetchTable = (url, tableRef) => {
    return fetch(url)
        .then((response) => response.json())
        .then((data) => {
            fillTable(tableRef, data);
        });
};


document.addEventListener('DOMContentLoaded', () => {
    const statisticTable = document.querySelector('#statisticTable');


    fetchTable('/get_statistics', statisticTable);
});




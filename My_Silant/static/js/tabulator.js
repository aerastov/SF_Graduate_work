function loadJson(selector) {
  return document.querySelector(selector).getAttribute('data-json');
}


$(document).ready(function() {
    var data = loadJson('#jsonData').replaceAll("'", '"');
    console.log('data = ', data)

    var table = new Tabulator('#car_table', {
        data:JSON.parse(data),
        layout: 'fitColumns',
        columns: [
            { title: 'Машина', field: 'factory_number', width: 80 },
            { title: 'Модель техники', field: 'technique_model', align: 'left', formatter: 'progress' },
            { title: 'Модель двигателя', field: 'engine_model' }
        ]
    });
});




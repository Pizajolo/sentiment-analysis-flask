// Table where to put the tweets
const table = document.getElementById('tweet-table');

// Select Dropdown
const sel = document.getElementById('dropdown');
// Chart to show the result
let ctx = document.getElementById('doughnutChart').getContext('2d');
ctx.height = 200;
let chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'doughnut',

    // The data for our dataset
    data: {
        labels: ['Positive', 'Negative', 'Neutral'],
        datasets: [{
            backgroundColor: ["#0b851f", "#a6141d", "#676a6a"],
            borderColor: 'rgb(200,201,210)',
            data: [0, 0, 0]
        }]
    },

    // Configuration options go here
    options: {
        legend: {
            display: true,
            position: 'bottom',
            labels: {
                fontColor: 'rgb(200,201,210)'
            }
        },
        maintainAspectRatio: false,
        responsive: true,
    }
});
// functions to add cells and rows to table
function addCell(tr, val) {
    var td = document.createElement('td');
    td.innerHTML = val;
    tr.appendChild(td)
}

function addRow(tbl, val_1, val_2, val_3, val_4) {
    var tr = document.createElement('tr');

    addCell(tr, val_1);
    addCell(tr, val_2);
    addCell(tr, val_3);
    addCell(tr, val_4);

    tbl.appendChild(tr)
}


async function app() {
    console.log('Hello Welcome to the Pizajolo Sentiment Website');
    document.querySelector('#form').onsubmit = () => {

        // Initialize new request
        const request = new XMLHttpRequest();
        const search_query = document.querySelector('#form-input').value;
        console.log(search_query);
        request.open('POST', '/search');

        // Callback function for when request completes
        request.onload = () => {

            // Extract JSON data from request
            const data = JSON.parse(request.responseText);

            for (var i = table.rows.length; i > 1; i--) {
                table.deleteRow(i - 1);
            }
            if (data.success) {
                // setting the numbers to display in DoughnutChart
                let neg = 0;
                let posi = 0;
                let neu = 0;
                for (let i = 0; i < data.tweets.length; i++) {
                    addRow(table, data.tweets[i][0], data.tweets[i][1], data.tweets[i][2], data.tweets[i][3]);
                    if (data.tweets[i][4] === -1) {
                        neg = neg + 1;
                    }
                    if (data.tweets[i][4] === 1) {
                        posi = posi + 1;
                    }
                    if (data.tweets[i][4] === 0) {
                        neu = neu + 1;
                    }
                }
                // Display Chart
                let data_chart = [posi, neg, neu];
                chart.canvas.parentNode.style.height = '200px';
                ctx.height = 200;
                chart.data.datasets[0].data = data_chart;
                chart.update();


            } else {
                // document.querySelector('#result').innerHTML = 'There was an error.';
            }
        };

        // Add data to send with request
        const data = new FormData();
        data.append('search_query', search_query);

        data.append('type', sel.value);
        // Send request
        request.send(data);
        return false;

    };

}

app();
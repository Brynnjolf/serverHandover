
$(document).ready(function() {
    let ticker = window.location.href.slice(-4).slice(0,3);
    $.get( "http://localhost:8000/api/getPriceData/"+ticker+"/", function( data ) {
        console.log(data);
        data = data.filter(valueNotZero)
        console.log(data);
        buildGraph(data);
    });
});

function buildGraph(priceSet) {
    const priceList = priceSet.map(el => el["fields"]['price']).reverse();
    const dateList = priceSet.map(el => el['pk'].slice(3)).reverse();
    
    console.log((priceList));
    console.log(dateList);
    var x = 6;
    var ctx = document.getElementById('priceChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dateList,
            datasets: [{
                label: 'Market Price',
                data: priceList,
                backgroundColor: [
                    'rgba(255,255,255,0)'
                ],
                borderColor: ['rgb(31, 69, 183)'],
                borderWidth: 2,
                pointBackgroundColor: 'rgba(255,255,255,0)',
                pointBorderColor: 'rgba(255,0,255,0)'
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        // beginAtZero: true
                        // max:Math.max(...priceList) + 0.5,
                        // min:Math.min(...priceList) - 0.5,
                    }
                }]
            },
            elements: {
                backgroundColor: 'rgba(0,0,0,0)'
            }
        }
    });
}

function valueNotZero(value) {
    return (value['fields']['price'] != 0);
}


function tearSheet() {
    downloadFile('tearsheet');
}
function annualreport() {
    downloadFile('annualReport');
}

function downloadFile(type) {
    alert('Coming Soon!');
}

// def tearSheet():
//     downloadfile("tearsheet")

// def downloadfile(type):
//     if type == 'tearsheet'

//     if type
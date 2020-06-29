"use strict";
let stuff = ['weckdengeparden', 'mega', 'Hogarama'];
function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color + '55';
}
$(document).ready(() => {
    let promises = stuff.map(singleStuff => Handler.get(singleStuff));
    Promise.all(promises).then((value) => {
        let chartDatas = value.map(item => ChartHelper.transformData(item, new Date(2020, 5, 1), new Date()));
        // const chartData:IChartData[] = ChartHelper.transformData(value, new Date(2019,11,1), new Date())
        const labels = chartDatas[0].map((data) => {
            return `${data.date.toDateString()}`;
        });
        let datasets = chartDatas.map((data, i) => {
            let color = getRandomColor();
            let singleDataSetData = data.map((item) => {
                return item.count;
            });
            return {
                label: value[i].name,
                data: singleDataSetData,
                backgroundColor: color,
                borderColor: color
            };
        });
        console.log(chartDatas);
        var ctx = document.getElementById('myChart').getContext('2d');
        var chart = new Chart(ctx == null ? "" : ctx, {
            // The type of chart we want to create
            type: 'line',
            // The data for our dataset
            data: {
                labels,
                datasets
            },
            // Configuration options go here
            options: {
                elements: { point: { radius: 0, hitRadius: 10, hoverRadius: 10 } },
                maintainAspectRatio: false,
                responsive: true,
                spanGaps: true,
                scales: {
                    yAxes: [{
                            display: true,
                            ticks: {
                                suggestedMin: 0,
                                // OR //
                                beginAtZero: true // minimum value will be 0.
                            }
                        }]
                }
            }
        });
    }, (value) => {
        console.error(value);
    });
});

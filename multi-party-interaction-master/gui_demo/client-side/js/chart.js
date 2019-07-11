backgroundColorList = [
    'rgba(255, 99, 132, 0.2)',
    'rgba(54, 162, 235, 0.2)',
    'rgba(75, 192, 80, 0.2)',
    'rgba(153, 102, 255, 0.2)',
    'rgba(255, 159, 64, 0.2)',
    'rgba(255, 206, 86, 0.2)'
];

borderColorList = [
    'rgba(255, 99, 132, 1)',
    'rgba(54, 162, 235, 1)',
    'rgba(75, 192, 80, 1)',
    'rgba(153, 102, 255, 1)',
    'rgba(255, 159, 64, 1)',
    'rgba(255, 206, 86, 1)'
];


function createChart(ctx, label, chartIdx = 0, type = 'bar', chartDataLabel = "Level of Trust") {
    let data = {
        labels: [label],
        datasets: [{
            label: chartDataLabel,
            data: [0],
            backgroundColor: [
                backgroundColorList[chartIdx]
            ],
            borderColor: [
                borderColorList[chartIdx]
            ],
            borderWidth: 1
        }]
    };

    let options = {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true,
                    stepSize: 1.0,
                    precision: 1.0,
                    maxTicksLimit: 4,
                    suggestedMax: 10,
                    suggestedMin: -10,
                }
            }]
        },
        // events: ['click'],
        maintainAspectRatio: false,
    };

    return new Chart(ctx, {
        type: type,
        data: data,
        options: options,
    });
}

function chartButtonOnClick(chartObj, videoObj, chartKey, action = "add") {
    if (action === 'add') {
        return () => {
            const keyPressTime = videoObj.currentTime;

            chartObj.config.data.datasets[0].data[0] += 1;
            chartObj.update();

            console.log(`${chartObj.chart.canvas.id}: +1 at ${keyPressTime}`);
            annotationHistoryMap[chartKey].push({
                time: keyPressTime,
                points: 1
            });
        }
    }

    return () => {
        const keyPressTime = videoObj.currentTime;
        chartObj.config.data.datasets[0].data[0] -= 1;
        chartObj.update();

        console.log(`${chartObj.chart.canvas.id}: -1 at ${keyPressTime}`);
        annotationHistoryMap[chartKey].push({
                time: keyPressTime,
                points: -1
            });
    }
}
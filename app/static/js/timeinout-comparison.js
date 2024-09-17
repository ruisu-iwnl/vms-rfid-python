document.addEventListener('DOMContentLoaded', function () {
    var chartDataElement = document.getElementById('timeInOutData');
    var chartLabels = chartDataElement.getAttribute('data-labels');
    var timeInData = chartDataElement.getAttribute('data-timein');
    var timeOutData = chartDataElement.getAttribute('data-timeout');

    console.log('Time-In/Time-Out Labels:', chartLabels);
    console.log('Time-In Data:', timeInData);
    console.log('Time-Out Data:', timeOutData);

    // Parse labels and data from data attributes
    var labels = chartLabels ? chartLabels.split(',').map(label => label.trim()) : [];
    var timeInCounts = timeInData ? timeInData.split(',').map(Number) : [];
    var timeOutCounts = timeOutData ? timeOutData.split(',').map(Number) : [];

    console.log('Parsed Labels:', labels);
    console.log('Parsed Time-In Data:', timeInCounts);
    console.log('Parsed Time-Out Data:', timeOutCounts);

    // Default to sample data if no data is provided
    if (labels.length === 0) {
        labels = Array.from({ length: 7 }, (_, i) => `Day ${i + 1}`); // Default daily labels
        timeInCounts = Array.from({ length: 7 }, () => Math.floor(Math.random() * 20) + 1); // Random time-ins
        timeOutCounts = Array.from({ length: 7 }, () => Math.floor(Math.random() * 20) + 1); // Random time-outs
    }

    var ctx = document.getElementById('timeInOutChart').getContext('2d');
    var timeInOutChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Time-Ins',
                data: timeInCounts,
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }, {
                label: 'Time-Outs',
                data: timeOutCounts,
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ': ' + context.raw;
                        }
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        maxRotation: 45,
                        minRotation: 30,
                        autoSkip: true,
                        maxTicksLimit: 7 // Limit number of labels shown
                    }
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});

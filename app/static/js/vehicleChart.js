document.addEventListener('DOMContentLoaded', function () {
    var chartDataElement = document.getElementById('chartData');
    var labelsString = chartDataElement.getAttribute('data-labels');
    var dataString = chartDataElement.getAttribute('data-data');

    // Parse labels and data from data attributes
    var dailyLabels = labelsString ? labelsString.split(',').map(label => label.trim()) : [];
    var dailyData = dataString ? dataString.split(',').map(Number) : [];

    // Default to daily data if no data is provided
    if (dailyLabels.length === 0) {
        dailyLabels = Array.from({ length: 7 }, (_, i) => `Day ${i + 1}`); // Default daily labels
        dailyData = Array.from({ length: 7 }, () => Math.floor(Math.random() * 20) + 1); // Random vehicle counts
    }

    // Check the parsed data
    console.log('Labels:', dailyLabels);
    console.log('Data:', dailyData);

    var ctx = document.getElementById('vehicleChart').getContext('2d');
    var vehicleChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: dailyLabels,
            datasets: [{
                label: 'Number of Vehicles',
                data: dailyData,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
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
                            return context.label + ': ' + context.raw + ' vehicles';
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

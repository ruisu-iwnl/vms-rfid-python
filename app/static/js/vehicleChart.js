document.addEventListener('DOMContentLoaded', function () {
    var ctx = document.getElementById('vehicleChart').getContext('2d');
    var vehicleChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Array.from({length: 7}, (_, i) => `Day ${i + 1}`), // Daily data for 7 days
            datasets: [{
                label: 'Number of Vehicles',
                data: Array.from({length: 7}, () => Math.floor(Math.random() * 20) + 1), // Random vehicle counts between 1 and 20
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
                        maxTicksLimit: 7, // Limit number of labels shown
                    }
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});

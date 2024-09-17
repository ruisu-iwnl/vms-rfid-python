document.addEventListener('DOMContentLoaded', function () {
    var chartDataElement = document.getElementById('mostActiveDaysData');
    var labelsString = chartDataElement.getAttribute('data-labels');
    var dataString = chartDataElement.getAttribute('data-data');

    console.log('Most Active Days Labels:', labelsString);
    console.log('Most Active Days Data:', dataString);

    // Parse labels and data from data attributes
    var activeDaysLabels = labelsString ? labelsString.split(',').map(label => label.trim()) : [];
    var activeDaysData = dataString ? dataString.split(',').map(Number) : [];

    console.log('Parsed Labels:', activeDaysLabels);
    console.log('Parsed Data:', activeDaysData);

    // Default to sample data if no data is provided
    if (activeDaysLabels.length === 0) {
        const daysOfWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
        activeDaysLabels = daysOfWeek;
        activeDaysData = Array.from({ length: 7 }, () => Math.floor(Math.random() * 20) + 1); // Random vehicle counts
    }

    var ctx = document.getElementById('mostActiveDaysChart').getContext('2d');
    var mostActiveDaysChart = new Chart(ctx, {
        type: 'line', // Change to 'line'
        data: {
            labels: activeDaysLabels,
            datasets: [{
                label: 'Number of Vehicle Entries',
                data: activeDaysData,
                backgroundColor: 'rgba(75, 192, 192, 0.2)', // Fill color
                borderColor: 'rgba(75, 192, 192, 1)', // Line color
                borderWidth: 2,
                fill: true // Fill the area under the line
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
                        maxTicksLimit: 7 // Show one label per day of the week
                    }
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});

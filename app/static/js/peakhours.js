document.addEventListener('DOMContentLoaded', function () {
    var chartDataElement = document.getElementById('peakHoursData');
    var labelsString = chartDataElement.getAttribute('data-labels');
    var dataString = chartDataElement.getAttribute('data-data');

    console.log('Peak Hours Labels:', labelsString);
    console.log('Peak Hours Data:', dataString);

    var peakHoursLabels = labelsString ? labelsString.split(',').map(label => label.trim()) : [];
    var peakHoursData = dataString ? dataString.split(',').map(Number) : [];

    var ctx = document.getElementById('peakHoursChart').getContext('2d');
    var peakHoursChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: peakHoursLabels,
            datasets: [{
                label: 'Number of Vehicle Entries',
                data: peakHoursData,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 2,
                fill: true 
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
                        callback: function(value, index, values) {
                            let label = value.toString();
                            let hour = parseInt(label.split(":")[0]);

                            return hour === 0 ? '12 AM' :
                                   hour < 12 ? hour + ' AM' :
                                   hour === 12 ? '12 PM' : (hour - 12) + ' PM';
                        },
                        maxRotation: 0,  
                        autoSkip: true,   
                        maxTicksLimit: 12 
                    }
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});

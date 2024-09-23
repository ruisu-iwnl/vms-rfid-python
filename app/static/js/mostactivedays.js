document.addEventListener('DOMContentLoaded', function () {
    var chartDataElement = document.getElementById('mostActiveDaysData');
    var labelsString = chartDataElement.getAttribute('data-labels');
    var timeInString = chartDataElement.getAttribute('data-time-in');
    var timeOutString = chartDataElement.getAttribute('data-time-out');

    console.log('Most Active Days Labels:', labelsString);
    console.log('Time In Data:', timeInString);
    console.log('Time Out Data:', timeOutString);

    // Parse labels and data from data attributes
    var activeDaysLabels = labelsString ? labelsString.split(',').map(label => label.trim()) : [];
    var timeInData = timeInString ? timeInString.split(',').map(Number) : [];
    var timeOutData = timeOutString ? timeOutString.split(',').map(Number) : [];

    // Initialize default data arrays
    var defaultDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
    var defaultTimeInData = new Array(defaultDays.length).fill(0);
    var defaultTimeOutData = new Array(defaultDays.length).fill(0);

    // Update default data with actual data from backend
    defaultDays.forEach((day, index) => {
        const dataIndex = activeDaysLabels.indexOf(day);
        if (dataIndex > -1) {
            defaultTimeInData[index] = timeInData[dataIndex] || 0;
            defaultTimeOutData[index] = timeOutData[dataIndex] || 0;
        }
    });

    var ctx = document.getElementById('mostActiveDaysChart').getContext('2d');
    var mostActiveDaysChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: defaultDays,
            datasets: [
                {
                    label: 'Time In',
                    data: defaultTimeInData,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 2,
                    fill: true
                },
                {
                    label: 'Time Out',
                    data: defaultTimeOutData,
                    backgroundColor: 'rgba(192, 75, 192, 0.2)',
                    borderColor: 'rgba(192, 75, 192, 1)',
                    borderWidth: 2,
                    fill: true
                }
            ]
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
                            return context.dataset.label + ': ' + context.raw + ' vehicles';
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
                        maxTicksLimit: 7
                    }
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});

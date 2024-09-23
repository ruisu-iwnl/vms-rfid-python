document.addEventListener('DOMContentLoaded', function () {
    var stayDurationElement = document.getElementById('stayDurationData');
    var labelsString = stayDurationElement.getAttribute('data-labels');
    var durationString = stayDurationElement.getAttribute('data-duration');

    console.log('Stay Duration Labels:', labelsString);
    console.log('Duration Data:', durationString);

    // Parse labels and data from data attributes
    var durationLabels = labelsString ? labelsString.split(',').map(label => label.trim()) : [];
    var durationData = durationString ? durationString.split(',').map(Number) : [];

    console.log('Parsed Labels:', durationLabels);
    console.log('Parsed Duration Data:', durationData);

    // Default to specific dates if none is provided
    if (durationLabels.length === 0) {
        const today = new Date();
        durationLabels = Array.from({ length: 7 }, (_, i) => {
            const date = new Date(today);
            date.setDate(today.getDate() - i);
            return date.toDateString(); // e.g., "Mon Sep 16 2024"
        }).reverse(); // Reverse to show the latest date first
        durationData = Array.from({ length: 7 }, () => Math.floor(Math.random() * 100) + 1); // Random durations
    }

    var ctx = document.getElementById('durationHistogram').getContext('2d');
    var durationChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: durationLabels,
            datasets: [{
                label: 'Average Duration of Stay (in hours)',
                data: durationData,
                backgroundColor: 'rgba(153, 102, 255, 0.2)',
                borderColor: 'rgba(153, 102, 255, 1)',
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
                            return context.label + ': ' + context.raw.toFixed(2) + ' hours'; // Show two decimal points
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
                        maxTicksLimit: 24 // Adjust for hourly labels
                    }
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});

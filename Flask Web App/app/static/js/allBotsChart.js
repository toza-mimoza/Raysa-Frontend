var chartContainer = document.getElementById("chartContainer");
var idCounter = 0;


function initChart(data, labels, title){
  var divBootstrapColumn = document.createElement("div");
  var canvas = document.createElement("canvas");
  var titleElement = document.createElement("h3");

  // set h3 title text and class
  titleElement.innerHTML = title;
  titleElement.className = "text-center";

  // append title as h3 elements to charts
  divBootstrapColumn.appendChild(titleElement);

  // set id for canvas
  canvas.id = idCounter++;
  divBootstrapColumn.className = "col-lg-4 col-md-6 col-sm-12";

  // append canvas to column
  divBootstrapColumn.appendChild(canvas);

  // finally append the column-title-canvas construct to the parent chart container
  chartContainer.appendChild(divBootstrapColumn);
  setTimeout(() => {
    var ctx = document.getElementById(canvas.id).getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: '# of user messages',
                data: data,
                backgroundColor: [
                    'rgba(75, 0, 130, 0.2)',
                ],
                borderColor: [
                    'rgba(75, 0, 130, 1)',
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
  }, 100)
}

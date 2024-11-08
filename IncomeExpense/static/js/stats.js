const renderChart = (data, labels) => {
  var ctx = document.getElementById("myChart").getContext("2d");
  new Chart(ctx, {
    type: "pie",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Last 6 months expenses",
          data: data,
          borderWidth: 1.4,
        },
      ],
    },
    options: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: "Expenses per category"
          }
        }
    }
      
  });
};

const getChartData = () => {
  fetch("/expense_category_summary")
    .then((res) => res.json())
    .then((results) => {

      const category_data = results.expense_category_data;
      const [labels, data] = [
        Object.keys(category_data),
        Object.values(category_data),
      ];

      renderChart(data, labels);
    });
};

document.onload = getChartData();
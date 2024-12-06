async function fetchData(endpoint) {
  // Fetch data from the repository
  const uri = `/api/chart-data/${endpoint}/github-168152007`;
  const data = await fetch(uri);

  if (data.ok) {
    return JSON.parse(await data.text());
  } else {
    // TODO: error
  }
}

async function drawChart(element, endpoint, chartType) {
  const data = await fetchData(endpoint);

  let plotlyData, layout;
  switch (chartType) {
    case 'pie-chart-commits-by-author':
      plotlyData = [
        {
          values: data.map(({author}) => commits),
          labels: data.map(({commit_count}) => commit_count),
          type: 'pie',
          //maybe for loop for the firs 3??
          textinfo: "none",
          showlegend: false,
          hoverinfo: 'percent+label',
          domain: {'x': [0, 1], 'y': [0, 1]},
        }
        ];

        layout = {
          height: 300,
          width: 600,
          margin: {
            l: 50,
            r: 50,
            t: 25,
            b: 25,
            pad: 2
          }
      }


break;
    case 'bar-chart-code-lines-per-file':
      plotlyData = [
        {
          y: data.map(({_, line_count}) => lineCount),
          x: data.map(({path}) => file),
          type: 'bar',
          marker: {color: 'rgba(5,112,1,0.65)'},

        }
      ];
      layout = {
        xaxis: {title: {text: 'Files'}},
        yaxis: {title: {text: 'Lines of code'}},
        barcornerradius: 7,

      };
  break;
    case 'bar-chart-commits-over-time':
      plotlyData = [
        {
          y: Array.from(commitCountsMap.values()),
          x: Array.from(commitCountsMap.keys()),
          type: 'histogram',
          marker: {color: 'rgba(5,112,1,0.65)'},

        }
      ];
      layout = {
        xaxis: {title: {text: 'Files'}},
        yaxis: {title: {text: 'Lines of code'}},


      };
  }

  Plotly.newPlot(element.querySelector('.plotly-graph'), plotlyData,layout);

  const mostCommitsTable = element.querySelector('.most-table');
  const leastCommitsTable = element.querySelector('.least-table');

  const highestCommitters = data.slice(0, 3);
  const lowestCommitters = data.slice(Math.max(data.length - 3, 0)).reverse();

  var i = 0;

  // for (const [author, commitCount] of highestCommitters) {
  //   const row = document.createElement('tr');
  //   mostCommitsTable.appendChild(row);
  //   const rankCell = document.createElement('td');
  //   rankCell.class = 'td';
  //   rankCell.textContent = `${i + 1}`;
  //   row.appendChild(rankCell);
  //   const authorCell = document.createElement('td');
  //   authorCell.class = 'td';
  //   authorCell.textContent = `${author} (${commitCount} commits)`
  //   row.appendChild(authorCell);

  //   i++;
  // }

  // i = data.length;

  // for (const [author, commitCount] of lowestCommitters) {
  //   const row = document.createElement('tr');
  //   leastCommitsTable.appendChild(row);
  //   const rankCell = document.createElement('td');
  //   rankCell.class = 'td';
  //   rankCell.textContent = `${i}`;
  //   row.appendChild(rankCell);
  //   const authorCell = document.createElement('td');
  //   authorCell.class = 'td';
  //   authorCell.textContent = `${author} (${commitCount} commits)`
  //   row.appendChild(authorCell);

  //   i--;
  // }
}

drawChart(document.querySelector('.commits-per-author-container'), 'commits-per-author', 'pie-chart-commits-by-author');
drawChart(document.querySelector('.code-lines-in-files-per-project-container'), 'line-counts-per-file', 'bar-chart-code-lines-per-file');
drawChart(document.querySelector('.commits-over-time-container'), 'commit-dates', 'bar-chart-commits-over-time');

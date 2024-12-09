async function fetchData(endpoint) {
  // Fetch data from the repository
  const uri = `/api/chart-data/${endpoint}/github-4710920`;
  const data = await fetch(uri);

  if (data.ok) {
    return JSON.parse(await data.text());
  } else {
    // TODO: error
  }
}

function drawTables(element, data) {
  const mostCommitsTable = element.querySelector('.most-table');
  const leastCommitsTable = element.querySelector('.least-table');

  const highestCommitters = data.slice(0, 3);
  const lowestCommitters = data.slice(Math.max(data.length - 3, 0)).reverse();

  var i = 0;

  for (const [author, commitCount] of highestCommitters) {
    const row = document.createElement('tr');
    mostCommitsTable.appendChild(row);
    const rankCell = document.createElement('td');
    rankCell.class = 'td';
    rankCell.textContent = `${i + 1}`;
    row.appendChild(rankCell);
    const authorCell = document.createElement('td');
    authorCell.class = 'td';
    authorCell.textContent = `${author} (${commitCount} commits)`
    row.appendChild(authorCell);

    i++;
  }

  i = data.length;

  for (const [author, commitCount] of lowestCommitters) {
    const row = document.createElement('tr');
    leastCommitsTable.appendChild(row);
    const rankCell = document.createElement('td');
    rankCell.class = 'td';
    rankCell.textContent = `${i}`;
    row.appendChild(rankCell);
    const authorCell = document.createElement('td');
    authorCell.class = 'td';
    authorCell.textContent = `${author} (${commitCount} commits)`
    row.appendChild(authorCell);

    i--;
  }
}

async function drawHistogram(domElement,{xLabel, yLabel, endpoint, getX}) {
  const data = await fetchData(endpoint);

  // Set the plotly settings, data, and other things, based on the chart type
  //
  let plotlyData, layout;

  plotlyData = [
    {
      x: data.map(getX),
      type: 'histogram',
      marker: {color: 'rgba(5,112,1,0.65)'},
      }];

  layout = {
    xaxis: {title: {text: xLabel}},
    yaxis: {title: {text: yLabel}},
    };

  Plotly.newPlot(domElement.querySelector('.plotly-graph'), plotlyData,layout);

  
}

async function drawPieChart(domElement, {endpoint, getLabel, getValue}) {
  const data = await fetchData(endpoint);

  const plotlyData = [
  {
    labels: data.map(getLabel),
    values: data.map(getValue),
    type: 'pie',
    //maybe for loop for the firs 3??
    textinfo: "none",
    showlegend: false,
    hoverinfo: 'percent+label',
    domain: {'x': [0, 1], 'y': [0, 1]},
  }
  ];

  const layout = {
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
  // `dataAsArrays` is just `data` but with each row as an array instead of an object,
  // to allow sharing the "most" and "least" table code below
  const dataAsArrays = data.map((row) => [getLabel(row), getValue(row)]);

  Plotly.newPlot(domElement.querySelector('.plotly-graph'), plotlyData, layout);
  drawTables(domElement, dataAsArrays);
}

async function drawBarChart(domElement, {xLabel, yLabel, endpoint, getX, getY}) {
  const data = await fetchData(endpoint);

const       plotlyData = [
        {
          x: data.map(getX),
          y: data.map(getY),
          marker: {color: 'rgba(5,112,1,0.65)'},
          textinfo: 'none'
        }
      ];
      layout = {
        xaxis: {title: {text: xLabel}},
        yaxis: {title: {text: yLabel}},
        barcornerradius: 7,

      };

  // `dataAsArrays` is just `data` but with each row as an array instead of an object,
  // to allow sharing the "most" and "least" table code below
  const dataAsArrays = data.map((row) => [getX(row),getY(row)]);

  Plotly.newPlot(domElement.querySelector('.plotly-graph'), plotlyData, layout);
  drawTables(domElement, dataAsArrays);
}

drawPieChart(document.querySelector('.commits-per-author-container'), {getLabel(row) { return row.author }, getValue(row) { return row.commit_count }, endpoint: 'commits-per-author' });
drawBarChart(document.querySelector('.code-lines-in-files-per-project-container'), {
  xLabel: 'File',
  yLabel: 'Lines of code',
  getX: (row) => row.path,
  getY: (row) => row.line_count,
  endpoint: 'line-counts-per-file',
});
drawHistogram(
  document.querySelector('.commits-over-time-container'),
  {
    getX: (commit) => commit.date,
    xLabel: 'Date',
    yLabel: 'Commit count',
    endpoint: 'commit-dates',
  }
);

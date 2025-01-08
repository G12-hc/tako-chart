const queryElements = new URL(document.location.toString()).searchParams;
let currentRepo1 = queryElements.get("repo1");
let currentRepo2 = queryElements.get("repo2");

// Update a chart based on repo, graphId, and chart type
function updateChart(repo, graphId, chartType) {
  if (repo) {
    drawChartsForRepo(repo, graphId, chartType);
  }
}

function clearTables(element) {
 const mostTable = element.querySelector(".most-table");
 const leastTable = element.querySelector(".least-table"); 
 clearTable(mostTable);
 clearTable(leastTable);
}

function clearTable(table) {
  while (table.lastElementChild.nodeName.toLowerCase() === "tr") {
    table.removeChild(table.lastElementChild);
  }
}

function drawTables(element, data) {
  const mostTable = element.querySelector(".most-table");
  const leastTable = element.querySelector(".least-table");

  const highest = data.slice(0, 3);
  const lowest = data.slice(Math.max(data.length - 3, 0)).reverse();

  clearTable(mostTable);
  clearTable(leastTable);

  var i = 0;

  for (const [author, commitCount] of highest) {
    const row = document.createElement("tr");
    mostTable.appendChild(row);
    const rankCell = document.createElement("td");
    rankCell.textContent = `${i + 1}`;
    row.appendChild(rankCell);
    const authorCell = document.createElement("td");
    authorCell.textContent = `${author} (${commitCount} commits)`;
    row.appendChild(authorCell);

    i++;
  }

  i = data.length;

  for (const [author, commitCount] of lowest) {
    const row = document.createElement("tr");
    leastTable.appendChild(row);
    const rankCell = document.createElement("td");
    rankCell.textContent = `${i}`;
    row.appendChild(rankCell);
    const authorCell = document.createElement("td");
    authorCell.textContent = `${author} (${commitCount} commits)`;
    row.appendChild(authorCell);

    i--;
  }
}

// Update both charts when the global chart type changes
function updateAllCharts() {
  const chartType = document.getElementById("global_type_chart").value;
  updateChart(currentRepo1, "plotly-graph1", chartType);
  updateChart(currentRepo2, "plotly-graph2", chartType);
}

// Add event listeners for global chart type and dropdowns
document.getElementById("global_type_chart").onchange = updateAllCharts;

document.getElementById("repos-dropdown1").onchange = function () {
  currentRepo1 = this.value;
  updateAllCharts();
};

document.getElementById("repos-dropdown2").onchange = function () {
  currentRepo2 = this.value;
  updateAllCharts();
};

// Initialize repository dropdowns
async function initReposDropdown(dropdown, queryKey) {
  try {
    const response = await fetch("/api/repos");

    if (!response.ok) {
      console.error("Failed to fetch repositories:", response.status);
      return;
    }
    dropdown.textContent = "";
    const repos = await response.json();
    // Insert an initial empty option
    const emptyOption = document.createElement("option");
    emptyOption.textContent = "--Select a repository--";
    emptyOption.value = "";
    dropdown.appendChild(emptyOption);
    for (const { id, name, owner } of repos.repos) {
      const option = document.createElement("option");
      option.textContent = `${owner}/${name}`;
      option.value = id;
      dropdown.appendChild(option);

      if (queryElements.get(queryKey) === id) {
        option.selected = true;
      }
    }

    dropdown.onchange(); // Trigger initial update for preselected values
  } catch (error) {
    console.error("Error initializing repositories:", error);
  }
}

// Centralized chart-drawing logic
function drawChartsForRepo(repo, graphId, chartType) {
  const chartMapping = {
    "commits-by-author": drawPieChart,
    "lines-per-file": drawBarChart,
    "functional-lines-per-file": drawBarChart,
    "commits-over-time": drawHistogram,
  };

  const chartFunc = chartMapping[chartType];
  if (chartFunc) {
    chartFunc(document.getElementById(graphId), {
      repo,
      endpoint: getEndpointForChart(chartType),
      getX: getXForChart(chartType),
      getY: getYForChart(chartType),
      getLabel: getLabelForChart(chartType),
      getValue: getValueForChart(chartType),
    });
  }
}

// Chart-specific configuration mappings
function getEndpointForChart(chartType) {
  return {
    "commits-by-author": "commits-per-author",
    "lines-per-file": "line-counts-per-file",
    "functional-lines-per-file": "functional-line-counts-per-file",
    "commits-over-time": "commit-dates",
  }[chartType];
}

function getXForChart(chartType) {
  return (
    {
      "lines-per-file": (row) => row.path,
      "functional-lines-per-file": (row) => row.path,
      "commits-over-time": (commit) => commit.date,
    }[chartType] || (() => null)
  );
}

function getYForChart(chartType) {
  return (
    {
      "lines-per-file": (row) => row.line_count,
      "functional-lines-per-file": (row) => row.functional_line_count,
      "commits-over-time": () => null,
    }[chartType] || (() => null)
  );
}

function getLabelForChart(chartType) {
  return (
    {
      "commits-by-author": (row) => row.author,
    }[chartType] || (() => null)
  );
}

function getValueForChart(chartType) {
  return (
    {
      "commits-by-author": (row) => row.commit_count,
    }[chartType] || (() => null)
  );
}

// Fetch data utility
async function fetchData({ endpoint, repo }) {
  // Fetch data for the chart
  const uri = `/api/chart-data/${endpoint}/${repo}`;
  const data = await fetch(uri);

  if (data.ok) {
    return JSON.parse(await data.text());
  }
}

// Chart rendering functions
async function drawPieChart(
  domElement,
  { endpoint, getLabel, getValue, repo },
) {
  const data = await fetchData({ endpoint, repo });
  const plotlyData = [
    {
      labels: data.map(getLabel),
      values: data.map(getValue),
      type: "pie",
      textinfo: "none",
      showlegend: false,
      hoverinfo: "percent+label",
      domain: { x: [0, 1], y: [0, 1] },
    },
  ];
  const layout = { margin: { l: 50, r: 50, t: 25, b: 25, pad: 2 } };
  const dataAsArrays = data.map((row) => [getLabel(row), getValue(row)]);
  Plotly.newPlot(domElement, plotlyData, layout);
  console.log(dataAsArrays);
  let element;
  if (domElement.id === "plotly-graph2") {
    element = ".plotly-graph2-table";
  } else {
    element = ".plotly-graph1-table";
  }
  drawTables(document.querySelector(element), dataAsArrays);
}

async function drawBarChart(
  domElement,
  { xLabel, yLabel, endpoint, getX, getY, repo },
) {
  const data = await fetchData({ endpoint, repo });

  const plotlyData = [
    {
      x: data.map(getX),
      y: data.map(getY),
      type: "bar",
      marker: { color: "rgba(5,112,1,0.65)" },
      textinfo: "none",
    },
  ];
  const layout = {
    xaxis: { title: { text: xLabel }, showticklabels: false },
    yaxis: { title: { text: yLabel }, barcornerradius: 7 },
  };

  const dataAsArrays = data.map((row) => [getX(row), getY(row)]);
  Plotly.newPlot(domElement, plotlyData, layout);
  let element;
  if (domElement.id === "plotly-graph2") {
    element = ".plotly-graph2-table";
  } else {
    element = ".plotly-graph1-table";
  }
  drawTables(document.querySelector(element), dataAsArrays);
}

async function drawHistogram(
  domElement,
  { xLabel, yLabel, endpoint, getX, repo },
) {
  const data = await fetchData({ endpoint, repo });

  const plotlyData = [
    {
      x: data.map(getX),
      type: "histogram",
      marker: { color: "rgba(5,112,1,0.65)" },
    },
  ];
  const layout = {
    xaxis: { title: { text: xLabel } },
    yaxis: { title: { text: yLabel } },
  };
  Plotly.newPlot(domElement, plotlyData, layout);
  let element;
  if (domElement.id === "plotly-graph2") {
    element = ".plotly-graph2-table";
  } else {
    element = ".plotly-graph1-table";
  }
  clearTables(document.querySelector(element));
}

// Initialize dropdowns for the two repositories
initReposDropdown(document.getElementById("repos-dropdown1"), "repo1");
initReposDropdown(document.getElementById("repos-dropdown2"), "repo2");

// Ensure charts are drawn on page load
updateAllCharts();

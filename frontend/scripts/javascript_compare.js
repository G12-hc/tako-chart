const queryElements = new URL(document.location.toString()).searchParams;
const currentRepo1 = queryElements.get("repo1");
const currentRepo2 = queryElements.get("repo2");

if (currentRepo1 || currentRepo2) {
  // Initialize both graphs
  if (currentRepo1) {
    drawChartsForRepo(currentRepo1, "plotly-graph1", "dropdown_type_chart1");
  }
  if (currentRepo2) {
    drawChartsForRepo(currentRepo2, "plotly-graph2", "dropdown_type_chart2");
  }
}

async function initReposDropdown(dropdown, graphId, chartTypeDropdownId, queryKey) {
  const data = await fetch("/api/repos");

  if (!data.ok) {
    console.error("Failed to fetch repositories", data.status);
    return;
  }

  const repos = JSON.parse(await data.text()).repos;

  for (const { id, name, owner } of repos) {
    const option = document.createElement("option");
    option.textContent = `${owner}/${name}`;
    option.value = id;
    dropdown.appendChild(option);

    if (queryElements.get(queryKey) === id) {
      option.selected = "selected";
    }
  }

  dropdown.onchange = function () {
    const selectedRepo = dropdown.value;
    const params = new URLSearchParams(document.location.search);
    params.set(queryKey, selectedRepo);

    // Update URL without refreshing
    history.replaceState(null, "", `?${params.toString()}`);

    // Draw charts for the selected repo
    drawChartsForRepo(selectedRepo, graphId, chartTypeDropdownId);
  };
}

function drawChartsForRepo(repo, graphId, chartTypeDropdownId) {
  const chartTypeDropdown = document.getElementById(chartTypeDropdownId);

  const chartMapping = {
    pie: drawPieChart,
    bar: drawBarChart,
    hist: drawHistogram,
  };

  const chartType = chartTypeDropdown.value || "pie"; // Default to Pie Chart
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

  chartTypeDropdown.onchange = function () {
    const newChartType = chartTypeDropdown.value;
    const newChartFunc = chartMapping[newChartType];

    if (newChartFunc) {
      newChartFunc(document.getElementById(graphId), {
        repo,
        endpoint: getEndpointForChart(newChartType),
        getX: getXForChart(newChartType),
        getY: getYForChart(newChartType),
        getLabel: getLabelForChart(newChartType),
        getValue: getValueForChart(newChartType),
      });
    }
  };
}

function getEndpointForChart(chartType) {
  const endpoints = {
    pie: "commits-per-author",
    bar: "line-counts-per-file",
    hist: "commit-dates",
  };
  return endpoints[chartType];
}

function getXForChart(chartType) {
  const getXFuncs = {
    bar: (row) => row.path,
    hist: (commit) => commit.date,
  };
  return getXFuncs[chartType] || (() => null);
}

function getYForChart(chartType) {
  const getYFuncs = {
    bar: (row) => row.line_count,
    hist: () => null,
  };
  return getYFuncs[chartType] || (() => null);
}

function getLabelForChart(chartType) {
  const getLabelFuncs = {
    pie: (row) => row.author,
  };
  return getLabelFuncs[chartType] || (() => null);
}

function getValueForChart(chartType) {
  const getValueFuncs = {
    pie: (row) => row.commit_count,
  };
  return getValueFuncs[chartType] || (() => null);
}

async function fetchData({ endpoint, repo }) {
  const uri = `/api/chart-data/${endpoint}/${repo}`;
  const data = await fetch(uri);

  if (data.ok) {
    return JSON.parse(await data.text());
  } else {
    console.error("Failed to fetch chart data", data.status);
  }
}

async function drawPieChart(domElement, { endpoint, getLabel, getValue, repo }) {
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

  Plotly.newPlot(domElement, plotlyData, {
    margin: { t: 20, b: 20, l: 20, r: 20 },
  });
}

async function drawBarChart(domElement, { xLabel, yLabel, endpoint, getX, getY, repo }) {
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

  Plotly.newPlot(domElement, plotlyData, {
    xaxis: { title: xLabel },
    yaxis: { title: yLabel },
  });
}

async function drawHistogram(domElement, { xLabel, yLabel, endpoint, getX, repo }) {
  const data = await fetchData({ endpoint, repo });

  const plotlyData = [
    {
      x: data.map(getX),
      type: "histogram",
      marker: { color: "rgba(5,112,1,0.65)" },
    },
  ];

  Plotly.newPlot(domElement, plotlyData, {
    xaxis: { title: xLabel },
    yaxis: { title: yLabel },
  });
}

// Initialize dropdowns for the two repositories
initReposDropdown(
  document.getElementById("repos-dropdown1"),
  "plotly-graph1",
  "dropdown_type_chart1",
  "repo1"
);

initReposDropdown(
  document.getElementById("repos-dropdown2"),
  "plotly-graph2",
  "dropdown_type_chart2",
  "repo2"
);

const queryElements = new URL(document.location.toString()).searchParams;
const currentRepo1 = queryElements.get("repo1");
const currentRepo2 = queryElements.get("repo2");

initializepage();
// Initialize charts for both repositories if they exist
if (currentRepo1) {
  drawChartsForRepo("repo1", currentRepo1, ".chart-content:nth-of-type(1)");
}

if (currentRepo2) {
  drawChartsForRepo("repo2", currentRepo2, ".chart-content:nth-of-type(2)");
}

async function initReposDropdown(dropdownId, queryParam, chartContainerClass) {
  const dropdown = document.getElementById(dropdownId);
  const data = await fetch("/api/repos");

  if (!data.ok) {
    console.error("Error fetching repositories");
    return;
  }

  const repos = JSON.parse(await data.text()).repos;

  for (const { id, name, owner } of repos) {
    const option = document.createElement("option");
    option.textContent = `${owner}/${name}`;
    option.value = id;
    dropdown.appendChild(option);
    if (queryParam === id) {
      option.selected = "selected";
    }
  }

  dropdown.onchange = function () {
    const selectedRepo = dropdown.value;
    const params = new URLSearchParams(document.location.search);
    params.set(dropdownId === "repos-dropdown1" ? "repo1" : "repo2", selectedRepo);
    document.location.search = params.toString();
  };
}

async function drawChartsForRepo(repoKey, repoId, containerSelector) {
  const container = document.querySelector(containerSelector);

  // Draw pie chart for commits per author
  await drawPieChart(container, {
    getLabel: (row) => row.author,
    getValue: (row) => row.commit_count,
    endpoint: "commits-per-author",
    repo: repoId,
  });

  // Draw bar chart for lines of code per file
  await drawBarChart(container, {
    xLabel: "File",
    yLabel: "Lines of code",
    getX: (row) => row.path,
    getY: (row) => row.line_count,
    endpoint: "line-counts-per-file",
    repo: repoId,
  });

  // Draw histogram for commits over time
  await drawHistogram(container, {
    getX: (commit) => commit.date,
    xLabel: "Date",
    yLabel: "Commit count",
    endpoint: "commit-dates",
    repo: repoId,
  });
}

async function fetchData({ endpoint, repo }) {
  const uri = `/api/chart-data/${endpoint}/${repo}`;
  const data = await fetch(uri);

  if (!data.ok) {
    console.error("Error fetching chart data");
    return [];
  }

  return JSON.parse(await data.text());
}

function drawGraph(domElement, { type, data, layout }) {
  Plotly.newPlot(domElement.querySelector(".plotly-graph"), data, layout);
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
    },
  ];

  const layout = {
    height: 300,
    width: 600,
  };

  drawGraph(domElement, { type: "pie", data: plotlyData, layout });
}

async function drawBarChart(domElement, { xLabel, yLabel, endpoint, getX, getY, repo }) {
  const data = await fetchData({ endpoint, repo });

  const plotlyData = [
    {
      x: data.map(getX),
      y: data.map(getY),
      type: "bar",
      marker: { color: "rgba(5,112,1,0.65)" },
    },
  ];

  const layout = {
    xaxis: { title: xLabel },
    yaxis: { title: yLabel },
  };

  drawGraph(domElement, { type: "bar", data: plotlyData, layout });
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

  const layout = {
    xaxis: { title: xLabel },
    yaxis: { title: yLabel },
  };

  drawGraph(domElement, { type: "histogram", data: plotlyData, layout });
}


async function initializePage() {
  await initReposDropdown("repos-dropdown1", currentRepo1, "plotly-graph1");
  await initReposDropdown("repos-dropdown2", currentRepo2, "plotly-graph2");

  const dropdown = document.getElementById("repos-dropdown");
  const graphContainers = document.querySelectorAll(".plotly-graph");

  // Initialize graphs for the query params if provided
  if (currentRepo1) {
    updateGraph(currentRepo1, "plotly-graph1");
  }

  if (currentRepo2) {
    updateGraph(currentRepo2, "plotly-graph2");
  }
}
  // Fetch repositories and populate the dropdown
  const data = await fetch("/api/repos");
  if (!data.ok) {
    console.error("Error fetching repositories");
    return;
  }

  const repos = JSON.parse(await data.text()).repos;
  for (const { id, name, owner } of repos) {
    const option = document.createElement("option");
    option.textContent = `${owner}/${name}`;
    option.value = id;
    dropdown.appendChild(option);
  }

  // Add event listener to update graphs
  dropdown.onchange = () => {
    const selectedRepo = dropdown.value;
    if (!selectedRepo) return;

    // Update graphs for each container
    graphContainers.forEach((container, index) => {
      if (index === 0) {
        drawPieChart(container, {
          endpoint: "commits-per-author",
          getLabel: (row) => row.author,
          getValue: (row) => row.commit_count,
          repo: selectedRepo,
        });
      } else if (index === 1) {
        drawBarChart(container, {
          xLabel: "File",
          yLabel: "Lines of Code",
          endpoint: "line-counts-per-file",
          getX: (row) => row.path,
          getY: (row) => row.line_count,
          repo: selectedRepo,
        });
      } else if (index === 2) {
        drawHistogram(container, {
          xLabel: "Date",
          yLabel: "Commit Count",
          endpoint: "commit-dates",
          getX: (row) => row.date,
          repo: selectedRepo,
        });
      }
    });
  };
}

const dropdown1 = document.getElementById("repos-dropdown1");
const dropdown2 = document.getElementById("repos-dropdown2");

dropdown1.onchange = () => updateGraph(dropdown1.value, "plotly-graph1");
dropdown2.onchange = () => updateGraph(dropdown2.value, "plotly-graph2");

async function initializeSingleGraphPage() {
  const graphContainer = document.getElementById("single-graph-container");
  const dropdown = document.getElementById("repo-dropdown");

  // Populate the dropdown with repositories
  const data = await fetch("/api/repos");
  if (!data.ok) {
    console.error("Error fetching repositories");
    return;
  }

  const repos = JSON.parse(await data.text()).repos;

  for (const { id, name, owner } of repos) {
    const option = document.createElement("option");
    option.textContent = `${owner}/${name}`;
    option.value = id;
    dropdown.appendChild(option);
  }

  // Event listener for dropdown to render the graph
  dropdown.onchange = () => {
    const selectedRepo = dropdown.value;
    updateGraph(selectedRepo, "single-graph-container");
  };
}

function updateGraph(repoId, graphId) {
  const graphElement = document.getElementById(graphId);

  // Check if the graph container exists
  if (!graphElement) {
    console.error(`Graph element with ID '${graphId}' not found`);
    return;
  }

  // Clear any existing graph
  graphElement.innerHTML = "";

  // Choose which graph to render (for simplicity, using a bar chart here)
  drawBarChart(graphElement, {
    xLabel: "File",
    yLabel: "Lines of Code",
    endpoint: "line-counts-per-file",
    getX: (row) => row.path,
    getY: (row) => row.line_count,
    repo: repoId,
  });
}

// Call the correct initializer based on the page's purpose
if (document.getElementById("single-graph-container")) {
  initializeSingleGraphPage();
} else {
  initializePage();
}
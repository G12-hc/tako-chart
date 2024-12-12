// Get query parameters from the URL
const queryElements = new URL(document.location.toString()).searchParams;
const currentRepo1 = queryElements.get("repo1");
const currentRepo2 = queryElements.get("repo2");

// Initialize dropdowns and graphs
initializePage();

async function initializePage() {
  const isComparePage = document.getElementById("repos-dropdown2") !== null;

  if (isComparePage) {
    await initReposDropdown("repos-dropdown1", currentRepo1, "plotly-graph1");
    await initReposDropdown("repos-dropdown2", currentRepo2, "plotly-graph2");

    if (currentRepo1) {
      updateGraph(currentRepo1, "plotly-graph1");
    }
    if (currentRepo2) {
      updateGraph(currentRepo2, "plotly-graph2");
    }
  } else {
    await initReposDropdown("repos-dropdown", currentRepo1, "plotly-graph");
    if (currentRepo1) {
      updateGraph(currentRepo1, "plotly-graph");
    }
  }
}

async function initReposDropdown(dropdownId, queryParam, graphId) {
  const dropdown = document.getElementById(dropdownId);
  if (!dropdown) {
    console.error(`Dropdown with ID '${dropdownId}' not found.`);
    return;
  }

  try {
    const response = await fetch("/api/repos");
    if (!response.ok) {
      console.error("Error fetching repositories", response.status);
      return;
    }

    const { repos } = await response.json();
    repos.forEach(({ id, name, owner }) => {
      const option = document.createElement("option");
      option.textContent = `${owner}/${name}`;
      option.value = id;
      dropdown.appendChild(option);

      // Pre-select the dropdown option if it matches the query parameter
      if (queryParam === id) {
        option.selected = true;
      }
    });

    dropdown.onchange = () => {
      const selectedRepo = dropdown.value;
      const params = new URLSearchParams(document.location.search);
      if (dropdownId === "repos-dropdown1" || dropdownId === "repos-dropdown2") {
        params.set(dropdownId === "repos-dropdown1" ? "repo1" : "repo2", selectedRepo);
      } else {
        params.set("repo1", selectedRepo);
      }
      document.location.search = params.toString();
    };
  } catch (error) {
    console.error("Error initializing dropdown:", error);
  }
}

async function updateGraph(repoId, graphId) {
  const graphElement = document.getElementById(graphId);
  if (!graphElement) {
    console.error(`Graph element with ID '${graphId}' not found.`);
    return;
  }

  // Clear existing graph content
  graphElement.innerHTML = "";

  // Fetch and render the required charts
  try {
    await drawPieChart(graphElement, {
      endpoint: "commits-per-author",
      getLabel: (row) => row.author,
      getValue: (row) => row.commit_count,
      repo: repoId,
    });

    await drawBarChart(graphElement, {
      xLabel: "File",
      yLabel: "Lines of Code",
      endpoint: "line-counts-per-file",
      getX: (row) => row.path,
      getY: (row) => row.line_count,
      repo: repoId,
    });

    await drawHistogram(graphElement, {
      xLabel: "Date",
      yLabel: "Commit Count",
      endpoint: "commit-dates",
      getX: (commit) => commit.date,
      repo: repoId,
    });
  } catch (error) {
    console.error("Error updating graph:", error);
  }
}

async function fetchData({ endpoint, repo }) {
  // Fetch data for the chart
  const uri = `/api/chart-data/${endpoint}/${repo}`;
  const data = await fetch(uri);

  if (data.ok) {
    return JSON.parse(await data.text());
  } else {
    // TODO: error
  }
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
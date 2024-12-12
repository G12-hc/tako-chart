// Get query parameters from the URL
const queryElements = new URL(document.location.toString()).searchParams;
const currentRepo1 = queryElements.get("repos-dropdown-compare-page-select");
const currentRepo2 = queryElements.get("repos-dropdown-compare-page-select-comparison");

// Determine if the page is a single-repo or multi-repo page
const isSingleRepoPage = document.getElementById("repos-dropdown");

// Initialize page based on type
if (isSingleRepoPage) {
  initializeSingleRepoPage();
} else {
  initializeMultiRepoPage();
}

async function initializeSingleRepoPage() {
  await initReposDropdown("repos-dropdown", currentRepo1);
  if (currentRepo1) {
    await updateGraphsForRepo(currentRepo1);
  }
}

async function initializeMultiRepoPage() {
  await initReposDropdown("repos-dropdown-compare-page-select", currentRepo1);
  await initReposDropdown("repos-dropdown-compare-page-select-comparison", currentRepo2);

  if (currentRepo1) {
    await updateGraphsForRepo(currentRepo1, "plotly-graph1");
  }

  if (currentRepo2) {
    await updateGraphsForRepo(currentRepo2, "plotly-graph2");
  }
}

async function initReposDropdown(dropdownId, queryParam) {
  const dropdown = document.getElementById(dropdownId);
  if (!data.ok) {
    console.error("Error fetching repositories");
    return;
  }
  if (!dropdown) {
    console.error(`Dropdown with ID '${dropdownId}' not found.`);
    return;
  }

  try {
    const data = await fetch("/api/repos");
    if (!data.ok) {
      console.error("Error fetching repositories", data.status);
      return;
    }

    for (const { id, name, owner } of repos) {
    const option = document.createElement("option");
    option.textContent = `${owner}/${name}`;
    option.value = id;
    dropdown.appendChild(option);
    if (queryParam === id) {
      option.selected = "selected";
    }
  }

    dropdown.onchange = () => {
      const selectedRepo = dropdown.value;
      const params = new URLSearchParams(document.location.search);
      params.set(
        dropdownId === "repos-dropdown-compare-page-select" ? "repos-dropdown-compare-page-select" : "repos-dropdown-compare-page-select-comparison",
        selectedRepo
      );
      document.location.search = params.toString();
    };
  } catch (error) {
    console.error("Error initializing dropdown:", error);
  }
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

function drawGraph(domElement, { type, data, layout }) {
  Plotly.newPlot(domElement.querySelector(".plotly-graph"), data, layout);
}


async function updateGraphsForRepo(repoId, graphContainerId) {
  // Identify containers for single or multi-repo pages
  const graphContainers = graphContainerId
    ? [document.getElementById(graphContainerId)]
    : document.querySelectorAll(".plotly-graph");

  if (!graphContainers || graphContainers.length === 0) {
    console.error("No graph containers found.");
    return;
  }

  graphContainers.forEach((container, index) => {
    container.innerHTML = ""; // Clear existing content

    if (index === 0 || graphContainerId === "plotly-graph1") {
      drawPieChart(container, {
        endpoint: "commits-per-author",
        getLabel: (row) => row.author,
        getValue: (row) => row.commit_count,
        repo: repoId,
      });
    } else if (index === 1 || graphContainerId === "plotly-graph2") {
      drawBarChart(container, {
        xLabel: "File",
        yLabel: "Lines of Code",
        endpoint: "line-counts-per-file",
        getX: (row) => row.path,
        getY: (row) => row.line_count,
        repo: repoId,
      });
    } else {
      drawHistogram(container, {
        xLabel: "Date",
        yLabel: "Commit Count",
        endpoint: "commit-dates",
        getX: (row) => row.date,
        repo: repoId,
      });
    }
  });
}

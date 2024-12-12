const queryElements = new URL(document.location.toString()).searchParams;
const currentRepo = queryElements.get("repo");

if (currentRepo !== "") {
  drawPieChart(document.querySelector(".commits-per-author-container"), {
    getLabel: (row) => row.author,
    getValue: (row) => row.commit_count,
    endpoint: "commits-per-author",
    repo: currentRepo,
  });

  drawBarChart(
    document.querySelector(".code-lines-in-files-per-project-container"),
    {
      xLabel: "File",
      yLabel: "Lines of code",
      getX: (row) => row.path,
      getY: (row) => row.line_count,
      endpoint: "line-counts-per-file",
      repo: currentRepo,
    },
  );
  drawHistogram(document.querySelector(".commits-over-time-container"), {
    getX: (commit) => commit.date,
    xLabel: "Date",
    yLabel: "Commit count",
    endpoint: "commit-dates",
    repo: currentRepo,
  });
}

async function initReposDropdown() {
  // Fetch data from the repository
  const data = await fetch("/api/repos");

  if (!data.ok) {
    // TODO: error
  }

  const repos = JSON.parse(await data.text()).repos;
  const dropdown = document.getElementById("repos-dropdown");

  for (const { id, name, owner } of repos) {
    const option = document.createElement("option");
    option.textContent = `${owner}/${name}`;
    option.value = id;
    dropdown.appendChild(option);
    if (currentRepo === id) {
      option.selected = "selected";
    }
  }

  dropdown.onchange = function () {
    // If a repo is selected, draw the charts for it
    // TODO: encode query properly
    document.location.search = `?repo=${dropdown.value}`;
  };
}

initReposDropdown();

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

function drawTables(element, data) {
  const mostCommitsTable = element.querySelector(".most-table");
  const leastCommitsTable = element.querySelector(".least-table");

  const highestCommitters = data.slice(0, 3);
  const lowestCommitters = data.slice(Math.max(data.length - 3, 0)).reverse();

  var i = 0;

  for (const [author, commitCount] of highestCommitters) {
    const row = document.createElement("tr");
    mostCommitsTable.appendChild(row);
    const rankCell = document.createElement("td");
    rankCell.textContent = `${i + 1}`;
    row.appendChild(rankCell);
    const authorCell = document.createElement("td");
    authorCell.textContent = `${author} (${commitCount} commits)`;
    row.appendChild(authorCell);

    i++;
  }

  i = data.length;

  for (const [author, commitCount] of lowestCommitters) {
    const row = document.createElement("tr");
    leastCommitsTable.appendChild(row);
    const rankCell = document.createElement("td");
    rankCell.textContent = `${i}`;
    row.appendChild(rankCell);
    const authorCell = document.createElement("td");
    authorCell.textContent = `${author} (${commitCount} commits)`;
    row.appendChild(authorCell);

    i--;
  }
}

async function drawHistogram(
  domElement,
  { xLabel, yLabel, endpoint, getX, repo },
) {
  const data = await fetchData({ endpoint, repo });

    const graphDiv = domElement.querySelector(".plotly-graph");
  const button = domElement.querySelector(".fullscreen-button");


  // Set up the Plotly data and layout
  let plotlyData, layout;

  plotlyData = [
    {
      x: data.map(getX),
      type: "histogram",
      marker: { color: "rgba(5,112,1,0.65)" },
    },
  ];

  layout = {
    xaxis: { title: { text: xLabel } },
    yaxis: { title: { text: yLabel } },
  };

  // Render the Plotly graph
  Plotly.newPlot(domElement.querySelector(".plotly-graph"), plotlyData, layout);

    setupFullscreenButton(graphDiv, button);

}


async function drawPieChart(
  domElement,
  { endpoint, getLabel, getValue, repo },
) {
  const data = await fetchData({ endpoint, repo });

    const graphDiv = domElement.querySelector(".plotly-graph");
  const button = domElement.querySelector(".fullscreen-button");


  const plotlyData = [
    {
      labels: data.map(getLabel),
      values: data.map(getValue),
      type: "pie",
      //maybe for loop for the firs 3??
      textinfo: "none",
      showlegend: false,
      hoverinfo: "percent+label",
      domain: { x: [0, 1], y: [0, 1] },
    },
  ];

  const layout = {
    margin: {
      l: 50,
      r: 50,
      t: 25,
      b: 25,
      pad: 2,
    },
  };
  // `dataAsArrays` is just `data` but with each row as an array instead of an object,
  // to allow sharing the "most" and "least" table code below
  const dataAsArrays = data.map((row) => [getLabel(row), getValue(row)]);

  Plotly.newPlot(domElement.querySelector(".plotly-graph"), plotlyData, layout);
  drawTables(domElement, dataAsArrays);

    setupFullscreenButton(graphDiv, button);

}

async function drawBarChart(
  domElement,
  { xLabel, yLabel, endpoint, getX, getY, repo },
) {
  const data = await fetchData({ endpoint, repo });

    const graphDiv = domElement.querySelector(".plotly-graph");
  const button = domElement.querySelector(".fullscreen-button");


  const plotlyData = [
    {
      type: "bar",
      x: data.map(getX),
      y: data.map(getY),
      type: "bar",
      marker: { color: "rgba(5,112,1,0.65)" },
      textinfo: "none",
    },
  ];
  layout = {
    xaxis: {
      title: { text: xLabel },
      showticklabels: false
    },
    yaxis: { title: { text: yLabel } },
    barcornerradius: 7,
  };

  // `dataAsArrays` is just `data` but with each row as an array instead of an object,
  // to allow sharing the "most" and "least" table code below
  const dataAsArrays = data.map((row) => [getX(row), getY(row)]);

  Plotly.newPlot(domElement.querySelector(".plotly-graph"), plotlyData, layout);
  drawTables(domElement, dataAsArrays);

    setupFullscreenButton(graphDiv, button);

}

function setupFullscreenButton(graphDiv, button) {
  button.addEventListener("click", () => {
    if (graphDiv.requestFullscreen) {
      graphDiv.requestFullscreen();
    } else if (graphDiv.mozRequestFullScreen) {
      graphDiv.mozRequestFullScreen();
    } else if (graphDiv.webkitRequestFullscreen) {
      graphDiv.webkitRequestFullscreen();
    } else if (graphDiv.msRequestFullscreen) {
      graphDiv.msRequestFullscreen();
    } else {
      alert("Fullscreen mode is not supported by your browser.");
    }

    document.addEventListener("fullscreenchange", () => {
      if (document.fullscreenElement) {
        graphDiv.style.width = "100vw";
        graphDiv.style.height = "100vh";
      } else {
        graphDiv.style.width = "";
        graphDiv.style.height = "";
      }
      Plotly.Plots.resize(graphDiv);
    });
  });
}

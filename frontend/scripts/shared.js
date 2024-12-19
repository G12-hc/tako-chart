// Fetch data utility
async function fetchData({ endpoint, repo }) {
  // Fetch data for the chart
  const uri = `/api/chart-data/${endpoint}/${repo}`;
  const data = await fetch(uri);

  if (data.ok) {
    return JSON.parse(await data.text());
  }
}

async function populateReposDropdown(dropdown, queryKey) {
  // Fetch data from the repository
  const response = await fetch("/api/repos");

  if (!response.ok) {
    console.error("Failed to fetch repositories:", response.status);
    return;
  }
  // Clear all dropdown options
  dropdown.textContent = "";

  // Insert an initial empty option
  const emptyOption = document.createElement("option");
  emptyOption.textContent = "--Select a repository--";
  emptyOption.value = "";
  dropdown.appendChild(emptyOption);

  const repos = JSON.parse(await response.text()).repos;

  const queryElements = new URL(document.location.toString()).searchParams;

  for (const { id, name, owner } of repos) {
    const option = document.createElement("option");
    option.textContent = `${owner}/${name}`;
    option.value = id;
    dropdown.appendChild(option);
    if (currentRepo === id) {
      option.selected = "selected";
    }
  }

  dropdown.onchange(); // Trigger initial update for preselected values
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

async function drawPieChart(
  domElement,
  { endpoint, getLabel, getValue, repo },
  label,
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
    autosize: true,
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

  Plotly.newPlot(graphDiv, plotlyData, layout, { responsive: true });
  drawTables(domElement, dataAsArrays, label);

  setupFullscreenButton(graphDiv, button);
}

async function drawBarChart(
  domElement,
  { xLabel, yLabel, endpoint, getX, getY, repo },
  label,
) {
  const data = await fetchData({ endpoint, repo });

  const graphDiv = domElement.querySelector(".plotly-graph");
  const button = domElement.querySelector(".fullscreen-button");

  const plotlyData = [
      {
        type: "bar",
        x: data.map(getX),
        y: data.map(getY),
        marker: { color: "rgba(5,112,1,0.65)" },
        textinfo: "none",
      },
    ],
    layout = {
      autosize: true,
      xaxis: {
        title: { text: xLabel },
        showticklabels: false,
      },
      yaxis: { title: { text: yLabel } },
      barcornerradius: 7,
    };

  // `dataAsArrays` is just `data` but with each row as an array instead of an object,
  // to allow sharing the "most" and "least" table code below
  const dataAsArrays = data.map((row) => [getX(row), getY(row)]);

  Plotly.newPlot(graphDiv, plotlyData, layout, { responsive: true });
  drawTables(domElement, dataAsArrays, label);

  setupFullscreenButton(graphDiv, button);
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
    autosize: true,
    xaxis: { title: { text: xLabel } },
    yaxis: { title: { text: yLabel } },
  };

  // Render the Plotly graph
  Plotly.newPlot(graphDiv, plotlyData, layout, { responsive: true });

  setupFullscreenButton(graphDiv, button);
}

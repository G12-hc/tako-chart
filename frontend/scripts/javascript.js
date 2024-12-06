async function fetchData() {
// Fetch data from the repository
    const api = "http://127.0.0.1:8000";
    console.log(api + "/repos/github-168152007")
    const reposData = await fetch(api + "/repos/github-168152007");
    console.log(reposData);
    if (reposData.ok) {
        return JSON.parse(await reposData.text());
    }
}

async function run() {
    var reposData = await fetchData();
    var commitCountsMap = new Map();

    for (const commit of reposData['commits']) {
        const author = commit['author'];
        if (!commitCountsMap.has(author)) {
            commitCountsMap.set(author, 0);
        }
        commitCountsMap.set(author, commitCountsMap.get(author) + 1);
    }

// Sort the commit counts map by number of commits
    commitCountsMap = new Map(Array.from(commitCountsMap.entries()).sort((a, b) => b[1] - a[1]));

    var data = [
        {
            x: Array.from(commitCountsMap.keys()),
            y: Array.from(commitCountsMap.values()),
            marker: {
                color: ['rgb(175,128,89)', 'rgb(175,128,89)']
            },
            type: 'bar'
        }
    ];
    var layout = {
        xaxis: {
            title: {
                text: 'Authors'
            }
        },
        yaxis: {
            title: {
                text: 'Commits'
            }
        },
        barcornerradius: 20,
    };

    Plotly.newPlot('myDiv', data, layout);

const mostCommitsTable = document.querySelector('.most-table');
const leastCommitsTable = document.querySelector('.least-table');

    const highestCommitters = Array.from(commitCountsMap.entries()).slice(0, 3);
    const lowestCommitters = Array.from(commitCountsMap.entries()).slice(Math.max(commitCountsMap.size - 3, 0)).reverse();

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

    i = commitCountsMap.size;

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

run();

async function initReposTable() {
    // Fetch data from the repository
    const data = await fetch("/api/repos");

    if (!data.ok) {
        // TODO: error
        return;
    }

    const repos = JSON.parse(await data.text()).repos;

    // Put data into table
    const managementTable = document.querySelector("#management-table");
    for (const { name, owner, linkedAt, modifiedAt } of repos) {
        // row
        const row = document.createElement("tr");
        managementTable.appendChild(row);

        // repository name (and link)
        const repoCell = document.createElement("td");
        const repoURL = document.createElement("a");
        repoURL.href = 'https://github.com/' + `${owner}/${name}`;
        repoURL.textContent = `${owner}/${name}`;
        row.appendChild(repoCell);
        repoCell.appendChild(repoURL);

    }

}


initReposTable();
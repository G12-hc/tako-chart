async function refreshManagementTable() {
    // Fetch data from the repository
    const data = await fetch("/api/repos");

    if (!data.ok) {
        // TODO: error
        return;
    }

    const repos = JSON.parse(await data.text()).repos;

    // Put data into table
    const managementTable = document.querySelector("#management-table");
    for (const {name, owner, linked_at, modified_at} of repos) {
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

        // linked at
        const linkedAtCell = document.createElement("td");
        const linkedAtString = new Date(linked_at).toLocaleString();
        linkedAtCell.textContent = `${linkedAtString}`;
        row.appendChild(linkedAtCell);

        // modified at
        const modifiedAtCell = document.createElement("td");
        const modifiedAtString = new Date(modified_at).toLocaleString();
        modifiedAtCell.textContent = `${modifiedAtString}`;
        row.appendChild(modifiedAtCell);

        // buttons
        const buttonsCell = document.createElement("td");

        const buttonUpdate = document.createElement("button");
        buttonUpdate.className = "update-button button";
        buttonUpdate.textContent = "Update";
        // TODO: button functionality

        const buttonDelete = document.createElement("button");
        buttonDelete.className = "delete-button button";
        buttonDelete.textContent = "Delete";
        // TODO: button functionality

        row.appendChild(buttonsCell);
        buttonsCell.appendChild(buttonUpdate);
        buttonsCell.appendChild(buttonDelete);
    }

}

document.getElementById("add-repo-btn").onclick = async () => {
  const repoRegex = /^(\w+(-?|\.?|_?)+)+(\/{1})(\w+(-?|\.?|_?)+)+$/g;

  // const repo = prompt("Owner/Repository\nex. (g12-hc/tako-chart)");
    const repo = document.getElementById("repo-url").value;
    debugger;
  if (!repo) return;
  if (repo.match(repoRegex) === null) {
    alert(`"${repo}" is not a valid repository string!`);
    return;
  }

  const response = await fetch(`/api/fetch-repo/${encodeURIComponent(repo)}`, {
    method: "POST",
  });

  if (!response.ok) {
    alert(
      `Fetching repository failed with HTTP status code ${response.status}`,
    );
    return;
  }

  alert("Repo fetched successfully!");
  // Reload to update repo list
  location.reload();
};


// Run stuff:
refreshManagementTable();
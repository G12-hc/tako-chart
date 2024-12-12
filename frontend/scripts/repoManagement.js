
async function initReposTable() {
    // Fetch data from the repository
    const data = await fetch("/api/repos");

    if (!data.ok) {
        // TODO: error
    }

    const repos = JSON.parse(await data.text()).repos;


    // Put data into table
    const table = element.querySelector(".repo-table");

}



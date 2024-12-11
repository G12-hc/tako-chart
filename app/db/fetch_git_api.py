import httpx
from httpx import Timeout

from app.config import config

GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = config.get("tokens", "github") # Set this in cfg.ini


async def fetch_github_data(endpoint: str, params: dict = None) -> dict:
    """
    Generic function to interact with GitHub's API.
    :param endpoint: GitHub API endpoint.
    :param params: Additional query parameters.
    :return: JSON response.
    """
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    timeout = Timeout(
        connect=10.0,  # Timeout for establishing the connection
        read=30.0,  # Timeout for receiving the response
        write=30.0,  # Timeout for sending the request
        pool=30.0  # Timeout for getting a connection from the pool
    )

    # Create a client with redirection disabled
    async with httpx.AsyncClient(timeout=timeout, follow_redirects=False) as client:
        response = await client.get(f"{GITHUB_API_URL}{endpoint}", headers=headers, params=params)

        # Handle redirect responses explicitly
        if response.status_code in (301, 302):
            redirect_location = response.headers.get("Location")
            if redirect_location:
                print(f"Redirected to: {redirect_location}")
                return {"redirected_to": redirect_location}

        # Raise an exception for other HTTP errors
        response.raise_for_status()

        # Return the JSON response as a dictionary
        return response.json()


async def get_repository_details(owner: str, repo: str):
    """
    Fetch detailed information about a repository.
    :param owner: Owner of the repository.
    :param repo: Name of the repository.
    :return: JSON response.
    """
    endpoint = f"/repos/{owner}/{repo}"
    return await fetch_github_data(endpoint)

async def get_commit_history(owner: str, repo: str):
    """
    Fetch the commit history for a repository.
    :param owner: Owner of the repository.
    :param repo: Repository name.
    :return: Commit history.
    """
    endpoint = f"/repos/{owner}/{repo}/commits"
    commits = []
    page = 1
    while True:
        params = {"per_page": 100, "page": page}
        page_commits = await fetch_github_data(endpoint, params)
        if not page_commits:
            break
        commits.extend(page_commits)
        page += 1
    return commits
    # return await fetch_github_data(endpoint)

async def get_contributors(owner: str, repo: str):
    """
    Fetch the list of contributors for a repository.
    :param owner: Owner of the repository.
    :param repo: Repository name.
    :return: List of contributors.
    """
    endpoint = f"/repos/{owner}/{repo}/contributors"
    return await fetch_github_data(endpoint)

async def get_file_path(owner, repo, default_branch):
    """
    Fetch the file path for a repository.
    :param owner: Repository owner.
    :param repo: Repository name.
    :param default_branch: Default branch of the repository.
    :return: The first file path found in the repository tree.
    """
    file_path_endpoint = f"/repos/{owner}/{repo}/git/trees/{default_branch}?recursive=1"

    # Fetch the data from the GitHub API
    file_paths_response = await fetch_github_data(file_path_endpoint)

    # Parse the response as JSON
    file_paths_json = file_paths_response

    # Ensure the response contains a 'tree' key
    if "tree" not in file_paths_json:
        raise ValueError("The response does not contain the 'tree' key.")

    # Iterate through the 'tree' list to find file paths
    for path_data in file_paths_json["tree"]:
        # Access the 'path' key in each tree object
        if "path" in path_data:
            final_path = path_data["path"]
            print(f"Found path: {final_path}")
            return final_path

    # If no paths are found, return None or raise an exception
    raise ValueError("No file paths found in the repository tree.")



async def get_files(owner: str, repo: str, default_branch: str = "main"):
    """
    Fetch the list of files for a repository.
    By selecting a branch
    :param owner
    :param repo
    :param default_branch:
    :return
    """
    endpoint = f"/repos/{owner}/{repo}/git/trees/{default_branch}?recursive=1"
    return await fetch_github_data(endpoint)

async def fetch_file_content(owner: str, repo: str, default_branch: str = "main"):
    """
    Fetch the content of a file from GitHub.
    :param owner
    :param repo
    :param default_branch
    :return
    """
    file_path = get_file_path(owner, repo, default_branch)
    endpoint = f"/repos/{owner}/{repo}/contents/{file_path}"
    return await fetch_github_data(endpoint)

async def download_zip(owner: str, repo: str, default_branch: str = "main"):
    """
    Download a tarball file from GitHub.
    :param owner: GitHub repository owner.
    :param repo: GitHub repository name.
    :param default_branch: GitHub branch to download (defaults to "main").
    :return: Content of the tarball file.
    """
    # Define the endpoint to fetch the tarball of the repository
    endpoint = f"/repos/{owner}/{repo}/tarball/{default_branch}"

    # Fetch the tarball, handle redirects automatically using follow_redirects=True
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            response = await client.get(f"{GITHUB_API_URL}{endpoint}")
            response.raise_for_status()  # Raise an exception for HTTP errors (404, 500, etc.)

            # Return the content of the tarball (binary data)
            return response.content
        except httpx.HTTPStatusError as e:
            # Handle specific HTTP errors like 404, 403, etc.
            print(f"HTTP error occurred while fetching tarball: {e}")
            raise
        except httpx.RequestError as e:
            # Handle general request errors (e.g., network issues)
            print(f"An error occurred while requesting the tarball: {e}")
            raise

    # return await fetch_github_data(endpoint)

async def fetch_lang_details(owner: str, repo: str):
    """
    Fetch the language details for a repository.
    """
    endpoint = f"/repos/{owner}/{repo}/languages"
    return await fetch_github_data(endpoint)



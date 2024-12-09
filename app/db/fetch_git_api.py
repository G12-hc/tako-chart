import httpx
from app.config import config

GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = config.get("tokens", "github") # Set this in cfg.ini


async def fetch_github_data(endpoint: str, params: dict = None):
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

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{GITHUB_API_URL}{endpoint}", headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
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
    :param owner:
    :param repo:
    :param default_branch:
    :return:
    """
    file_path_endpoint = f"/repos/{owner}/{repo}/git/trees/{default_branch}?recursive=1"
    file_path = await fetch_github_data(file_path_endpoint)
    for file in file_path:
        path = file["path"]
        return path


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

async def fetch_lang_details(owner: str, repo: str):
    """
    Fetch the language details for a repository.
    """
    endpoint = f"/repos/{owner}/{repo}/languages"
    return await fetch_github_data(endpoint)



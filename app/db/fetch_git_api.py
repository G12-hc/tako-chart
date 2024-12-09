import httpx
from app.config import config

GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = config.get("tokens", "github") # Set this in cfg.ini


async def fetch_github_data(endpoint: str, params: dict = None):
    """
    Generic function to interact with GitHub's API.
    :param endpoint: GitHub API endpoint (e.g., "/repos/owner/repo").
    :param params Query parameters for the API call.
    :return: Parsed JSON response.
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
    :param repo: Repository name.
    :return Repository returned as a dictionary.
    """
    endpoint = f"/repos/{owner}/{repo}"
    return await fetch_github_data(endpoint)

async def get_commit_history(owner: str, repo: str):
    """
    Fetch the commit history for a repository.
    :param owner: Repository owner.
    :param repo: Repository name.
    :return: List of commits.
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
    :param owner: Repository owner.
    :param repo: Repository name.
    :return: List of contributors.
    """
    endpoint = f"/repos/{owner}/{repo}/contributors"
    return await fetch_github_data(endpoint)

async def get_file_path(owner, repo):
    repo_details = await get_repository_details(owner, repo)
    default_branch = repo_details.get("default_branch", "main")
    file_path_endpoint = f"/repos/{owner}/{repo}/git/trees/{default_branch}?recursive=1"
    file_path = await fetch_github_data(file_path_endpoint)
    for file in file_path:
        path = file["path"]
        return path


async def get_files(owner: str, repo: str):
    """
    Fetch the list of files for a repository.
    By selecting a branch
    :param owner: Repo owner.
    :param repo: Repo name.
    :return:
    """
    repo_details = await get_repository_details(owner, repo)
    default_branch = repo_details.get("default_branch", "main")
    endpoint = f"/repos/{owner}/{repo}/git/trees/{default_branch}?recursive=1"
    return await fetch_github_data(endpoint)

async def fetch_file_content(owner: str, repo: str, file_path: str):
    """
    Fetch the content of a file from GitHub.
    """
    file_path = get_file_path(owner, repo)
    endpoint = f"/repos/{owner}/{repo}/contents/{file_path}"
    return await fetch_github_data(endpoint)

async def fetch_lang_details(owner: str, repo: str):
    """
    Fetch the language details for a repository.
    :param owner:
    :param repo:
    :return:
    """
    endpoint = f"/repos/{owner}/{repo}/languages"
    return await fetch_github_data(endpoint)
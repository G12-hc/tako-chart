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
    :param Repository owner
    :param Repository name
    :return: Repository returned as a dictionary.
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
    return await fetch_github_data(endpoint)


async def get_contributors(owner: str, repo: str):
    """
    Fetch the list of contributors for a repository.
    :param owner: Repository owner.
    :param repo: Repository name.
    :return: List of contributors.
    """
    endpoint = f"/repos/{owner}/{repo}/contributors"
    return await fetch_github_data(endpoint)

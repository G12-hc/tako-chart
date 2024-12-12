import httpx
from typing import Optional

from app.config import config

GITHUB_API_URL = "https://api.github.com"
GITHUB_TOKEN = config.get("tokens", "github")  # Set this in cfg.ini


async def fetch_github_data(endpoint: str, params: dict = None) -> dict:
    """
    Generic function to interact with GitHub's API.
    :param endpoint: GitHub API endpoint.
    :param params: Additional query parameters.
    :return: JSON response.
    """
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    timeout = httpx.Timeout(
        connect=10.0,  # Timeout for establishing the connection
        read=30.0,  # Timeout for receiving the response
        write=30.0,  # Timeout for sending the request
        pool=30.0,  # Timeout for getting a connection from the pool
    )

    # Create a client with redirection disabled
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.get(
            f"{GITHUB_API_URL}{endpoint}", headers=headers, params=params
        )

        # Raise an exception for other HTTP errors
        response.raise_for_status()

        # Return the JSON response as a dictionary
        return response.json()


async def fetch_paginated_github_data(endpoint: str, params: Optional[dict] = None):
    """
    Generic function to interact with GitHub API endpoints that use pagination,
    returning all the pages.
    Generic function to interact with GitHub's API.
    :param endpoint: GitHub API endpoint.
    :param params: Additional query parameters.
    :param paginate: Additional query parameters.
    :return: Combined results from all API calls.
    """
    results = []
    page = 1
    while True:
        # 100 is the max
        params = {"per_page": 100, "page": page}
        page_results = await fetch_github_data(endpoint, params)
        if not page_results:
            break
        results.extend(page_results)
        page += 1
    return results


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
    return await fetch_paginated_github_data(endpoint)


async def get_contributors(owner: str, repo: str):
    """
    Fetch the list of contributors for a repository.
    :param owner: Owner of the repository.
    :param repo: Repository name.
    :return: List of contributors.
    """
    endpoint = f"/repos/{owner}/{repo}/contributors"
    return await fetch_paginated_github_data(endpoint)


async def download_zip(owner: str, repo: str, default_branch: str):
    """
    Download a tarball file from GitHub.
    :param owner: GitHub repository owner.
    :param repo: GitHub repository name.
    :param default_branch: GitHub branch to download.
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


async def fetch_lang_details(owner: str, repo: str):
    """
    Fetch the language details for a repository.
    """
    endpoint = f"/repos/{owner}/{repo}/languages"
    return await fetch_github_data(endpoint)

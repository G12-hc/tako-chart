from app.db.fetch_git_api import get_repository_details, get_commit_history, get_contributors
from app.db.queries import query_insert_commits, query_insert_repository, query_insert_contributors


def assign_repo_data(owner: str, repo: str):
    repo_details = get_repository_details(owner, repo)
    commits = get_commit_history(owner, repo)
    repo_contributors = get_contributors(owner, repo)

    # repo data
    repository_id = "github-"+ repo_details.get("id")
    external_id = repo_details.get("id")
    watchers = repo_details.get("watchers")
    forks_count = repo_details.get("forks_count")
    name = repo_details.get("owner", {}).get("login")
    owner = repo_details.get("owner")
    status = "linked"
    linked_at = repo_details.get("created_at")
    modified_at = repo_details.get("updated_at")
    contributors_url = repo_details.get("contributors_url")
    default_branch = repo_details.get("default_branch")
    user_ids = repo_details.get("owner", {}).get("id")
    archieved_user_ids =  "Something"
    license_id = "find from another table the ID"
    workspace_id =  "No idea"

    # commit data
    for commit_data in commits:
        sha = commit_data.get("sha")
        date = commit_data.get("commit", {}).get("author", {}).get("date")
        message = commit_data.get("commit", {}).get("message")
        author = commit_data.get("commit", {}).get("author", {}).get("name")
        repository_id = "github-" + commit_data.get("commit", {}).get("id", {}).get("id")  # Example repository ID
        query_insert_commits(conn, date,message,author,repository_id)


    # contributor data
    # for repo_contributors in contributors:




    query_insert_repository(conn, repository_id ,external_id, watchers, forks_count, name, owner, status,
                            linked_at, modified_at, contributors_url, default_branch,
                            user_ids, archieved_user_ids, workspace_id,  license_id)
    query_insert_contributors(
        conn,
    )
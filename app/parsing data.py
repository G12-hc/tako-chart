from app.db import get_db_connection
from app.db.fetch_git_api import get_repository_details, get_commit_history, get_contributors
from app.db.queries import query_insert_commits, query_insert_repository


async def assign_repo_data(owner: str, repo: str, null=None):
    conn = get_db_connection()
    repo_details = await get_repository_details(owner, repo)
    commit_data = await get_commit_history(owner, repo)
    # repo_contributors = await get_contributors(owner, repo)

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
    archieved_user_ids =  null
    license_id = "find from another table the ID"
    workspace_id =  null
    path = repo_details.get("full_name")
    description = repo_details.get("description")
    language = repo_details.get("language")



    # commit data
    sha = commit_data.get("sha")
    date = commit_data.get("commit", {}).get("author", {}).get("date")
    message = commit_data.get("commit", {}).get("message")
    author = commit_data.get("commit", {}).get("author", {}).get("name")


    # contributor data
    # for repo_contributors in contributors:
    query_insert_commits(conn, sha, date, message, author, repository_id)
    query_insert_repository(conn, repository_id ,external_id, watchers, forks_count, name, owner, status,
                            linked_at, modified_at, contributors_url, default_branch,
                            user_ids, archieved_user_ids, workspace_id,  license_id)
    query_insert_branches(default_branch, repository_id)
    query_insert_files(is_directory, path, name, line_count, functional_line_count, symlinkTarget, branch_id)
    query_insert_repository_languages(languge_id,repository_id)

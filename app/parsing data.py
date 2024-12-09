import os

from app.count_lines import analyze_repository
from app.db import get_db_connection
from app.db.fetch_git_api import get_repository_details, get_commit_history, get_contributors, get_files, \
    fetch_lang_details
from app.db.queries import query_insert_commits, query_insert_repository, query_insert_files, query_insert_branches, \
    query_insert_languages


async def assign_repo_data(owner: str, repo: str, null=None):
    conn = get_db_connection()
    try:
        repo_details = await get_repository_details(owner, repo)
        commit_data = await get_commit_history(owner, repo)
        # repo_contributors = await get_contributors(owner, repo)
        file_data = await get_files(owner, repo, branch="main")
        lang_data = await fetch_lang_details(owner, repo)
        # repo data
        repository_id = f"github-{repo_details['id']}"
        default_branch = repo_details.get("default_branch", "main")
        workspace_id = None  # Assign workspace ID dynamically if available, not sure what to put
        for lang_name, num_bytes in lang_data.items():
            query_insert_languages(repository_id, lang_name)
        query_insert_repository(
            conn,
            repository_id,
            repo_details["id"],
            repo_details["watchers"],
            repo_details["forks_count"],
            repo_details["name"],
            repo_details["owner"]["login"],
            "linked", # not sure what to put for linked
            repo_details["created_at"],
            repo_details["updated_at"],
            repo_details["contributors_url"],
            default_branch,
            repo_details["owner"]["id"],
            None,  # Archived user IDs
            workspace_id,
        )
        query_insert_branches(default_branch, repository_id)

        for commit in commit_data:
            query_insert_commits(
                conn,
                commit["sha"],
                commit["commit"]["author"]["date"],
                commit["commit"]["message"],
                commit["commit"]["author"]["name"],
                repository_id,
            )

        for file in file_data.get("tree", []):
            path = file["path"]
            analyzed_files = await analyze_repository(owner, repo, branch="main", file_types=[".py", ".js"])
            for file_info in analyzed_files:
                total_lines = file_info["total_lines"]
                functional_lines = file_info["functional_lines"]
                query_insert_files(
                    conn,
                    file["type"] == "tree",  # is directory true
                    path,
                    os.path.basename(path),
                    total_lines,  # total line count
                    functional_lines,  # functional lines
                    None,  # symlinkTarget placeholder as I am unsure
                    "branch_id_placeholder",  # Replace dynamically,
                    # improve query to match a branch ID to the name
                )






        # for repo_contributors in contributors:
        query_insert_repository_languages(languge_id,repository_id)



    except Exception as e:
        print(f"Error processing repository {owner}/{repo}: {e}")
    finally:
        conn.close()
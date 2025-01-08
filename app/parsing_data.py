import os
import asyncio

from datetime import datetime

from app.count_lines import analyze_repository
from app.db import db_connection
from app.fetch_git_api import (
    get_repository_details,
    get_commit_history,
    fetch_lang_details,
    get_contributors,
)
from app.db.queries import (
    query_delete_all_repo_data,
    query_insert_branches,
    query_insert_commits,
    query_insert_files,
    query_insert_language,
    query_insert_licenses,
    query_insert_repository,
)


async def assign_repo_data(owner: str, repo: str):
    async with db_connection() as conn:
        # fetch data from the git api
        [repo_details, commit_data, lang_data, contributor_data] = await asyncio.gather(
            get_repository_details(owner, repo),
            get_commit_history(owner, repo),
            fetch_lang_details(owner, repo),
            get_contributors(owner, repo),
        )

        default_branch = repo_details.get("default_branch", "main")
        # prep repo data
        repository_id = f"github-{repo_details['id']}"
        workspace_id = (
            None  # Assign workspace ID dynamically if available, not sure what to put
        )
        license_id = None  # Is assigned after inset attempt
        user_ids = [user["id"] for user in contributor_data]
        archived_user_ids = [0, 1]
        linked_status = "Linked"

        # Delete repo's data (in case it already exists, to refresh)
        await query_delete_all_repo_data(conn, repository_id)

        # Licence
        if repo_details["license"] is None:
            print("No licenses found")
        else:
            license_id = await query_insert_licenses(
                conn,
                repo_details["license"]["key"],
                repo_details["license"]["name"],
                repo_details["license"]["spdx_id"],
                # Can be null
                repo_details["license"]["url"] or "",
                repo_details["license"]["node_id"],
            )
        # Repository
        await query_insert_repository(
            conn,
            repository_id,
            repo_details["id"],
            repo_details["watchers"],
            repo_details["forks_count"],
            repo_details["name"],
            repo_details["owner"]["login"],
            linked_status,  # not sure what to put for linked
            datetime.now(),
            datetime.now(),
            repo_details["contributors_url"],
            default_branch,
            user_ids,
            archived_user_ids,  # Archived user IDs
            license_id,
            workspace_id,
        )
        # Branches
        await query_insert_branches(conn, default_branch, repository_id)

        # Files
        analyzed_files = await analyze_repository(owner, repo, default_branch)
        for path, data in analyzed_files.items():
            await query_insert_files(
                conn,
                data["is_directory"],
                path,
                os.path.basename(path),
                data.get("line_count", 0),  # total line count (0 for dirs)
                data.get(
                    "functional_line_count", 0
                ),  # functional line count (0 for dirs)
                "",  # symlinkTarget placeholder as I am unsure
                default_branch,  # Replace dynamically
                repository_id,
            )

        for commit in commit_data:
            await query_insert_commits(
                conn,
                commit["sha"],
                commit["commit"]["author"]["date"],
                commit["commit"]["message"],
                commit["commit"]["author"]["name"],
                repository_id,
            )

        for lang_name in lang_data.keys():
            lang_name = str(lang_name)
            await query_insert_language(conn, repository_id, lang_name)

    # except Exception as e:
    #       exc_type, exc_obj, exc_tb = sys.exc_info()
    #       f_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #       print(exc_type, f_name, exc_tb.tb_lineno)
    #       print(f"Error processing repository {owner}/{repo}: {e}")

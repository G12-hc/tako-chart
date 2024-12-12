from datetime import datetime

from psycopg.rows import dict_row
from typing import List


def query(query_function):
    async def wrapper(conn, *args, **kwargs):
        try:
            async with conn.cursor(row_factory=dict_row) as cursor:
                result = await query_function(cursor, *args, **kwargs)

                if result is not None:
                    return result

                if cursor.description is not None:
                    if result == "one":
                        return await cursor.fetchone()
                    return await cursor.fetchall()

                return cursor.rowcount
        except Exception as e:
            print(f"Error executing query: {e}")
            raise

    return wrapper


@query
async def query_repos(cursor):
    await cursor.execute("SELECT * FROM repositories")


@query
async def query_file_by_line_count(cursor, repo_id):
    """
    Fetch files for a specific branch with a minimum line count.
    :param cursor:
    :param repo_id:
    :return:
    """
    params = [repo_id]
    await cursor.execute(
        """
        SELECT
            REGEXP_REPLACE(f.name, '^[^.]*\.', '') AS stripped_name,
            SUM(f.line_count) AS total_line_count
        FROM files f
        JOIN branches b ON f.branch_id = b.id
        JOIN repositories r ON b.repository_id = r.id
        WHERE f.is_directory = FALSE AND r.id = %s
        GROUP BY stripped_name
        ORDER BY stripped_name
        """,
        params,
    )


@query
async def query_insert_commits(cursor, sha, date, message, author, repository_id):
    params = [sha, date, message, author, repository_id]
    await cursor.execute(
        """
        INSERT INTO commits (sha, date, message, author, repository_id)
        VALUES(%s, %s, %s, %s, %s)
        """,
        params,
    )


@query
async def query_insert_repository(
    cursor,
    repository_id: str,
    external_id: int,
    watchers: int,
    forks_count: int,
    name: str,
    owner: str,
    status: str,
    linked_at: datetime,
    modified_at: datetime,
    contributors_url: str,
    default_branch: str,
    user_ids: List[int],
    archieved_user_ids: List[int],
    license_id: int = None,
    workspace_id: str = None,
):
    params = [
        repository_id,
        external_id,
        watchers,
        forks_count,
        name,
        owner,
        status,
        linked_at,
        modified_at,
        contributors_url,
        default_branch,
        user_ids,
        archieved_user_ids,
        license_id,
        workspace_id,
    ]

    await cursor.execute(
        """
        INSERT INTO repositories (id,external_id, watchers, forks_count, name, owner, status, 
                                    linked_at, modified_at, contributors_url, default_branch, 
                                    user_ids, archieved_user_ids, license_id, workspace_id)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        params,
    )


@query
async def query_insert_files(
    cursor,
    is_directory,
    path,
    name,
    line_count,
    functional_line_count,
    symlinkTarget,
    branch_name,
    repo_id,
):
    await cursor.execute(
        """
        INSERT INTO files (is_directory, path, name, line_count, functional_line_count, "symlinkTarget", branch_id)
        SELECT %(is_directory)s, %(path)s, %(name)s, %(line_count)s, %(functional_line_count)s, %(symlink_target)s, b.id
        FROM branches b
        WHERE b.repository_id = %(repo_id)s AND b.name = %(branch_name)s
        """,
        {
            "is_directory": is_directory,
            "path": path,
            "name": name,
            "line_count": line_count,
            "functional_line_count": functional_line_count,
            "symlink_target": symlinkTarget,
            "branch_name": branch_name,
            "repo_id": repo_id,
        },
    )


@query
async def query_insert_branches(cursor, name, repository_id):
    params = [name, repository_id]
    await cursor.execute(
        """
        INSERT INTO branches (name, repository_id)
        VALUES(%s, %s)
        """,
        params,
    )


@query
async def query_insert_language(cursor, repository_id, lang_name: str):
    """
    Inserts a language into the `languages` table if it doesn't already exist.
    Returns the ID of the language.
    """
    await cursor.execute(
        """
        INSERT INTO languages (name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING
        RETURNING id
        """,
        [lang_name],
    )
    result = await cursor.fetchone()

    # If result is not set then (language already exists), else set to the existing ID
    if result is None:
        await cursor.execute("SELECT id FROM languages WHERE name = %s", [lang_name])
        result = cursor.fetchone()
    lang_id = result["id"]
    await cursor.execute(
        """
        INSERT INTO repository_languages (language_id, repository_id)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
        """,
        [lang_id, repository_id],
    )


@query
async def query_insert_licenses(
    cursor, key=None, name=None, spdx_id=None, url=None, node_id=None
):
    """
    Inserts a license into the `licenses` table if it doesn't exist and associates
    it with a repository in the `repositories` table.
    """
    # Check if the license already exists by key or other attributes
    await cursor.execute(
        """
        SELECT id
        FROM licenses
        WHERE 
            key = %s OR
            name = %s OR
            spdx_id = %s OR 
            url = %s OR 
            node_id = %s
        """,
        [key, name, spdx_id, url, node_id],
    )
    lic = await cursor.fetchone()

    # If a license exists, return its ID
    if lic is not None:
        existing_license = lic["id"]
    else:
        # Insert the new license and fetch the ID
        await cursor.execute(
            """
            INSERT INTO licenses (key, name, spdx_id, url, node_id)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
            """,
            [key, name, spdx_id, url, node_id],
        )
        lic = await cursor.fetchone()
        existing_license = lic["id"]

    print("ID inside query: ", existing_license, "Type: ", type(existing_license))
    return existing_license


@query
async def query_commits_per_author(cursor, repo_id):
    params = [repo_id]
    await cursor.execute(
        """
        SELECT c.author, COUNT(DISTINCT c.id) as commit_count
        FROM commits c
        WHERE c.repository_id = %s
        GROUP BY c.author
        ORDER BY commit_count DESC
        """,
        params,
    )


@query
async def query_line_counts_per_file(cursor, repo_id):
    params = [repo_id]
    await cursor.execute(
        """
        SELECT f.path, f.line_count
        FROM files f
        WHERE f.branch_id = (
            SELECT b.id
            FROM branches b
            JOIN repositories r ON r.id = %s AND b.repository_id = r.id
            WHERE r.default_branch = b.name

        )
        ORDER BY f.line_count DESC
        """,
        params,
    )


@query
async def query_functional_line_counts_per_file(cursor, repo_id):
    params = [repo_id]
    await cursor.execute(
        """
        SELECT f.path, f.functional_line_count
        FROM files f
        WHERE f.branch_id = (
            SELECT b.id
            FROM branches b
            JOIN repositories r ON r.id = %s
            WHERE r.default_branch = b.name

        )
        ORDER BY f.functional_line_count DESC
        """,
        params,
    )


@query
async def query_commit_dates(cursor, repo_id):
    params = [repo_id]
    await cursor.execute(
        """
        SELECT c.date
        FROM commits c
        WHERE c.repository_id = %s
        ORDER BY c.date DESC
        """,
        params,
    )

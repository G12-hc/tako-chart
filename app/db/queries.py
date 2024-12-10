from datetime import datetime

from psycopg.rows import dict_row
from typing import List

def query(query_function):
    def wrapper(conn, *args, **kwargs):
        with conn.cursor(row_factory=dict_row) as cursor:
            # Execute the query function
            result = query_function(cursor, *args, **kwargs)

            # If the query function explicitly returns a value, use it
            if result is not None:
                return result

            # Otherwise, handle return value based on query type
            if cursor.description is not None:  # SELECT query
                return cursor.fetchall()  # Fetch all rows by default

            return cursor.rowcount  # For non-SELECT queries, return affected rows count

    return wrapper


@query
def query_repos(cursor):
    cursor.execute("SELECT * FROM repositories")


@query
def query_repo(cursor, repo_id):
    cursor.execute("SELECT * FROM repositories WHERE id = %s", [repo_id])


@query
def query_commit(cursor, repo_id):
    params = [repo_id]
    cursor.execute("""
        SELECT * 
        FROM commits 
        WHERE repository_id = %s
        """, params
                   )


@query
def query_branches(cursor, repo_id):
    params = [repo_id]
    cursor.execute(
        """
        SELECT * 
        FROM branches 
        WHERE repository_id = %s
        """, params
    )


@query
def query_files(cursor, branch_id: int, min_line_count: int = 0):
    """
    Fetch files for a specific branch with a minimum line count.
    """
    cursor.execute(
        """
        SELECT * 
        FROM files 
        WHERE branch_id = %s AND line_count > %s
        """,
        [branch_id, min_line_count],
    )



@query
def query_languages(cursor, repo_id: str):
    params = [repo_id]
    cursor.execute(
        """
        SELECT languages.name 
        FROM languages 
        JOIN repository_languages ON languages.id = repository_languages.language_id
        WHERE repository_languages.repository_id = %s
        """, params
    )


@query
def query_licenses(cursor, repo_id):
    params = [repo_id]
    cursor.execute(
        """
        SELECT licenses.* 
        FROM licenses 
        JOIN repositories ON licenses.id = repositories.license_id
        WHERE repositories.id = %s
        """, params
    )


# Query purpose incase I want to update the branch dynamically
@query
def query_get_branch_id(cursor, branch_name: str, repository_id: str):
    """
    Fetch the branch ID for a specific branch name and repository.
    """
    cursor.execute(
        "SELECT id FROM branches WHERE name = %s AND repository_id = %s",
        [branch_name, repository_id],
    )
    result = cursor.fetchone()
    return result["id"] if result else None


@query
def query_workspaces(cursor, repo_id):
    params = [repo_id]
    cursor.execute(
        """
        SELECT workspaces.* 
        FROM workspaces 
        JOIN repositories ON workspaces.id = repositories.workspace_id
        WHERE repositories.id = %s
        """, params
    )


@query
def query_insert_commits(cursor, sha, date, message, author, repository_id):
    params = [sha, date, message, author, repository_id]
    cursor.execute(
        """
        INSERT INTO commits (sha, date, message, author, repository_id)
        VALUES(%s, %s, %s, %s, %s)
        """, params
    )


@query
def query_insert_repository(cursor,
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
                            workspace_id: str = None):
    params = [repository_id, external_id, watchers, forks_count, name, owner, status,
              linked_at, modified_at, contributors_url, default_branch,
              user_ids, archieved_user_ids, license_id, workspace_id]

    cursor.execute(
        """
        INSERT INTO repositories (id,external_id, watchers, forks_count, name, owner, status, 
                                    linked_at, modified_at, contributors_url, default_branch, 
                                    user_ids, archieved_user_ids, license_id, workspace_id)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, params
    )


@query
def query_insert_files(cursor, is_directory, path, name, line_count, functional_line_count, symlinkTarget, branch_id):
    params = [is_directory, path, name, line_count, functional_line_count, symlinkTarget, branch_id]
    cursor.execute(
        """
        INSERT INTO files (is_directory, path, name, line_count, functional_line_count, "symlinkTarget", branch_id)
        VALUES(%s, %s, %s, %s, %s, %s, %s)
        """, params
    )


@query
def query_insert_branches(cursor, name, repository_id):
    params = [name, repository_id]
    cursor.execute(
        """
        INSERT INTO branches (name, repository_id)
        VALUES(%s, %s)
        """, params
    )


@query
def query_insert_language(cursor, repository_id, lang_name: str):
    """
    Inserts a language into the `languages` table if it doesn't already exist.
    Returns the ID of the language.
    """
    cursor.execute(
        """
        INSERT INTO languages (name)
        VALUES (%s)
        ON CONFLICT (name) DO NOTHING
        RETURNING id
        """,
        [lang_name]
    )
    result = cursor.fetchone()

    # If result is not set then (language already exists), else set to the existing ID
    if result is None:
        cursor.execute("SELECT id FROM languages WHERE name = %s", [lang_name])
        result = cursor.fetchone()
    lang_id = result['id']
    cursor.execute(
        """
        INSERT INTO repository_languages (language_id, repository_id)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
        """,
        [lang_id, repository_id]
    )


@query
def query_insert_licenses(cursor, key=None, name=None, spdx_id=None, url=None, node_id=None):
    """
    Inserts a license into the `licenses` table if it doesn't exist and associates
    it with a repository in the `repositories` table.
    """
    # Check if the license already exists by key or other attributes
    cursor.execute(
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
        [key, name, spdx_id, url, node_id]
    )
    lic = cursor.fetchone()

    # If a license exists, return its ID
    if lic is not None:
        existing_license = lic['id']
    else:
        # Insert the new license and fetch the ID
        cursor.execute(
            """
            INSERT INTO licenses (key, name, spdx_id, url, node_id)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
            """,
            [key, name, spdx_id, url, node_id]
        )
        lic = cursor.fetchone()
        existing_license = lic['id']

    print("ID inside query: ",existing_license, "Type: ", type(existing_license))
    return existing_license



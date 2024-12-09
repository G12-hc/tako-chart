from psycopg.rows import dict_row

def query(query_function):
    def wrapper(conn, *args, **kwargs):
        with conn.cursor(row_factory=dict_row) as cursor:
            query_function(cursor, *args, **kwargs)
            return cursor.fetchall()

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
def query_files(cursor, repo_id):
    params = [repo_id]
    cursor.execute(
        """
        SELECT * 
        FROM files 
        WHERE line_count > %s
        """, params
    )


@query
def query_languages(cursor, repo_id):
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
        """SELECT * 
        FROM licenses 
        WHERE id = (SELECT license_id 
                    FROM repositories 
                    WHERE id = %s)
        """, params
        )

@query
def query_workspaces(cursor, repo_id):
    params = [repo_id]
    cursor.execute(
        """
        SELECT wID.* 
        FROM repositories rID
        JOIN workspaces wID ON rID.workspace_id = wID.id
        WHERE rID.id = %s
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
def query_insert_repository(cursor, repository_id, external_id, watchers, forks_count, name, owner, status,
                                    linked_at, modified_at, contributors_url, default_branch,
                                    user_ids, archieved_user_ids, workspace_id,  license_id):
    params = [repository_id,external_id, watchers, forks_count, name, owner, status,
                                    linked_at, modified_at, contributors_url, default_branch,
                                    user_ids, archieved_user_ids, workspace_id,  license_id]
    cursor.execute(
        """
        INSERT INTO repositories (id,external_id, watchers, forks_count, name, owner, status, 
                                    linked_at, modified_at, contributors_url, default_branch, 
                                    user_ids, archieved_user_ids, workspace_id, license_id)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
@query
def query_insert_languages(cursor, repository_id, name):
    """
    Inserts a language into the `languages` table if it doesn't already exist
    and associates it with the `repository_languages` table.
    """
    # Insert the language if it doesn't exist, returning the ID
    cursor.execute(
        """
        INSERT INTO languages (name)
        VALUES (%s)
        ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name
        RETURNING id
        """,
        [name]
    )
    language_id = cursor.fetchone()["id"]

    # Link the language to the repository
    cursor.execute(
        """
        INSERT INTO repository_languages (repository_id, language_id)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
        """,
        [repository_id, language_id]
    )

@query
@query
def query_insert_licenses(cursor, repository_id, key, name, spdx_id, url, node_id):
    """
    Inserts a license into the `licenses` table if it doesn't exist and associates
    it with a repository in the `repositories` table.
    """
    # Insert or fetch the license
    cursor.execute(
        """
        INSERT INTO licenses (key, name, spdx_id, url, node_id)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (key) DO UPDATE SET
            name = EXCLUDED.name,
            spdx_id = EXCLUDED.spdx_id,
            url = EXCLUDED.url,
            node_id = EXCLUDED.node_id
        RETURNING id
        """,
        [key, name, spdx_id, url, node_id]
    )
    license_id = cursor.fetchone()["id"]

    # Associate the license with the repository
    cursor.execute(
        """
        UPDATE repositories
        SET license_id = %s
        WHERE id = %s
        """,
        [license_id, repository_id]
    )

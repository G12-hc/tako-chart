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
        """,
        params)


@query
def query_branches(cursor, repo_id):
    params = [repo_id]
    cursor.execute(
        """
        SELECT * 
        FROM branches 
        WHERE repository_id = %s
        """,
        params)


@query
def query_files(cursor, repo_id):
    params = [repo_id]
    cursor.execute(
        """
        SELECT * 
        FROM files 
        WHERE line_count > %s
        """,
        params)


@query
def query_languages(cursor, repo_id):
    params = [repo_id]
    cursor.execute(
        """
        SELECT languages.name 
        FROM languages 
        JOIN repository_languages ON languages.id = repository_languages.language_id
        WHERE repository_languages.repository_id = %s
        """,
        params
        )


@query
def query_licenses(cursor, repo_id):
    params = [repo_id]
    cursor.execute(
        """SELECT * 
        FROM licenses 
        WHERE id = (SELECT license_id 
                    FROM repositories 
                    WHERE id = %s)""",
            params
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
        """,
        params
    )





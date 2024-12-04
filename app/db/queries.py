from sqlite3.dbapi2 import paramstyle


def query(query_function):
    def wrapper(conn, *args, **kwargs):
        with conn.cursor() as cursor:
            query_function(cursor, *args, **kwargs)
            return cursor.fetchall()

    return wrapper

@query
def query_commit(cursor, repo_id):
    params = [repo_id]
    cursor.execute("SELECT * FROM commits WHERE repository_id = %s", params)

@query
def query_branches(cursor,repo_id):
    params = [repo_id]
    cursor.execute("SELECT * FROM branches WHERE repository_id = %s", params)

@query
def query_files(cursor, threshold):
    params = [threshold]
    cursor.execute("SELECT * FROM files WHERE line_count > %s", params)

@query
def query_languages(cursor, repo_id):
    params = [repo_id]
    cursor.execute("""
    SELECT language.name 
    FROM languages 
    JOIN repository_language ON languages.id = repository_language.language_id
    WHERE repository_language.repository_id = %s""",params)


@query
def query_licenses(cursor, repo_id):
    params = [repo_id]
    cursor.execute("SELECT * FROM licenses WHERE id = (SELECT license_id FROM repositories WHERE id = %s)",params)

@query
def query_repositories(cursor, repo_id):
    params = [repo_id]
    cursor.execute("""
    SELECT
        (SELECT COUNT(*) FROM commits WHERE repository_id = %s) AS commit_count,
        (SELECT COUNT(*) FROM branches WHERE repository_id = %s) AS branch_count,
        (SELECT COUNT(*) FROM files WHERE branch_id IN (
         SELECT id FROM branches WHERE repository_id = %s)) AS file_count""", params)
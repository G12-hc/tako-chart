from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# PostgreSQL connection function with a context manager
def get_db_connection():
    conn = psycopg2.connect(
        dbname="HackCamp",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
    return conn

@app.route('/commits', methods=['GET'])
def fetch_commits():
    author = request.args.get('author')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    commits = get_commits(author, start_date, end_date)
    return jsonify(commits)

@app.route('/files/large', methods=['GET'])
def large_files():
    threshold = int(request.args.get('threshold', 1000))
    files = get_large_files(threshold)
    return jsonify(files)

@app.route('/repositories/<repo_id>/stats', methods=['GET'])
def repo_stats(repo_id):
    stats = get_repository_stats(repo_id)
    return jsonify(stats)

def get_commits(author=None, start_date=None, end_date=None):
    query = "SELECT * FROM commits WHERE TRUE"
    params = []
    if author:
        query += " AND author = %s"
        params.append(author)
    if start_date and end_date:
        query += " AND date BETWEEN %s AND %s"
        params.extend([start_date, end_date])

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(query, tuple(params))
    commits = cursor.fetchall()
    cursor.close()
    conn.close()
    return commits

def get_large_files(threshold=1000):
    query = "SELECT * FROM files WHERE line_count > %s"
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(query, (threshold,))
    files = cursor.fetchall()
    cursor.close()
    conn.close()
    return files

def get_repository_stats(repo_id):
    query = """
    SELECT
        (SELECT COUNT(*) FROM commits WHERE repository_id = %s) AS commit_count,
        (SELECT COUNT(*) FROM branches WHERE repository_id = %s) AS branch_count,
        (SELECT COUNT(*) FROM files WHERE branch_id IN (SELECT id FROM branches WHERE repository_id = %s)) AS file_count
    """
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(query, (repo_id, repo_id, repo_id))
    stats = cursor.fetchone()
    cursor.close()
    conn.close()
    return stats

if __name__ == '__main__':
    app.run(debug=True)

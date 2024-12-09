import os, subprocess, tempfile, json

from app.db.fetch_git_api import fetch_file_content, get_files

async def save_files_locally(owner: str, repo: str, branch: str = "main", file_types: list = None):
    """
    Fetch files from GitHub, filter by file types, and save them locally.
    :param owner: Repository owner.
    :param repo: Repository name.
    :param branch: Branch name.
    :param file_types: List of file extensions to filter (e.g., ['.py', '.js']).
    :return: Path to the temporary directory with saved files.
    """
    file_list = await get_files(owner, repo, branch)
    temp_dir = tempfile.mkdtemp()

    for file in file_list.get("tree", []):
        if file["type"] == "blob":  # Process only files (not directories)
            file_path = file["path"]

            # Check if the file extension matches the allowed types
            # if file_types and not any(file_path.endswith(ext) for ext in file_types):
                # continue  # Skip this file if it doesn't match the filter

            # Fetch file content
            file_content = await fetch_file_content(owner, repo, file_path)

            # Create directory structure
            local_path = os.path.join(temp_dir, file_path)
            os.makedirs(os.path.dirname(local_path), exist_ok=True)

            # Save file content
            with open(local_path, "w", encoding="utf-8") as f:
                f.write(file_content)

    return temp_dir


def run_cloc(directory: str):
    """
    Run cloc on a directory to calculate line counts.
    """
    result = subprocess.run(["cloc", "--json", directory], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"cloc failed: {result.stderr}")
    return result.stdout


async def analyze_repository(owner: str, repo: str, branch: str = "main", file_types: list = None):
    """
    Analyze a repository's line counts using cloc, with filtering for specific file types.
    :param owner: Repository owner.
    :param repo: Repository name.
    :param branch: Branch name.
    :param file_types: List of file extensions to filter (e.g., ['.py', '.js']).
    :return: Dictionary with line count statistics.
    """
    # Save filtered files locally
    temp_dir = await save_files_locally(owner, repo, branch, file_types)

    try:
        # Run cloc
        cloc_output = run_cloc(temp_dir)
        cloc_data = json.loads(cloc_output)

        # Extract data
        total_lines = cloc_data.get("SUM", {}).get("code", 0)
        comment_lines = cloc_data.get("SUM", {}).get("comment", 0)
        blank_lines = cloc_data.get("SUM", {}).get("blank", 0)

        functional_lines = total_lines - comment_lines - blank_lines

        return {
            "total_lines": total_lines,
            "functional_lines": functional_lines,
        }
    finally:
        # Cleanup temporary directory
        if os.path.exists(temp_dir):
            import shutil
            shutil.rmtree(temp_dir)

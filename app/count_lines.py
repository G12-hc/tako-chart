import os
import subprocess
import tempfile
import shutil
import json
import tarfile  # Import tarfile for handling .tar.gz files

from app.db.fetch_git_api import download_zip  # Assuming your method is defined here


def run_cloc(directory: str):
    """
    Run cloc on a directory to calculate line counts.
    :param directory: Directory to analyze.
    :return: JSON output from cloc.
    """
    result = subprocess.run(["cloc", "--json", directory], capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception(f"cloc failed: {result.stderr}")

    return result.stdout


async def analyze_repository(owner: str, repo: str, branch: str = "main"):
    """
    Analyze a repository's line counts using cloc.
    :param owner: Repository owner.
    :param repo: Repository name.
    :param branch: Branch name.
    :return: Dictionary with line count statistics.
    """

    # Create a temporary directory for extraction
    temp_dir = tempfile.mkdtemp()

    # Download the repository content
    zip_content = await download_zip(owner, repo, branch)  # Fetch the .tar.gz file

    # Save the .tar.gz content to a file
    tar_path = os.path.join(temp_dir, f"{repo}.tar.gz")
    with open(tar_path, "wb") as f:
        f.write(zip_content)  # Save the downloaded tar.gz content

    # Define the extraction directory
    extract_dir = os.path.join(temp_dir, f"{repo}_extracted")
    os.makedirs(extract_dir, exist_ok=True)
    if not os.path.exists(extract_dir):
        raise FileNotFoundError(f"The directory {extract_dir} does not exist.")

    # Extract the .tar.gz file using tarfile
    with tarfile.open(tar_path, "r:gz") as tar:
        tar.extractall(path=extract_dir)  # Extract all contents

    try:
        # Run cloc on the extracted repository
        cloc_output = run_cloc(extract_dir)
        cloc_data = json.loads(cloc_output)  # Parse the JSON output from cloc

        # Extract line count statistics
        total_lines = cloc_data.get("SUM", {}).get("code", 0)
        comment_lines = cloc_data.get("SUM", {}).get("comment", 0)
        blank_lines = cloc_data.get("SUM", {}).get("blank", 0)

        # Calculate functional lines (excluding comments and blanks)
        functional_lines = total_lines - comment_lines - blank_lines

        return {
            "total_lines": total_lines,
            "functional_lines": functional_lines,
        }

    except Exception as e:
        print(f"Error analyzing repository {owner}/{repo}: {e}")
        raise

    finally:
        # Clean up the temporary directory
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
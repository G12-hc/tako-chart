import os
import subprocess
import tempfile
import shutil
import json
import tarfile  # Import tarfile for handling .tar.gz files
from pathlib import Path

from app.db.fetch_git_api import download_zip  # Assuming your method is defined here


def run_cloc(directory: str):
    """
    Run cloc on a directory to calculate line counts.
    :param directory: Directory to analyze.
    :return: JSON output from cloc.
    """
    result = subprocess.run(
        ["cloc", "--by-file", "--json", "."],
        capture_output=True,
        text=True,
        cwd=directory,
    )

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

    # Extract the .tar.gz file using tarfile
    files = None
    with tarfile.open(tar_path, "r:gz") as tar:
        tar.extractall(path=temp_dir)  # Extract all contents
        files = {
            # Remove the root tarball directory (not actually part of the repo)
            os.path.join(*(Path(member.name).parts[1:])): {
                "is_directory": member.isdir(),
            }
            for member in tar.getmembers()
            if len(Path(member.name).parts) > 1
        }

    try:
        # Run cloc on the extracted repository
        cloc_output = run_cloc(temp_dir)
        cloc_data = json.loads(cloc_output)  # Parse the JSON output from cloc
        for key, data in cloc_data.items():
            # We want only actual file data per file
            if key == "header" or key == "SUM":
                continue
            # key is filepath, data is the stats for the file
            files.setdefault(
                os.path.join(*(Path(key).parts[1:])), {"is_directory": False}
            ).update(
                {
                    # line_count includes all lines
                    "line_count": data["code"] + data["blank"] + data["comment"],
                    # functional_line_count includes only actual lines of code,
                    # excluding comments and blank lines
                    "functional_line_count": data["code"],
                }
            )

        return files
    except Exception as e:
        print(f"Error analyzing repository {owner}/{repo}: {e}")
        raise

    finally:
        # Clean up the temporary directory
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

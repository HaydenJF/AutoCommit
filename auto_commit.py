import os
import subprocess
import time

CHECK_INTERVAL = 10 * 60  # Check every 10 seconds (adjust as needed)
MIN_CHANGED_LINES = 30  # Minimum lines changed to trigger a commit
COMMIT_MESSAGE = "WIP: Auto-save at {timestamp}"  # Commit message format
ENV_FILE = ".env"  # Path to the shared environment file

def load_repo_path():
    """
    Load the repository path from the .env file.
    """
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, "r") as env_file:
            for line in env_file:
                if line.startswith("WIP_REPO_PATH="):
                    return line.strip().split("=", 1)[1]
    print(f"{ENV_FILE} not found. Exiting.")
    return None

def is_git_repo(path):
    """
    Check if the specified path is a valid Git repository.
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        return result.stdout.strip() == "true"
    except subprocess.CalledProcessError:
        return False

def get_changed_lines(path):
    """
    Get the number of changed lines in the repository.
    """
    try:
        result = subprocess.run(
            ["git", "diff", "--stat"],
            cwd=path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode != 0:
            print(f"Error checking changes: {result.stderr}")
            return 0

        output = result.stdout.strip()
        if output:
            # Example output: "test.txt | 52 ++++++++++++++++++++++++++++++++++++++++++++++++++++\n 1 file changed, 52 insertions(+)"
            lines_changed = sum(
                int(word) for word in output.split() if word.isdigit()
            )
            return lines_changed
        return 0
    except Exception as e:
        print(f"Exception while checking changes: {e}")
        return 0

def commit_changes(path):
    """
    Stage all changes and commit with a timestamped message.
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    commit_message = COMMIT_MESSAGE.format(timestamp=timestamp)
    try:
        subprocess.run(["git", "add", "."], cwd=path, check=True)
        subprocess.run(["git", "commit", "-m", commit_message], cwd=path, check=True)
        print(f"Committed changes: {commit_message}")
    except subprocess.CalledProcessError as e:
        print(f"Error committing changes: {e}")

def main():
    """
    Main function to monitor the repository and commit changes if needed.
    """
    while True:
        repo_path = load_repo_path()
        if not repo_path:
            print("No repository path found. Exiting.")
            break

        if not os.path.exists(repo_path):
            print(f"Path does not exist: {repo_path}")
            time.sleep(CHECK_INTERVAL)
            continue

        if not is_git_repo(repo_path):
            print(f"Path is not a Git repository: {repo_path}")
            time.sleep(CHECK_INTERVAL)
            continue

        print(f"Monitoring repository path: {repo_path}")
        changed_lines = get_changed_lines(repo_path)
        print(f"Changed lines: {changed_lines}")

        if changed_lines >= MIN_CHANGED_LINES:
            print("Threshold met. Committing changes...")
            commit_changes(repo_path)
        else:
            print("No significant changes to commit.")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()

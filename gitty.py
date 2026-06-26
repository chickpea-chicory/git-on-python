import os
import subprocess
import sys


def run_git_command(command, cwd=None):
    """Executes a git command and handles potential errors."""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"\n[!] Error executing: {' '.join(command)}")
        print(f"[!] Details: {e.stderr.strip()}")
        sys.exit(1)


def main():
    # 1. Get file path
    file_path = input("Give the file path of your code: ").strip().strip("'\"")

    if not os.path.exists(file_path):
        print("[!] Error: File does not exist.")
        sys.exit(1)

    # Determine project directory and file name
    repo_dir = os.path.dirname(os.path.abspath(file_path))
    file_name = os.path.basename(file_path)

    # 2. Get GitHub Repo URL and Commit Message
    repo_url = input("Enter the GitHub repo URL: ").strip()
    commit_message = input("Enter your commit message: ").strip()

    if not commit_message:
        commit_message = "Initial commit"

    print(f"\n[*] Initializing operations in: {repo_dir}")

    # 3. Git Operations
    # Initialize repo if it doesn't exist
    if not os.path.exists(os.path.join(repo_dir, ".git")):
        run_git_command(["git", "init"], cwd=repo_dir)

    # Configure or update the remote origin
    try:
        run_git_command(
            ["git", "remote", "add", "origin", repo_url], cwd=repo_dir
        )
    except SystemExit:
        # If origin already exists, update it instead of failing
        run_git_command(
            ["git", "remote", "set-url", "origin", repo_url], cwd=repo_dir
        )

    # Stage the specific file
    run_git_command(["git", "add", file_name], cwd=repo_dir)

    # Commit the changes
    run_git_command(["git", "commit", "-m", commit_message], cwd=repo_dir)

    # Set default branch name to main and push
    run_git_command(["git", "branch", "-M", "main"], cwd=repo_dir)

    print("[*] Pushing code to GitHub...")
    run_git_command(["git", "push", "-u", "origin", "main"], cwd=repo_dir)

    print("\n[+] Code successfully pushed!")


if __name__ == "__main__":
    main()
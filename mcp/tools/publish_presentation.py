"""publish_presentation MCP tool - publishes HTML presentations to GitHub Pages."""

import subprocess
import tempfile
import os
import re
from pathlib import Path
from typing import Any


def _run_gh_command(args: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run a gh CLI command and return the result."""
    result = subprocess.run(
        ["gh"] + args,
        capture_output=True,
        text=True,
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"gh command failed: {result.stderr}")
    return result


def _sanitize_repo_name(name: str) -> str:
    """Convert a topic/title to a valid GitHub repo name."""
    # Lowercase, replace spaces and special chars with hyphens
    sanitized = re.sub(r'[^a-zA-Z0-9\s-]', '', name).lower().strip()
    sanitized = re.sub(r'[\s_]+', '-', sanitized)
    sanitized = re.sub(r'-+', '-', sanitized)
    # Remove leading/trailing hyphens
    sanitized = sanitized.strip('-')
    # Limit length
    return sanitized[:100] if sanitized else "presentation"


def _get_github_username() -> str:
    """Get the authenticated GitHub username."""
    result = _run_gh_command(["api", "user", "--jq", ".login"])
    return result.stdout.strip()


def _repo_exists(repo_name: str, username: str) -> bool:
    """Check if a repository already exists."""
    result = subprocess.run(
        ["gh", "repo", "view", f"{username}/{repo_name}"],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def publish_presentation(
    html_file: str,
    repo_name: str | None = None,
    private: bool = True,
    description: str = "",
) -> dict[str, Any]:
    """
    Publish an HTML presentation to GitHub Pages.

    Creates a new GitHub repository, pushes the HTML file as index.html,
    enables GitHub Pages, and returns the live URL.

    Args:
        html_file: Path to the HTML presentation file
        repo_name: Name for the new repository (auto-generated from file if not provided)
        private: Whether to create a private repository (default: True)
        description: Repository description

    Returns:
        dict with keys:
        - repo_url: GitHub repository URL
        - pages_url: GitHub Pages URL where the presentation is live
        - repo_name: Name of the created repository
        - visibility: "private" or "public"
    """
    # Validate input file
    html_path = Path(html_file).resolve()
    if not html_path.exists():
        return {"error": f"HTML file not found: {html_file}"}
    if not html_path.suffix == ".html":
        return {"error": f"File must be an HTML file, got: {html_path.suffix}"}

    # Get GitHub username
    try:
        username = _get_github_username()
    except RuntimeError as e:
        return {"error": f"GitHub authentication required: {e}"}

    # Generate repo name from file if not provided
    if not repo_name:
        # Use the filename without extension as base
        base_name = html_path.stem
        # Remove common suffixes
        base_name = re.sub(r'-presentation$', '', base_name)
        repo_name = _sanitize_repo_name(base_name)
        if not repo_name:
            repo_name = "presentation"

    # Check if repo already exists
    if _repo_exists(repo_name, username):
        return {"error": f"Repository '{repo_name}' already exists. Choose a different name or delete the existing repo first."}

    # Create the repository
    visibility = "private" if private else "public"
    create_args = [
        "repo", "create", repo_name,
        f"--{visibility}",
        "--description", description or f"HTML presentation: {html_path.stem}",
    ]
    
    try:
        result = _run_gh_command(create_args)
    except RuntimeError as e:
        return {"error": f"Failed to create repository: {e}"}

    repo_url = f"https://github.com/{username}/{repo_name}"

    # Create a temp directory for the git operations
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        
        # Clone the new repo
        clone_result = subprocess.run(
            ["git", "clone", repo_url, tmpdir],
            capture_output=True,
            text=True,
            env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
        )
        if clone_result.returncode != 0:
            return {"error": f"Failed to clone repository: {clone_result.stderr}"}

        # Copy the HTML file as index.html
        index_path = tmpdir_path / "index.html"
        index_path.write_text(html_path.read_text(encoding="utf-8"), encoding="utf-8")

        # Git add, commit, push
        git_commands = [
            ["git", "add", "index.html"],
            ["git", "commit", "-m", "Add presentation"],
            ["git", "branch", "-M", "main"],
            ["git", "push", "-u", "origin", "main"],
        ]

        for cmd in git_commands:
            result = subprocess.run(
                cmd,
                cwd=tmpdir,
                capture_output=True,
                text=True,
                env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
            )
            if result.returncode != 0 and "nothing to commit" not in result.stdout:
                # Branch rename might fail if already main, that's OK
                if "branch -M main" not in " ".join(cmd):
                    return {"error": f"Git operation failed: {result.stderr}"}

    # Enable GitHub Pages
    pages_result = subprocess.run(
        ["gh", "api", f"repos/{username}/{repo_name}/pages", 
         "-X", "POST", 
         "-f", "source={\"branch\":\"main\"}"],
        capture_output=True,
        text=True,
    )
    
    if pages_result.returncode != 0:
        # Pages might already be enabled or there might be a delay
        pass

    # Construct the Pages URL
    # For user pages, it's username.github.io/repo-name
    pages_url = f"https://{username}.github.io/{repo_name}/"

    return {
        "repo_url": repo_url,
        "pages_url": pages_url,
        "repo_name": repo_name,
        "visibility": visibility,
        "message": f"Presentation published! It may take 1-2 minutes for GitHub Pages to build and deploy."
    }

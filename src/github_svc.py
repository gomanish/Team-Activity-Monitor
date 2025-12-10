import os
import requests
from dotenv import load_dotenv

load_dotenv()


class GitHubClient:
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github.v3+json",
        }
        if not self.token:
            print("GITHUB_TOKEN not found in .env")

    def get_recent_activity(self, username):
        if not self.token:
            return {}

        self.github_base_url = os.getenv("GITHUB_BASE_URL", "https://api.github.com")

        try:
            repos_url = f"{self.github_base_url}/user/repos"
            params = {
                "type": "all",
                "sort": "pushed",
                "direction": "desc",
                "per_page": 10,
            }
            response = requests.get(repos_url, headers=self.headers, params=params)

            if response.status_code != 200:
                print(f"GitHub API Error (Repos): {response.text}")
                return {}

            repos = response.json()
            commits = []

            for repo in repos:
                repo_name = repo.get("full_name")

                commits_url = f"{self.github_base_url}/repos/{repo_name}/commits"
                commit_params = {"author": username, "per_page": 3}

                c_response = requests.get(
                    commits_url, headers=self.headers, params=commit_params
                )

                if c_response.status_code == 200:
                    repo_commits = c_response.json()
                    for commit in repo_commits:
                        commit_data = commit.get("commit", {})
                        commits.append(
                            {
                                "repo": repo_name,
                                "message": commit_data.get("message"),
                                "date": commit_data.get("author", {}).get("date"),
                                "url": commit.get("html_url"),
                            }
                        )

            commits.sort(key=lambda x: x["date"], reverse=True)

            return {
                "commits": commits[:10],
                "scan_info": f"Scanned top {len(repos)} active repositories.",
            }

        except Exception as e:
            print(f"Error fetching GitHub activity: {e}")
            return {}

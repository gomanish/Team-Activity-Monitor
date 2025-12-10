import os
from jira import JIRA
from dotenv import load_dotenv

load_dotenv()


class JiraClient:
    def __init__(self):
        self.server = os.getenv("JIRA_URL")
        self.email = os.getenv("JIRA_EMAIL")
        self.token = os.getenv("JIRA_API_TOKEN")

        if not all([self.server, self.email, self.token]):
            print("Warning: JIRA credentials not fully found in .env")
            self.client = None
        else:
            try:
                self.client = JIRA(
                    server=self.server, basic_auth=(self.email, self.token)
                )
            except Exception as e:
                print(f"Failed to connect to JIRA: {e}")
                self.client = None

    def get_assigned_issues(self, user_email):
        if not self.client:
            return []

        try:
            jql = f'assignee = "{user_email}" AND statusCategory != Done ORDER BY updated DESC'
            issues = self.client.search_issues(jql, maxResults=5)

            results = []
            for issue in issues:
                results.append(
                    {
                        "key": issue.key,
                        "summary": issue.fields.summary,
                        "status": issue.fields.status.name,
                        "updated": issue.fields.updated,
                    }
                )
            return results
        except Exception as e:
            print(f"Error fetching JIRA issues: {e}")
            return []

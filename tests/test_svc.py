from unittest.mock import MagicMock, patch
import os
from src.github_svc import GitHubClient
from src.jira_svc import JiraClient


@patch.dict(
    os.environ,
    {"GITHUB_TOKEN": "test_token", "GITHUB_BASE_URL": "https://api.github.com"},
    clear=True,
)
def test_github_init_success():
    client = GitHubClient()
    assert client.token == "test_token"
    assert client.headers["Authorization"] == "Bearer test_token"


@patch.dict(os.environ, {}, clear=True)
def test_github_init_missing_token():
    client = GitHubClient()
    assert client.token is None


@patch("src.github_svc.requests.get")
@patch.dict(os.environ, {"GITHUB_TOKEN": "test_token"}, clear=True)
def test_github_get_recent_activity_api_error(mock_get):
    client = GitHubClient()

    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.text = "Not Found"
    mock_get.return_value = mock_response

    activity = client.get_recent_activity("testuser")
    assert activity == {}


@patch.dict(os.environ, {}, clear=True)
def test_github_get_recent_activity_no_token():
    client = GitHubClient()
    activity = client.get_recent_activity("testuser")
    assert activity == {}


@patch.dict(
    os.environ,
    {
        "JIRA_URL": "http://jira.com",
        "JIRA_EMAIL": "manish@manish.com",
        "JIRA_API_TOKEN": "test_token",
    },
    clear=True,
)
@patch("src.jira_svc.JIRA")
def test_jira_init_success(mock_jira_cls):
    client = JiraClient()
    assert client.client is not None
    mock_jira_cls.assert_called_once()


@patch.dict(os.environ, {}, clear=True)
def test_jira_init_missing_creds():
    client = JiraClient()
    assert client.client is None


@patch.dict(
    os.environ,
    {
        "JIRA_URL": "http://jira.com",
        "JIRA_EMAIL": "manish@manish.com",
        "JIRA_API_TOKEN": "test_token",
    },
    clear=True,
)
@patch("src.jira_svc.JIRA")
def test_jira_get_assigned_issues_success(mock_jira_cls):
    mock_jira_instance = MagicMock()
    mock_jira_cls.return_value = mock_jira_instance

    mock_issue = MagicMock()
    mock_issue.key = "PROJ-1"
    mock_issue.fields.summary = "Fix bug"
    mock_issue.fields.status.name = "In Progress"
    mock_issue.fields.updated = "2025-11-10T10:00:00Z"

    mock_jira_instance.search_issues.return_value = [mock_issue]

    client = JiraClient()
    issues = client.get_assigned_issues("manish@manish.com")

    assert len(issues) == 1
    assert issues[0]["key"] == "PROJ-1"
    assert issues[0]["summary"] == "Fix bug"


@patch.dict(os.environ, {}, clear=True)
def test_jira_get_assigned_issues_no_client():
    client = JiraClient()
    issues = client.get_assigned_issues("manish@manish.com")
    assert issues == []

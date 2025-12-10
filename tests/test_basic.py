from unittest.mock import MagicMock, patch
from src.ai_svc import AIService
from src.jira_svc import JiraClient
from src.github_svc import GitHubClient


def test_clients_instantiation():
    jira = JiraClient()
    github = GitHubClient()
    ai = AIService()
    assert jira is not None
    assert github is not None
    assert ai is not None


@patch("src.ai_svc.genai.Client")
def test_ai_extraction(mock_genai):
    params = MagicMock()
    params.text = "Manish"

    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = params
    mock_genai.return_value = mock_client

    ai = AIService()
    ai.client = mock_client

    name = ai.extract_member_name("What is Manish working on?")
    assert name == "Manish"


def test_user_mapping():
    from src.user_mapping import get_user_details, USER_DIRECTORY

    USER_DIRECTORY["TestUser"] = {
        "jira_email": "test@example.com",
        "github_username": "testuser",
    }

    email, github = get_user_details("TestUser")
    assert email == "test@example.com"
    assert github == "testuser"

    email, github = get_user_details("UnknownUser")
    assert email is None
    assert github is None

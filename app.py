from flask import Flask, render_template, request, jsonify

from src.jira_svc import JiraClient
from src.github_svc import GitHubClient
from src.ai_svc import AIService
from src.user_mapping import get_user_details

app = Flask(__name__)

jira_client = JiraClient()
github_client = GitHubClient()
ai_service = AIService()


@app.route("/")
def home():
    return render_template("app.html")


@app.route("/api/query", methods=["POST"])
def process_query():
    data = request.json
    user_query = data.get("query")

    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    member_name = ai_service.extract_member_name(user_query)

    if not member_name:
        return (
            jsonify(
                {
                    "response": "I couldn't identify a team member name in your question. Please try asking about specific person, e.g., 'What is John working on?'"
                }
            ),
            200,
        )
    member_name = member_name.lower()
    jira_email, github_username = get_user_details(member_name)

    if not jira_email or not github_username:
        return jsonify({"response": "Member not found"}), 200

    jira_data = jira_client.get_assigned_issues(jira_email)
    github_data = github_client.get_recent_activity(github_username)

    answer = ai_service.generate_response(
        user_query, jira_data, github_data, member_name
    )

    return jsonify(
        {
            "member": member_name,
            "jira_data": jira_data,
            "github_data": github_data,
            "response": answer,
        }
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)

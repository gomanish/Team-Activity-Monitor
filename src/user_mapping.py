USER_DIRECTORY = {
    "manish": {"jira_email": "manishtu98@gmail.com", "github_username": "gomanish"},
    "jhon": {"jira_email": "krmanish2101@gmail.com", "github_username": "rajaniket"},
}


def get_user_details(name):
    user = USER_DIRECTORY.get(name)
    if user:
        return user.get("jira_email"), user.get("github_username")
    return None, None

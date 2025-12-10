# Team Activity Monitor

A simple AI-powered chatbot that integrates with JIRA and GitHub to provide summaries of team member activities.

## Features

- **JIRA Integration**: Fetches assigned issues and their status for a specific user.
- **GitHub Integration**: Fetches recent commits and pull requests.
- **AI-Powered Summaries**: Uses Google Gemini to synthesize data into natural language responses.

## Prerequisites

- Python 3.12+
- `uv` package manager (optional but recommended)
- JIRA Account & API Token
- GitHub Personal Access Token
- Google Gemini API Key

## Setup

1. **Clone the repository** (if not already local).

2. **Configure Environment Variables**:
   Create a `.env` file in the root directory and add the following:
   ```env
   GEMINI_API_KEY="gemini-api-key"
   MODEL_NAME="model-name"
   JIRA_URL="https://your-domain.atlassian.net"
   JIRA_EMAIL="your-email@example.com"
   JIRA_API_TOKEN="your-jira-api-token"
   GITHUB_TOKEN="your-github-token"
   ```

3. **Install Dependencies**:
   Using `uv`:
   ```bash
   uv sync
   ```

## Usage

1. **Start the Application**:
   ```bash
   uv run python app.py
   ```

2. **Open the Interface**:
   Go to [http://localhost:5000](http://localhost:5000) in your browser.

3. **Ask a Question**:
   - "What is Manish working on?"

## Project Structure

- `src/`: Backend logic for JIRA, GitHub, and AI services.
- `static/`: CSS and JavaScript files.
- `templates/`: HTML templates.
- `app.py`: Main Flask application entry point.

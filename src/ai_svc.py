import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash-lite")


class AIService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            print("Warning: GEMINI_API_KEY not found in .env")
            self.client = None
        else:
            self.client = genai.Client(api_key=self.api_key)

    def generate_response(self, user_query, jira_data, github_data, member_name):
        if not self.client:
            return (
                "AI Service unavailable. Here is the raw data: "
                + str(jira_data)
                + str(github_data)
            )

        prompt = f"""
        You are a helpful team assistant. A user asked about {member_name}'s activity.
        User Query: "{user_query}"
        
        Here is the data retrieved from JIRA:
        {jira_data}
        
        Here is the data retrieved from GitHub:
        {github_data}
        
        Please provide a concise, natural language summary of what {member_name} is working on based on this data.
        If there is no activity in one source, mention that briefly or focus on the source that has data.
        Do not make up facts. If no data exists at all, say so politely.
        Format the response nicely with bullet points if there are multiple items.
        """

        try:
            response = self.client.models.generate_content(
                model=MODEL_NAME, contents=prompt
            )
            return response.text
        except Exception as e:
            print(f"Error generating AI response: {e}")
            return "Sorry, I encountered an error generating the summary."

    def extract_member_name(self, query):
        if not self.client:
            return None

        prompt = f"""
        Extract the name of the team member from this query: "{query}"
        Return ONLY the name. If no name is found, return "None".
        Examples:
        "What is John working on?" -> John
        "Show me Sarah's tickets" -> Sarah
        """

        try:
            response = self.client.models.generate_content(
                model=MODEL_NAME, contents=prompt
            )
            name = response.text.strip()
            if "None" in name:
                return None
            return name
        except Exception as e:
            print(f"Error extracting name: {e}")
            return None

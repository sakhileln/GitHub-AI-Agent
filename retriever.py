import os
import requests
from dotenv import load_dotenv
from langchain_core.documents import Document

load_dotenv()

github_token = os.getenv("GITHUB_TOKEN")

def fetch_github(owner, repo, endpoint):
    url = f"https://api.github.com/repos/{owner}/{repo}/{endpoint}"
    headers = {
        "Authorization": f"Bearer {github_token}"
    }
    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code == 200:
        data = response.json()
    else:
        print("Failed with status code: ", response.status_code)
        return []

    print(data)
    return data
    


if __name__ == "__main__":
    owner = "sakhileln"
    repo = "Space-Nomad"
    endpoint = "issues"
    fetch_github(owner, repo, endpoint)
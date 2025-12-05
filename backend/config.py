import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Inner
    ACCESS_TOKEN_COOKIE = "astra.access_token"
    BASE_CLIENT_URL= "http://localhost:3000"
    BASE_API_URL = "http://localhost:4000"
    
    # Key for JWT tokens
    SECRET_KEY = os.getenv("SECRET_KEY")
    
    # Google OAuth
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI= f"{BASE_API_URL}/auth/google/callback"
    
    # Google Docs
    GDOCS_CLIENT_ID = os.getenv("GDOCS_CLIENT_ID")
    GDOCS_CLIENT_SECRET = os.getenv("GDOCS_CLIENT_SECRET")
    GDOCS_REDIRECT_URI= f"{BASE_API_URL}/auth/gdocs/callback"
    GDOCS_TOKEN_URL = "https://oauth2.googleapis.com/token"
    GDOCS_OAUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    GDOCS_SCOPE = (
        "https://www.googleapis.com/auth/documents.readonly "
        "https://www.googleapis.com/auth/drive.metadata.readonly"
    )

    # Goofle Drive for Google Docs
    GDRIVE_BASE_API = "https://www.googleapis.com/drive/v3"
    
    GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
    GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
    GITHUB_REDIRECT_URI = os.getenv("GITHUB_REDIRECT_URI")
    GITHUB_REDIRECT_URI= f"{BASE_API_URL}/auth/github/callback"
    GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
    GITHUB_OAUTH_URL = "https://github.com/login/oauth/authorize"
    GITHUB_BASE_API = "https://api.github.com"
    GITHUB_REPO_URL = f"{GITHUB_BASE_API}/repos"
    
    # GitLab
    GITLAB_CLIENT_ID = os.getenv("GITLAB_CLIENT_ID")
    GITLAB_CLIENT_SECRET = os.getenv("GITLAB_CLIENT_SECRET")
    GITLAB_BASE_URL = os.getenv("GITLAB_BASE_URL")
    GITLAB_BASE_API = os.getenv("GITLAB_BASE_API")
    GITLAB_REDIRECT_URI = f"{BASE_API_URL}/auth/gitlab/callback"
    GITLAB_OAUTH_URL = f"{GITLAB_BASE_URL}/oauth/authorize"
    GITLAB_TOKEN_URL = f"{GITLAB_BASE_URL}/oauth/token"
    
    # TODO Trello
    # TRELLO_REDIRECT_URL= f"{BASE_API_URL}/trello/callback"
    
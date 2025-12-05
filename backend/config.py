import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ACCESS_TOKEN_COOKIE = "astra.access_token"
    BASE_CLIENT_URL= "http://localhost:3000"
    BASE_API_URL = "http://localhost:4000"
    
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI= f"{BASE_API_URL}/auth/google/callback"
    
    GDOCS_CLIENT_ID = os.getenv("GDOCS_CLIENT_ID")
    GDOCS_CLIENT_SECRET = os.getenv("GDOCS_CLIENT_SECRET")
    GDOCS_REDIRECT_URI= f"{BASE_API_URL}/auth/gdocs/callback"
    GDOCS_TOKEN_URL = "https://github.com/login/oauth/access_token"
    GDOCS_OAUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    GDOCS_SCOPE = (
        "https://www.googleapis.com/auth/documents.readonly "
        "https://www.googleapis.com/auth/drive.metadata.readonly"
    )
    
    GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
    GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
    GITHUB_REDIRECT_URI = os.getenv("GITHUB_REDIRECT_URI")
    GITHUB_REDIRECT_URI= f"{BASE_API_URL}/auth/github/callback"
    GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
    GITHUB_OAUTH_URL = "https://github.com/login/oauth/authorize"
    
    GITLAB_CLIENT_ID = os.getenv("GITLAB_CLIENT_ID")
    GITLAB_CLIENT_SECRET = os.getenv("GITLAB_CLIENT_SECRET")
    GITLAB_BASE_URL = os.getenv("GITLAB_BASE_URL")
    GITLAB_REDIRECT_URI = f"{BASE_API_URL}/auth/gitlab/callback"
    GITLAB_OAUTH_URL = f"{GITLAB_BASE_URL}/oauth/authorize"
    GITLAB_TOKEN_URL = f"{GITLAB_BASE_URL}/oauth/token"
    
    TRELLO_REDIRECT_URL= f"{BASE_API_URL}/trello/callback"
    
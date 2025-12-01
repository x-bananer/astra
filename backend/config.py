import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
    GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
    GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
    GITHUB_REDIRECT_URI = os.getenv("GITHUB_REDIRECT_URI")
    GITLAB_CLIENT_ID = os.getenv("GITLAB_CLIENT_ID")
    GITLAB_CLIENT_SECRET = os.getenv("GITLAB_CLIENT_SECRET")
    GITLAB_BASE_URL = os.getenv("GITLAB_BASE_URL")
    GITLAB_REDIRECT_URI = os.getenv("GITLAB_REDIRECT_URI")
    
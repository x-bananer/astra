## ASTRA Backend

## The project uses:
- Python 3.11 (recommended)
- Flask
- SQLModel
- Google OAuth
- GitHub / GitLab / Google Docs integrations

## How to run the project
1.	Make sure you are in the backend directory:
    `cd backend`

2.	Create and activate a virtual environment:
    `python3 -m venv venv`

    MacOS: `source venv/bin/activate`

    Windows: `venv\Scripts\activate`

3.	Install required dependencies:

    `pip install -r requirements.txt`

4.	Configure environment variables

    You must register your own app integrations and obtain API keys for:
    - Google OAuth
    - GitHub API
    - GitLab API
    - Google Docs API
    - LLM provider

    All keys must be placed in a .env file in the backend directory. There is a .env_example file that lists all required variables. Copy it and fill in your values:

    `cp .env_example .env`

    If the keys are missing or incorrect, the backend will not function.

5.	Start the backend:

    `python app.py`
    or
    `flask --app app run --debug --port 4000`

    The backend runs on: http://localhost:4000. Frontend communicates with the backend through this URL.
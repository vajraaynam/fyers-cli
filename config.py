import os
from pathlib import Path
from dotenv import load_dotenv

def load_config():
    """Loads configuration from the .env file."""
    env_path = Path(".env")
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
    else:
        # Try finding it in the user's home directory as a fallback for global installation
        global_env = Path.home() / ".fyers-cli-env"
        if global_env.exists():
            load_dotenv(dotenv_path=global_env)

def get_app_id() -> str:
    return os.getenv("FYERS_APP_ID", "")

def get_secret_key() -> str:
    return os.getenv("FYERS_SECRET_KEY", "")

def get_redirect_url() -> str:
    return os.getenv("FYERS_REDIRECT_URL", "")

def get_pin() -> str:
    return os.getenv("FYERS_PIN", "")

def get_client_id() -> str:
    # Client ID for Fyers model usually contains the App ID without suffix if any, or it's exactly the APP ID
    return get_app_id()

def get_token_file_path() -> Path:
    return Path.home() / ".fyers_access_token"

def save_access_token(token: str):
    with open(get_token_file_path(), "w") as f:
        f.write(token)

def get_access_token() -> str:
    token_file = get_token_file_path()
    if token_file.exists():
        with open(token_file, "r") as f:
            return f.read().strip()
    return ""

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    MONGODB_URI: str = os.getenv("MONGODB_URI")
    LLM_API_URL: str = os.getenv("LLM_API_URL")
    TELA_URL: str = os.getenv("TELA_URL")

settings = Settings()
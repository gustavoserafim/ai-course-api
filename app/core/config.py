import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    MONGODB_URI: str = os.getenv("MONGODB_URI")
    LLM_API_URL: str = os.getenv("LLM_API_URL")

settings = Settings()
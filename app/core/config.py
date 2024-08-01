import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    MONGODB_URI: str = os.getenv("MONGODB_URI")
    TELA_MOTOR_A_URL: str = os.getenv("TELA_MOTOR_A_URL")
    TELA_MOTOR_B_URL: str = os.getenv("TELA_MOTOR_B_URL")

settings = Settings()
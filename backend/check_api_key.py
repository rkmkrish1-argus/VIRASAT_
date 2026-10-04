import os
from pathlib import Path

from dotenv import load_dotenv


env_file = Path(__file__).with_name("br.env")
load_dotenv(env_file, override=False)
print("API key loaded:", bool(os.getenv("ELEVENLABS_API_KEY")))

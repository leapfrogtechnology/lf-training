import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv('JWT_SECRET')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')
JWT_ACCESS_TOKEN_LIFE = os.getenv('JWT_ACCESS_TOKEN_LIFE')
JWT_REFRESH_TOKEN_LIFE = os.getenv('JWT_REFRESH_TOKEN_LIFE')
COOKIE_LIFE = float(os.getenv('COOKIE_LIFE'))
SESSION_SECRET = os.getenv('SESSION_SECRET')

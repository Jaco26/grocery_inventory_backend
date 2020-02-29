from app.config import BaseConfig
from app.main import create_app

app = create_app(BaseConfig)

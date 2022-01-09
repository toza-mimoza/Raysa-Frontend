from flask_caching import Cache
from app.settings import cache_config

cache = Cache(config=cache_config)
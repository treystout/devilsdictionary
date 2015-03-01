import os

LOG_FORMAT = '%(asctime)s %(levelname)-7s [%(name)s] %(message)s'
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
SECRET_KEY = os.getenv("SECRET_KEY", "development")
TEST_MODE = bool(int(os.getenv("TEST_MODE", 1)))
DEBUG = bool(int(os.getenv("DEBUG", 1)))

del os

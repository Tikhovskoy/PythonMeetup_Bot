import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = os.path.join(os.path.dirname(__file__), '../logs')
LOG_FILE = os.path.join(LOG_DIR, 'bot.log')

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

handler = RotatingFileHandler(LOG_FILE, maxBytes=500_000, backupCount=5, encoding="utf-8")
handler.setFormatter(formatter)

logger = logging.getLogger("bot_logger")
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.propagate = False

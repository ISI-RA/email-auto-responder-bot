"""
Email Auto-Responder Bot - Configuration
Central configuration for all bot settings
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Email Configuration
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
IMAP_SERVER = os.getenv('IMAP_SERVER', 'imap.gmail.com')
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
IMAP_PORT = int(os.getenv('IMAP_PORT', 993))
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))

# Bot Settings
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', 60))  # seconds
MAX_EMAILS_PER_CHECK = int(os.getenv('MAX_EMAILS_PER_CHECK', 10))
ENABLE_RESPONSES = os.getenv('ENABLE_RESPONSES', 'true').lower() == 'true'
WORKING_HOURS_START = os.getenv('WORKING_HOURS_START', '09:00')
WORKING_HOURS_END = os.getenv('WORKING_HOURS_END', '18:00')
WORKING_HOURS_ENABLED = os.getenv('WORKING_HOURS_ENABLED', 'false').lower() == 'true'

# Flask Configuration
FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Database
DATABASE_PATH = os.getenv('DATABASE_PATH', 'bot_database.db')

# Logging
LOG_FILE = os.getenv('LOG_FILE', 'logs/bot.log')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Rules File
RULES_FILE = os.getenv('RULES_FILE', 'rules.json')

# Validation
def validate_config():
    """Validate that all required configuration is present"""
    required = ['EMAIL_ADDRESS', 'EMAIL_PASSWORD']
    missing = [key for key in required if not globals().get(key)]
    if missing:
        raise ValueError(f"Missing required configuration: {', '.join(missing)}. Check .env file.")
    return True

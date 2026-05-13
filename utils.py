#!/usr/bin/env python3
"""
Utility Functions - Helper functions for the bot
"""

import re
import logging
from datetime import datetime, time
from config import WORKING_HOURS_START, WORKING_HOURS_END, WORKING_HOURS_ENABLED

logger = logging.getLogger(__name__)

def is_within_working_hours():
    """Check if current time is within working hours"""
    if not WORKING_HOURS_ENABLED:
        return True
    
    try:
        current_time = datetime.now().time()
        start = datetime.strptime(WORKING_HOURS_START, '%H:%M').time()
        end = datetime.strptime(WORKING_HOURS_END, '%H:%M').time()
        
        return start <= current_time <= end
    except Exception as e:
        logger.error(f"Error checking working hours: {e}")
        return True

def extract_email_from_header(email_header):
    """Extract email address from email header"""
    try:
        match = re.search(r'<([^>]+)>', email_header)
        if match:
            return match.group(1)
        return email_header.strip()
    except:
        return email_header

def normalize_text(text):
    """Normalize text for comparison"""
    return text.lower().strip()

def contains_keywords(text, keywords):
    """Check if text contains any of the keywords"""
    text_lower = normalize_text(text)
    for keyword in keywords:
        if normalize_text(keyword) in text_lower:
            return True
    return False

def contains_all_keywords(text, keywords):
    """Check if text contains all keywords"""
    text_lower = normalize_text(text)
    return all(normalize_text(keyword) in text_lower for keyword in keywords)

def get_current_timestamp():
    """Get current timestamp in standard format"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def truncate_text(text, length=100):
    """Truncate text to specified length"""
    if len(text) > length:
        return text[:length] + "..."
    return text

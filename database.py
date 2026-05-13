#!/usr/bin/env python3
"""
Database Operations - Manages SQLite database for logging
"""

import sqlite3
import logging
from datetime import datetime
from config import DATABASE_PATH

logger = logging.getLogger(__name__)

class Database:
    """SQLite database manager"""
    
    def __init__(self):
        self.db_path = DATABASE_PATH
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Email logs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS email_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    from_email TEXT NOT NULL,
                    subject TEXT NOT NULL,
                    body TEXT,
                    category TEXT,
                    action_taken TEXT,
                    response_sent TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    rule_matched TEXT
                )
            ''')
            
            # Bot statistics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS bot_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date DATE,
                    emails_received INTEGER DEFAULT 0,
                    emails_processed INTEGER DEFAULT 0,
                    auto_replies_sent INTEGER DEFAULT 0,
                    emails_forwarded INTEGER DEFAULT 0,
                    UNIQUE(date)
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
    
    def log_email(self, from_email, subject, body, category, action, response, rule):
        """Log email processing"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO email_logs 
                (from_email, subject, body, category, action_taken, response_sent, rule_matched)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (from_email, subject, body[:200], category, action, response, rule))
            
            conn.commit()
            conn.close()
            logger.info(f"Email logged: {subject[:50]}")
            return True
        except Exception as e:
            logger.error(f"Error logging email: {e}")
            return False
    
    def get_logs(self, limit=50):
        """Retrieve recent logs"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM email_logs 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
            
            logs = cursor.fetchall()
            conn.close()
            return logs
        except Exception as e:
            logger.error(f"Error retrieving logs: {e}")
            return []
    
    def update_daily_stats(self, emails_received=0, emails_processed=0, 
                          replies_sent=0, emails_forwarded=0):
        """Update daily statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            today = datetime.now().date()
            
            cursor.execute('''
                INSERT INTO bot_stats 
                (date, emails_received, emails_processed, auto_replies_sent, emails_forwarded)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(date) DO UPDATE SET
                    emails_received = emails_received + ?,
                    emails_processed = emails_processed + ?,
                    auto_replies_sent = auto_replies_sent + ?,
                    emails_forwarded = emails_forwarded + ?
            ''', (today, emails_received, emails_processed, replies_sent, 
                  emails_forwarded, emails_received, emails_processed, replies_sent, emails_forwarded))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error updating stats: {e}")
            return False

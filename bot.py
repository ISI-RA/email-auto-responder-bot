#!/usr/bin/env python3
"""
Email Auto-Responder Bot - Main Bot Logic
Monitors inbox and automatically responds to emails based on rules
"""

import json
import logging
import time
import schedule
from email_handler import EmailHandler
from database import Database
from utils import (
    is_within_working_hours, extract_email_from_header, 
    contains_keywords, contains_all_keywords, get_current_timestamp
)
from config import CHECK_INTERVAL, MAX_EMAILS_PER_CHECK, ENABLE_RESPONSES, RULES_FILE

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EmailBot:
    """Main bot class for email automation"""
    
    def __init__(self):
        self.email_handler = EmailHandler()
        self.database = Database()
        self.rules = self.load_rules()
        self.running = False
    
    def load_rules(self):
        """Load rules from JSON file"""
        try:
            with open(RULES_FILE, 'r') as f:
                config = json.load(f)
                logger.info(f"Loaded {len(config['rules'])} rules")
                return config['rules']
        except Exception as e:
            logger.error(f"Error loading rules: {e}")
            return []
    
    def match_rule(self, email_data):
        """Match email against rules and return matching rule"""
        subject = email_data['subject'].lower()
        body = email_data['body'].lower()
        combined_text = f"{subject} {body}"
        
        for rule in self.rules:
            if not rule['active']:
                continue
            
            conditions = rule['conditions']
            keywords = conditions.get('keywords', [])
            match_type = conditions.get('match_type', 'any')
            
            # Check keywords
            if match_type == 'any':
                if contains_keywords(combined_text, keywords):
                    return rule
            elif match_type == 'all':
                if contains_all_keywords(combined_text, keywords):
                    return rule
        
        return None
    
    def execute_rule(self, email_data, rule):
        """Execute the action defined in the rule"""
        action = rule['action']
        from_email = extract_email_from_header(email_data['from'])
        
        logger.info(f"Executing rule '{rule['name']}' for {from_email}")
        
        if action == 'reply':
            return self.send_reply(email_data, rule)
        elif action == 'forward':
            return self.forward_email(email_data, rule)
        elif action == 'categorize':
            return self.categorize_email(email_data, rule)
        elif action == 'delete':
            return self.delete_email(email_data)
        else:
            logger.warning(f"Unknown action: {action}")
            return None
    
    def send_reply(self, email_data, rule):
        """Send auto-reply"""
        from_email = extract_email_from_header(email_data['from'])
        
        if not ENABLE_RESPONSES:
            logger.info(f"Responses disabled. Would reply to {from_email}")
            return 'skipped'
        
        success = self.email_handler.send_reply(
            from_email,
            email_data['subject'],
            rule.get('response', 'Thank you for your email.')
        )
        
        if success:
            self.database.log_email(
                from_email,
                email_data['subject'],
                email_data['body'],
                rule.get('category', 'general'),
                'replied',
                rule.get('response'),
                rule['name']
            )
            logger.info(f"Reply sent to {from_email}")
            return 'replied'
        return 'failed'
    
    def forward_email(self, email_data, rule):
        """Forward email to specified address"""
        from_email = extract_email_from_header(email_data['from'])
        forward_to = rule.get('forward_to')
        
        if not forward_to:
            logger.warning(f"No forward address specified for rule '{rule['name']}'")
            return None
        
        success = self.email_handler.forward_email(
            email_data,
            forward_to,
            f"Auto-forwarded by rule: {rule['name']}"
        )
        
        if success:
            self.database.log_email(
                from_email,
                email_data['subject'],
                email_data['body'],
                rule.get('category', 'general'),
                'forwarded',
                f"Forwarded to {forward_to}",
                rule['name']
            )
            logger.info(f"Email from {from_email} forwarded to {forward_to}")
            return 'forwarded'
        return 'failed'
    
    def categorize_email(self, email_data, rule):
        """Log email categorization"""
        from_email = extract_email_from_header(email_data['from'])
        
        self.database.log_email(
            from_email,
            email_data['subject'],
            email_data['body'],
            rule.get('category', 'general'),
            'categorized',
            rule.get('response'),
            rule['name']
        )
        
        logger.info(f"Email from {from_email} categorized as {rule.get('category')}")
        return 'categorized'
    
    def delete_email(self, email_data):
        """Delete email (not implemented for safety)"""
        logger.warning("Delete action not implemented for safety reasons")
        return 'skipped'
    
    def process_emails(self):
        """Main email processing loop"""
        logger.info("\n" + "="*50)
        logger.info(f"Processing emails at {get_current_timestamp()}")
        logger.info("="*50)
        
        try:
            # Check if within working hours
            if not is_within_working_hours():
                logger.info("Outside working hours. Skipping processing.")
                return
            
            # Get unread emails
            emails = self.email_handler.get_unread_emails(limit=MAX_EMAILS_PER_CHECK)
            logger.info(f"Found {len(emails)} unread emails")
            
            if not emails:
                logger.info("No unread emails to process")
                return
            
            # Process each email
            processed = 0
            for email_data in emails:
                try:
                    logger.info(f"\nProcessing: {email_data['subject'][:50]}")
                    
                    # Match against rules
                    matching_rule = self.match_rule(email_data)
                    
                    if matching_rule:
                        logger.info(f"Matched rule: {matching_rule['name']}")
                        result = self.execute_rule(email_data, matching_rule)
                        logger.info(f"Action result: {result}")
                    else:
                        logger.info("No matching rule found")
                    
                    processed += 1
                
                except Exception as e:
                    logger.error(f"Error processing email: {e}")
            
            logger.info(f"\nProcessed {processed} emails successfully")
        
        except Exception as e:
            logger.error(f"Error in process_emails: {e}")
    
    def start(self):
        """Start the bot"""
        self.running = True
        logger.info("\n" + "*"*50)
        logger.info("📧 EMAIL AUTO-RESPONDER BOT STARTED")
        logger.info("*"*50)
        logger.info(f"Check interval: {CHECK_INTERVAL} seconds")
        logger.info(f"Responses enabled: {ENABLE_RESPONSES}")
        logger.info(f"Rules loaded: {len(self.rules)}")
        logger.info("*"*50 + "\n")
        
        try:
            while self.running:
                self.process_emails()
                logger.info(f"Next check in {CHECK_INTERVAL} seconds...\n")
                time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            self.stop()
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            self.stop()
    
    def stop(self):
        """Stop the bot"""
        self.running = False
        logger.info("\n" + "*"*50)
        logger.info("📧 EMAIL BOT STOPPED")
        logger.info("*"*50 + "\n")

if __name__ == '__main__':
    bot = EmailBot()
    bot.start()

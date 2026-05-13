#!/usr/bin/env python3
"""
Email Handler - Manages IMAP and SMTP operations
Handles email retrieval, parsing, and sending
"""

import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import decode_header
import logging
from config import EMAIL_ADDRESS, EMAIL_PASSWORD, IMAP_SERVER, SMTP_SERVER, IMAP_PORT, SMTP_PORT

logger = logging.getLogger(__name__)

class EmailHandler:
    """Handles all email operations (IMAP/SMTP)"""
    
    def __init__(self):
        self.email = EMAIL_ADDRESS
        self.password = EMAIL_PASSWORD
        self.imap_server = IMAP_SERVER
        self.smtp_server = SMTP_SERVER
        self.imap_connection = None
        self.smtp_connection = None
    
    def connect_imap(self):
        """Connect to IMAP server and login"""
        try:
            self.imap_connection = imaplib.IMAP4_SSL(self.imap_server, IMAP_PORT)
            self.imap_connection.login(self.email, self.password)
            logger.info(f"Connected to IMAP server: {self.imap_server}")
            return True
        except imaplib.IMAP4.error as e:
            logger.error(f"IMAP connection failed: {e}")
            return False
    
    def disconnect_imap(self):
        """Disconnect from IMAP server"""
        try:
            if self.imap_connection:
                self.imap_connection.close()
                self.imap_connection.logout()
                logger.info("Disconnected from IMAP server")
        except Exception as e:
            logger.error(f"Error disconnecting IMAP: {e}")
    
    def get_unread_emails(self, mailbox='INBOX', limit=10):
        """Get unread emails from inbox"""
        try:
            self.connect_imap()
            self.imap_connection.select(mailbox)
            
            # Search for unread emails
            status, message_ids = self.imap_connection.search(None, 'UNSEEN')
            
            if status != 'OK':
                logger.error("Failed to search for unread emails")
                return []
            
            email_ids = message_ids[0].split()[-limit:]
            emails = []
            
            for email_id in email_ids:
                status, msg_data = self.imap_connection.fetch(email_id, '(RFC822)')
                if status == 'OK':
                    msg = email.message_from_bytes(msg_data[0][1])
                    emails.append({
                        'id': email_id,
                        'from': msg.get('From'),
                        'subject': self._decode_subject(msg.get('Subject')),
                        'body': self._get_email_body(msg),
                        'date': msg.get('Date'),
                        'raw': msg
                    })
            
            logger.info(f"Retrieved {len(emails)} unread emails")
            return emails
        
        except Exception as e:
            logger.error(f"Error fetching emails: {e}")
            return []
        finally:
            self.disconnect_imap()
    
    def _decode_subject(self, subject):
        """Decode email subject"""
        if not subject:
            return "(No Subject)"
        try:
            decoded_parts = decode_header(subject)
            decoded_subject = ""
            for part, charset in decoded_parts:
                if isinstance(part, bytes):
                    decoded_subject += part.decode(charset or 'utf-8', errors='ignore')
                else:
                    decoded_subject += part
            return decoded_subject
        except:
            return subject
    
    def _get_email_body(self, msg):
        """Extract email body (text or html)"""
        body = ""
        try:
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                        break
                    elif part.get_content_type() == "text/html":
                        body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
            else:
                body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
        except Exception as e:
            logger.warning(f"Error extracting email body: {e}")
            body = "[Error extracting body]"
        
        return body[:500]  # Limit to 500 characters
    
    def send_reply(self, to_email, subject, body, is_html=False):
        """Send an email reply"""
        try:
            self.smtp_connection = smtplib.SMTP(self.smtp_server, SMTP_PORT)
            self.smtp_connection.starttls()
            self.smtp_connection.login(self.email, self.password)
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"Re: {subject}"
            msg['From'] = self.email
            msg['To'] = to_email
            
            # Add body
            if is_html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            self.smtp_connection.send_message(msg)
            self.smtp_connection.quit()
            
            logger.info(f"Reply sent to {to_email}")
            return True
        
        except Exception as e:
            logger.error(f"Error sending reply: {e}")
            return False
    
    def forward_email(self, original_email, forward_to, note=""):
        """Forward an email to another address"""
        try:
            self.smtp_connection = smtplib.SMTP(self.smtp_server, SMTP_PORT)
            self.smtp_connection.starttls()
            self.smtp_connection.login(self.email, self.password)
            
            # Create forwarded message
            msg = MIMEMultipart()
            msg['Subject'] = f"Fwd: {original_email['subject']}"
            msg['From'] = self.email
            msg['To'] = forward_to
            
            # Add note and original body
            body = f"---Forwarded Message---\n{note}\n\nFrom: {original_email['from']}\nSubject: {original_email['subject']}\n\n{original_email['body']}"
            msg.attach(MIMEText(body, 'plain'))
            
            # Send
            self.smtp_connection.send_message(msg)
            self.smtp_connection.quit()
            
            logger.info(f"Email forwarded to {forward_to}")
            return True
        
        except Exception as e:
            logger.error(f"Error forwarding email: {e}")
            return False
    
    def mark_as_read(self, email_id):
        """Mark email as read"""
        try:
            self.connect_imap()
            self.imap_connection.select('INBOX')
            self.imap_connection.store(email_id, '+FLAGS', '\\Seen')
            logger.info(f"Marked email {email_id} as read")
            self.disconnect_imap()
            return True
        except Exception as e:
            logger.error(f"Error marking email as read: {e}")
            return False

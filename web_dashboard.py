#!/usr/bin/env python3
"""
Web Dashboard - Flask web interface for the Email Bot
Run with: python web_dashboard.py
"""

from flask import Flask, render_template, jsonify, request
from datetime import datetime
import json
import logging
from email_handler import EmailHandler
from database import Database
from config import SECRET_KEY, FLASK_HOST, FLASK_PORT

app = Flask(__name__)
app.secret_key = SECRET_KEY

db = Database()
email_handler = EmailHandler()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.route('/')
def dashboard():
    """Main dashboard"""
    return render_template('dashboard.html')

@app.route('/api/stats')
def get_stats():
    """Get bot statistics"""
    try:
        logs = db.get_logs(limit=100)
        
        total_processed = len(logs)
        replies_sent = sum(1 for log in logs if log[5] == 'replied')
        forwarded = sum(1 for log in logs if log[5] == 'forwarded')
        
        return jsonify({
            'total_emails_processed': total_processed,
            'auto_replies_sent': replies_sent,
            'emails_forwarded': forwarded,
            'last_checked': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/logs')
def get_logs():
    """Get recent logs"""
    try:
        limit = request.args.get('limit', 50, type=int)
        logs = db.get_logs(limit=limit)
        
        log_data = []
        for log in logs:
            log_data.append({
                'id': log[0],
                'from_email': log[1],
                'subject': log[2],
                'category': log[4],
                'action': log[5],
                'timestamp': log[8],
                'rule': log[9]
            })
        
        return jsonify(log_data)
    except Exception as e:
        logger.error(f"Error getting logs: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/unread-count')
def unread_count():
    """Get count of unread emails"""
    try:
        emails = email_handler.get_unread_emails(limit=1)
        return jsonify({'unread_count': len(emails)})
    except Exception as e:
        logger.error(f"Error getting unread count: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/status')
def status():
    """Get bot status"""
    return jsonify({
        'status': 'running',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/rules')
def get_rules():
    """Get all rules"""
    try:
        with open('rules.json', 'r') as f:
            rules_data = json.load(f)
            return jsonify(rules_data['rules'])
    except Exception as e:
        logger.error(f"Error getting rules: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/rules/<int:rule_id>', methods=['PUT'])
def update_rule(rule_id):
    """Update a specific rule"""
    try:
        data = request.json
        with open('rules.json', 'r') as f:
            rules_data = json.load(f)
        
        for rule in rules_data['rules']:
            if rule['rule_id'] == rule_id:
                rule.update(data)
                break
        
        with open('rules.json', 'w') as f:
            json.dump(rules_data, f, indent=2)
        
        logger.info(f"Rule {rule_id} updated")
        return jsonify({'message': 'Rule updated successfully'})
    except Exception as e:
        logger.error(f"Error updating rule: {e}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    logger.info("\n" + "*"*50)
    logger.info("🌐 EMAIL BOT WEB DASHBOARD")
    logger.info(f"Starting server on {FLASK_HOST}:{FLASK_PORT}")
    logger.info(f"Open http://localhost:{FLASK_PORT}")
    logger.info("*"*50 + "\n")
    
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=True)

# 📧 Email Auto-Responder Bot

An intelligent Python-based email automation tool that monitors your inbox, automatically responds to emails, categorizes messages, and forwards them to appropriate departments. Perfect for customer support, business automation, and workflow optimization.

## ✨ Features

- 🤖 **Automatic Response System** - Reply to emails based on keywords and patterns
- 📂 **Email Categorization** - Automatically sort emails into categories (Support, Sales, HR, etc.)
- 🔄 **Smart Forwarding** - Route emails to correct departments/people
- ⏰ **Schedule Management** - Set working hours and auto-responders
- 📊 **Analytics & Reporting** - Track email responses and patterns
- 🔐 **Secure** - OAuth2 authentication, no password storage
- 🎨 **Web Dashboard** - Monitor bot activity in real-time
- 📝 **Custom Rules** - Create flexible email handling rules
- 💾 **Database Logging** - Track all automated responses
- 🚀 **Easy Deployment** - Works with Gmail, Outlook, and other IMAP/SMTP providers

## 🛠️ Technology Stack

- **Python 3.8+** - Core language
- **smtplib & imaplib** - Email protocol handling
- **Flask** - Web dashboard
- **SQLite** - Database for logging
- **regex** - Pattern matching for categorization
- **schedule** - Task scheduling
- **python-dotenv** - Environment variables

## 📋 Prerequisites

- Python 3.8 or higher
- Gmail account (or other email provider)
- App Password (for Gmail: [Setup Guide](https://support.google.com/accounts/answer/185833))
- Git & pip installed

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/ISI-RA/email-auto-responder-bot.git
cd email-auto-responder-bot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
# Gmail Configuration
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
IMAP_SERVER=imap.gmail.com
SMTP_SERVER=smtp.gmail.com

# Bot Settings
CHECK_INTERVAL=60
ENABLE_RESPONSES=true
WORKING_HOURS_START=09:00
WORKING_HOURS_END=18:00

# Flask Dashboard
FLASK_HOST=0.0.0.0
FLASK_PORT=5000
FLASK_DEBUG=false
```

**Note:** For Gmail, use an [App Password](https://myaccount.google.com/apppasswords), not your regular password!

### 4. Run the Bot

#### **CLI Mode (Simple)**
```bash
python bot.py
```

#### **With Web Dashboard**
```bash
python web_dashboard.py
```

Then open your browser: `http://localhost:5000`

## 📁 Project Structure

```
email-auto-responder-bot/
├── README.md
├── requirements.txt
├── .env.example
├── bot.py                      # Main bot logic
├── email_handler.py            # Email operations (IMAP/SMTP)
├── config.py                   # Configuration & settings
├── rules.json                  # Email rules & patterns
├── web_dashboard.py            # Flask web interface
├── database.py                 # SQLite database operations
├── utils.py                    # Utility functions
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── logs.html
│   ├── rules.html
│   └── settings.html
├── static/
│   ├── style.css
│   ├── script.js
│   └── images/
└── logs/
    └── bot.log
```

## 📝 How It Works

### **1. Email Monitoring Loop**
- Connects to your email inbox every N seconds
- Fetches unread emails
- Checks sender, subject, and body against rules

### **2. Rule Matching**
- Matches emails against predefined rules
- Identifies category, urgency, and required action
- Determines if auto-response is needed

### **3. Auto-Response**
- Sends intelligent replies based on rules
- Logs all responses to database
- Marks email as read (optional)

### **4. Forwarding/Categorization**
- Routes emails to appropriate departments
- Adds labels/categories for organization
- Creates task tickets if needed

### **5. Analytics**
- Tracks response times
- Monitors patterns
- Generates reports

## 🎯 Usage Examples

### **Example 1: Auto-Reply to "Out of Office" Inquiries**

```json
{
  "rule_id": 1,
  "name": "Out of Office Reply",
  "active": true,
  "conditions": {
    "keywords": ["when", "available", "back"],
    "match_type": "any"
  },
  "action": "reply",
  "response": "Thank you for your email. I am currently out of the office and will return on Monday. For urgent matters, please contact support@company.com"
}
```

### **Example 2: Auto-Categorize Support Tickets**

```json
{
  "rule_id": 2,
  "name": "Support Ticket Categorization",
  "active": true,
  "conditions": {
    "keywords": ["issue", "bug", "error", "problem"],
    "match_type": "any"
  },
  "action": "categorize",
  "category": "support",
  "forward_to": "support@company.com"
}
```

### **Example 3: Forward Sales Inquiries**

```json
{
  "rule_id": 3,
  "name": "Sales Lead",
  "active": true,
  "conditions": {
    "keywords": ["pricing", "demo", "quote", "interested"],
    "match_type": "any"
  },
  "action": "forward",
  "forward_to": "sales@company.com",
  "add_note": "Auto-forwarded sales inquiry"
}
```

## 🖥️ Web Dashboard

Access the dashboard at `http://localhost:5000` to:

- 📊 **View Statistics** - Response rates, email volumes
- 📝 **Manage Rules** - Create, edit, delete automation rules
- 📋 **View Logs** - Track all bot activities
- ⚙️ **Settings** - Configure bot behavior
- 🚀 **Start/Stop Bot** - Control the automation
- 🔍 **Search Logs** - Find specific responses

## 🔧 Configuration

### **Edit Rules**

Edit `rules.json` to customize behavior:

```json
{
  "rules": [
    {
      "rule_id": 1,
      "name": "Rule Name",
      "active": true,
      "conditions": {
        "keywords": ["word1", "word2"],
        "from_domain": "example.com",
        "subject_contains": "text",
        "match_type": "all" // or "any"
      },
      "action": "reply",
      "response": "Auto-reply message",
      "forward_to": "email@example.com"
    }
  ]
}
```

### **Supported Actions**

- `reply` - Send auto-reply
- `forward` - Forward to another email
- `categorize` - Add label/category
- `delete` - Move to trash
- `archive` - Archive email
- `snooze` - Snooze for later

## 📊 Database Schema

The bot logs all activities in SQLite:

```sql
-- Table: email_logs
- id (PRIMARY KEY)
- from_email
- subject
- body
- category
- action_taken
- response_sent
- timestamp
- rule_matched

-- Table: bot_stats
- date
- emails_received
- emails_processed
- auto_replies_sent
- emails_forwarded
```

## 🔐 Security Best Practices

✅ **Never commit `.env` file** - Use `.env.example` as template  
✅ **Use App Passwords** - Not your actual Gmail password  
✅ **Enable 2FA** - For your email account  
✅ **Rotate Credentials** - Periodically change app passwords  
✅ **HTTPS Only** - For web dashboard in production  
✅ **Limit Forwarding** - Only to trusted email addresses  

## 📈 Performance Tips

- Adjust `CHECK_INTERVAL` based on your email volume
- Use specific keywords to reduce false matches
- Enable `WORKING_HOURS` to avoid off-hours processing
- Archive old logs periodically

## 🐛 Troubleshooting

### **Bot won't connect to Gmail**
```
Solution: Use App Password, not your regular password
- Go to myaccount.google.com/apppasswords
- Generate a 16-character password
- Paste it in .env file
```

### **Emails not being received**
```
Solution: Check IMAP is enabled
- Gmail: Settings > Forwarding and POP/IMAP > Enable IMAP
- Verify IMAP_SERVER and SMTP_SERVER in .env
```

### **High memory usage**
```
Solution: Reduce CHECK_INTERVAL or limit email batch size
- Increase CHECK_INTERVAL from 30 to 60+ seconds
- Reduce MAX_EMAILS_PER_CHECK in config.py
```

## 🚀 Deployment

### **Deploy to Heroku**

```bash
heroku create your-app-name
git push heroku main
heroku config:set EMAIL_ADDRESS=your-email@gmail.com
heroku config:set EMAIL_PASSWORD=your-app-password
```

### **Deploy to PythonAnywhere**

1. Upload files to PythonAnywhere
2. Create virtual environment
3. Install requirements
4. Set up cron job for bot.py

### **Deploy to AWS Lambda**

Use `lambda_handler.py` for serverless execution.

## 📚 Learning Outcomes

By working with this project, you'll learn:

✅ IMAP & SMTP protocols  
✅ Email automation patterns  
✅ Regular expressions for pattern matching  
✅ Flask web framework  
✅ Database operations (SQLite)  
✅ Background task scheduling  
✅ Security best practices (authentication, credentials)  
✅ Logging & monitoring  
✅ Error handling & resilience  
✅ Environment configuration  

## 🎓 Advanced Features (Future)

- [ ] AI-powered email classification (NLP)
- [ ] Machine learning for smart responses
- [ ] Integration with Slack notifications
- [ ] Support for multiple email accounts
- [ ] Attachment handling
- [ ] Calendar integration
- [ ] SMS notifications
- [ ] Docker containerization

## 📝 API Reference

### **Get Email Count**
```bash
GET /api/email-count
Response: {"total": 42, "unread": 5, "processed": 37}
```

### **Get Bot Status**
```bash
GET /api/status
Response: {"running": true, "last_check": "2026-05-13 15:30:00"}
```

### **Get Recent Logs**
```bash
GET /api/logs?limit=10
Response: [{"id": 1, "action": "reply", "timestamp": "..."}]
```

### **Create Rule**
```bash
POST /api/rules
Body: {"name": "...", "conditions": {...}, "action": "..."}
```

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👨‍💻 Author

**ISI-RA** - [GitHub Profile](https://github.com/ISI-RA)

## 🙏 Acknowledgments

- Inspired by business automation needs
- Built with Python community libraries
- Special thanks to [smtplib](https://docs.python.org/3/library/smtplib.html) and [imaplib](https://docs.python.org/3/library/imaplib.html) documentation

---

## 💡 Need Help?

- 📖 Check the [Wiki](https://github.com/ISI-RA/email-auto-responder-bot/wiki)
- 🐛 Report bugs in [Issues](https://github.com/ISI-RA/email-auto-responder-bot/issues)
- 💬 Start a [Discussion](https://github.com/ISI-RA/email-auto-responder-bot/discussions)

**Happy Automating!** 🚀

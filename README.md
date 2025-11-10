# Post-Conversation Analysis - Django REST API

A production-ready Django REST Framework application that automatically analyzes conversations between AI agents and human users, extracting insights about clarity, sentiment, empathy, resolution rates, and more.

## 🎯 Project Overview

This application performs comprehensive post-conversation analysis on chat messages and stores results in a database. It analyzes **10+ parameters** including clarity, relevance, accuracy, sentiment, empathy, and resolution. The system includes **automated daily analysis** using Celery Beat scheduling.

**Objective:** Build an automated Django application that performs post-conversation analysis on chat messages between an AI agent and a human user, storing results in a database with scheduled automation.

---

## ✨ Features

- ✅ **10+ Analysis Metrics**
  - Clarity Score (readability assessment)
  - Relevance Score (topic alignment)
  - Accuracy Score (confidence detection)
  - Completeness Score (answer completeness)
  - Sentiment Analysis (positive/neutral/negative)
  - Empathy Score (emotional understanding)
  - Response Time (average message delay)
  - Resolution Detection (issue resolved?)
  - Escalation Detection (needs human help?)
  - Fallback Count (AI uncertainty tracking)
  - Overall Score (weighted composite)

- ✅ **REST API** - Full CRUD operations on conversations
- ✅ **VADER Sentiment Analysis** - Optimized for conversational text
- ✅ **Automated Daily Analysis** - Celery Beat scheduled tasks
- ✅ **SQLite Database** - Proper schema with relationships
- ✅ **Django Admin** - Beautiful admin interface
- ✅ **Comprehensive Logging** - Error tracking and debugging
- ✅ **Production Ready** - Error handling, validation, security


---

## 📋 Project Structure

```
post-conversation-analysis/
├── config/
│   ├── __init__.py
│   ├── settings.py          # Django configuration
│   ├── urls.py              # URL routing
│   ├── celery.py            # Celery setup
│   └── wsgi.py              # Production deployment
│
├── conversations/           # App for managing conversations
│   ├── models.py            # Database tables
│   ├── views.py             # API endpoints
│   ├── serializers.py       # JSON conversion
│   ├── admin.py             # Django admin interface
│   └── migrations/          # Database changes
│
├── analysis/                # App for analysis logic
│   ├── analyzer.py          # 10+ analysis functions
│   ├── tasks.py             # Celery background tasks
│   └── migrations/
│
├── logs/                    # Application logs
├── venv/                    # Python virtual environment
├── manage.py                # Django management
├── db.sqlite3               # SQLite database
├── requirements.txt         # Python dependencies
```

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### 2. Setup

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/post-conversation-analysis.git
cd post-conversation-analysis

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('vader_lexicon'); nltk.download('punkt')"

# Create database
python manage.py makemigrations
python manage.py makemigrations conversations
python manage.py makemigrations analysis
python manage.py migrate

# Create admin user (optional)
python manage.py createsuperuser
```

### 3. Run Application

**Terminal 1 - Django Server:**
```bash
python manage.py runserver
# Visit: http://localhost:8000/api/
```

**Terminal 2 - Celery Worker:**
```bash
celery -A config worker -l info
```

**Terminal 3 - Celery Beat (Scheduler):**
```bash
celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

---

## 📚 API Endpoints

### Conversations

| Method | Endpoint | Description | Request |
|--------|----------|-------------|---------|
| POST | `/api/conversations/batch-create/` | Create conversation with messages | JSON with title & messages |
| GET | `/api/conversations/` | List all conversations | - |
| GET | `/api/conversations/{id}/` | Get conversation details | - |
| POST | `/api/conversations/{id}/analyze/` | Trigger analysis | - |
| GET | `/api/conversations/analytics/` | Get aggregated stats | - |

### Analysis

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/analysis/` | List all analyses |
| GET | `/api/analysis/{id}/` | Get specific analysis |
| GET | `/api/analysis/?sentiment=positive` | Filter by sentiment |
| GET | `/api/analysis/?escalation_needed=true` | Filter escalations |

---


```

### View Analysis Results

```bash
curl http://localhost:8000/api/analysis/
```

### Get Aggregated Statistics

```bash
curl http://localhost:8000/api/conversations/analytics/
```

---

## 📊 Analysis Metrics Explained

### 1. Clarity Score (0-100)
Measures how easy the response is to understand by analyzing sentence length and structure.
- **High (>80)**: Short, clear sentences
- **Low (<50)**: Long, complex sentences

### 2. Relevance Score (0-100)
Checks if AI response stays on topic using keyword overlap.
- **High (>80)**: Many shared words between question and answer
- **Low (<30)**: Different topics discussed

### 3. Accuracy Score (0-100)
Detects confidence by checking for uncertainty language.
- **High (>80)**: Confident, definitive statements
- **Low (<50)**: Many uncertainty phrases ("maybe", "I think", "I'm not sure")

### 4. Completeness Score (0-100)
Evaluates if the answer is complete with proper length and details.
- **High (>80)**: Long response with examples
- **Low (<50)**: Short, vague response

### 5. Sentiment (positive/neutral/negative)
Uses VADER (Valence Aware Dictionary and sEntiment Reasoner) for emotion detection.
- **Positive**: User is satisfied/happy
- **Neutral**: Factual, no emotion
- **Negative**: User is unhappy/frustrated

### 6. Empathy Score (0-100)
Detects empathetic language like "I understand", "I apologize", etc.
- **High (>70)**: Shows understanding and care
- **Low (<30)**: Robotic, no emotional support

### 7. Response Time (seconds)
Average time between user and AI messages.

### 8. Resolution (true/false)
Detected by keywords ("thanks", "ok", "perfect") or brief final message after multiple exchanges.

### 9. Escalation Needed (true/false)
Triggered if: negative sentiment + multiple fallbacks OR conversation exceeds 5 user messages.

### 10. Fallback Count (integer)
Counts how many times AI said "I don't know" or similar phrases.

### 11. Overall Score (0-100)
Weighted average combining all metrics:
- Resolution: 20% (most important)
- Clarity: 15%
- Relevance: 15%
- Accuracy: 15%
- Others: 5-10% each

---
# 🧪 Complete Testing Guide - Step by Step

This guide shows you exactly how to test the entire system with sample data.

---

## ✅ Prerequisites

Make sure you have:
1. ✅ Django server running: `python manage.py runserver`
2. ✅ Celery worker running: `celery -A config worker -l info`
3. ✅ Celery beat running: `celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler`

---

## 📊 Test 1: View All Conversations

**Command:**
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/api/conversations/" -Method GET
```

**Expected Output:**
```json
{
  "count": 0,
  "next": null,
  "previous": null,
  "results": []
}
```

(Empty if no conversations created yet)

---

## ➕ Test 2: Create Sample Conversation #1 - Order Support

**Command:**
```powershell
$body = @{
    title = "Order Support"
    messages = @(
        @{ sender = "user"; text = "Hi, I need help with my order." },
        @{ sender = "ai"; text = "Sure! Can you please share your order ID?" },
        @{ sender = "user"; text = "It is 12345." },
        @{ sender = "ai"; text = "Thanks! Your order has been shipped and will arrive tomorrow." },
        @{ sender = "user"; text = "Perfect, thanks so much!" }
    )
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/api/conversations/batch-create/" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body
```

**Expected Output:**
```json
{
  "id": 1,
  "title": "Order Support",
  "messages": [
    {"id": 1, "sender": "user", "text": "Hi, I need help with my order."},
    {"id": 2, "sender": "ai", "text": "Sure! Can you please share your order ID?"},
    ...
  ],
  "created_at": "2025-11-10T20:00:00Z",
  "is_analyzed": false
}
```

---

## ➕ Test 3: Create Sample Conversation #2 - Technical Issue

**Command:**
```powershell
$body = @{
    title = "Technical Issue"
    messages = @(
        @{ sender = "user"; text = "My app keeps crashing." },
        @{ sender = "ai"; text = "I'm sorry to hear that. I don't have specific information about your issue." },
        @{ sender = "user"; text = "It crashes when I click on settings." },
        @{ sender = "ai"; text = "I'm not sure what's causing that. You might need to contact support." },
        @{ sender = "user"; text = "This is frustrating. No one is helping me." },
        @{ sender = "ai"; text = "I apologize for the inconvenience. I'm unable to resolve this issue." }
    )
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/api/conversations/batch-create/" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body
```

**What You'll See:**
- Issue NOT resolved (too many messages, AI can't help)
- Negative sentiment (user is frustrated)
- Multiple fallbacks (AI said "I don't know", "I'm not sure")
- Should recommend escalation

---

## ➕ Test 4: Create Sample Conversation #3 - Billing Issue

**Command:**
```powershell
$body = @{
    title = "Billing Issue"
    messages = @(
        @{ sender = "user"; text = "Why was I charged twice?" },
        @{ sender = "ai"; text = "I understand your concern. Let me check that for you. Can you provide your account email?" },
        @{ sender = "user"; text = "It's john@example.com" },
        @{ sender = "ai"; text = "I found the issue - there was a duplicate charge. I've processed a refund for $50. You should see it in 3-5 business days. I sincerely apologize for this error." },
        @{ sender = "user"; text = "Thank you for fixing that!" }
    )
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/api/conversations/batch-create/" `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body $body
```

**What You'll See:**
- Issue RESOLVED (user said "Thank you")
- Positive sentiment (user is satisfied)
- High empathy (AI said "I understand", "I sincerely apologize")
- No escalation needed

---

## 📋 Test 5: View All Conversations Created

**Command:**
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/api/conversations/" -Method GET
```

**Expected Output:**
```json
{
  "count": 3,
  "results": [
    {"id": 1, "title": "Order Support", "message_count": 5, "is_analyzed": false},
    {"id": 2, "title": "Technical Issue", "message_count": 6, "is_analyzed": false},
    {"id": 3, "title": "Billing Issue", "message_count": 5, "is_analyzed": false}
  ]
}
```

---

## 🔍 Test 6: Analyze Conversation #1

**Command:**
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/api/conversations/1/analyze/" -Method POST
```

**Expected Output:**
```json
{
  "id": 1,
  "conversation": 1,
  "conversation_title": "Order Support",
  "clarity_score": 97.33,
  "relevance_score": 20.0,
  "accuracy_score": 100.0,
  "completeness_score": 85.0,
  "sentiment": "positive",
  "sentiment_score": 0.27,
  "empathy_score": 20.0,
  "response_time_avg": 3.0,
  "resolution": true,
  "escalation_needed": false,
  "fallback_count": 0,
  "overall_score": 78.27
}
```

**Analysis:**
- ✅ Resolution: TRUE (issue was solved)
- ✅ Sentiment: POSITIVE (user is happy)
- ✅ No escalation needed
- ✅ No fallbacks (AI was helpful)

---

## 🔍 Test 7: Analyze Conversation #2

**Command:**
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/api/conversations/2/analyze/" -Method POST
```

**Expected Output (Different from #1):**
```json
{
  "id": 2,
  "conversation": 2,
  "conversation_title": "Technical Issue",
  "clarity_score": 95.0,
  "relevance_score": 15.0,
  "accuracy_score": 60.0,
  "completeness_score": 50.0,
  "sentiment": "negative",
  "sentiment_score": -0.45,
  "empathy_score": 15.0,
  "response_time_avg": 3.0,
  "resolution": false,
  "escalation_needed": true,
  "fallback_count": 2,
  "overall_score": 42.5
}
```

**Analysis:**
- ❌ Resolution: FALSE (issue NOT solved)
- ❌ Sentiment: NEGATIVE (user is frustrated)
- ⚠️ Escalation: TRUE (needs human help!)
- ❌ Multiple fallbacks (AI couldn't help)
- ❌ Low empathy

---

## 🔍 Test 8: Analyze Conversation #3

**Command:**
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/api/conversations/3/analyze/" -Method POST
```

**Expected Output (Best one):**
```json
{
  "id": 3,
  "conversation": 3,
  "conversation_title": "Billing Issue",
  "clarity_score": 98.5,
  "relevance_score": 85.0,
  "accuracy_score": 100.0,
  "completeness_score": 95.0,
  "sentiment": "positive",
  "sentiment_score": 0.65,
  "empathy_score": 90.0,
  "response_time_avg": 3.0,
  "resolution": true,
  "escalation_needed": false,
  "fallback_count": 0,
  "overall_score": 88.5
}
```

**Analysis:**
- ✅ Resolution: TRUE (issue solved)
- ✅ Sentiment: POSITIVE (user is very happy)
- ✅ High empathy (AI was very understanding)
- ✅ High overall score (best conversation!)

---

## 📊 Test 9: View All Analysis Results

**Command:**
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/api/analysis/" -Method GET
```

**Expected Output:**
```json
{
  "count": 3,
  "results": [
    {
      "id": 1,
      "conversation_title": "Order Support",
      "overall_score": 78.27,
      "sentiment": "positive",
      "resolution": true,
      "escalation_needed": false
    },
    {
      "id": 2,
      "conversation_title": "Technical Issue",
      "overall_score": 42.5,
      "sentiment": "negative",
      "resolution": false,
      "escalation_needed": true
    },
    {
      "id": 3,
      "conversation_title": "Billing Issue",
      "overall_score": 88.5,
      "sentiment": "positive",
      "resolution": true,
      "escalation_needed": false
    }
  ]
}
```

---

## 📈 Test 10: Get Aggregated Analytics

**Command:**
```powershell
Invoke-WebRequest -Uri "http://localhost:8000/api/conversations/analytics/" -Method GET
```

**Expected Output:**
```json
{
  "total_conversations": 3,
  "average_overall_score": 69.76,
  "average_sentiment_score": 0.16,
  "conversations_needing_escalation": 1,
  "conversations_resolved": 2,
  "resolution_rate": 66.67
}
```

**What This Means:**
- 📊 Total conversations analyzed: 3
- 📈 Average overall score: 69.76/100 (decent)
- 😊 Average sentiment: 0.16 (slightly positive)
- ⚠️ Needs escalation: 1 (Technical Issue)
- ✅ Resolved: 2 out of 3 (66.67%)

---

## 🔄 Test 11: Test Automated Daily Analysis (Manual Trigger)

**Command (Python shell):**
```bash
python manage.py shell
```

Then inside Python:
```python
from analysis.tasks import analyze_new_conversations
result = analyze_new_conversations()
print(result)
```

**Expected Output:**
```
{'status': 'success', 'analyzed': 0, 'failed': 0}
```

(0 new conversations since we already analyzed the 3)

---

## 🎯 Summary of What You Tested

| Test | Command | Purpose | Result |
|------|---------|---------|--------|
| 1 | GET /conversations/ | View conversations | Empty list (0) |
| 2 | POST batch-create | Create conversation #1 | ID: 1 created |
| 3 | POST batch-create | Create conversation #2 | ID: 2 created |
| 4 | POST batch-create | Create conversation #3 | ID: 3 created |
| 5 | GET /conversations/ | View all conversations | Count: 3 |
| 6 | POST /1/analyze/ | Analyze #1 | Overall: 78.27 |
| 7 | POST /2/analyze/ | Analyze #2 | Overall: 42.5 |
| 8 | POST /3/analyze/ | Analyze #3 | Overall: 88.5 |
| 9 | GET /analysis/ | View all analyses | Count: 3 |
| 10 | GET /analytics/ | View stats | Resolution rate: 66.67% |
| 11 | Shell task | Manual automation | Works! |

---

## ✅ All Tests Passed!

If you see all of this working, your system is **100% complete** and ready for submission! 🚀

The system successfully:
- ✅ Accepts conversations via API
- ✅ Analyzes with 10+ metrics
- ✅ Detects sentiment (positive/negative)
- ✅ Detects resolution
- ✅ Detects escalation needs
- ✅ Stores results in database
- ✅ Provides aggregated statistics
- ✅ Supports automation

## 📤 Example Response

```json
{
  "id": 1,
  "conversation": 1,
  "conversation_title": "Customer Support",
  "clarity_score": 97.33,
  "relevance_score": 20.0,
  "accuracy_score": 100.0,
  "completeness_score": 85.0,
  "sentiment": "positive",
  "sentiment_score": 0.273,
  "empathy_score": 20.0,
  "response_time_avg": 3.0,
  "resolution": true,
  "escalation_needed": false,
  "fallback_count": 0,
  "overall_score": 78.27,
  "created_at": "2025-11-09T09:16:47.658390Z"
}
```

---

## ⚙️ Configuration

### Change Celery Schedule

Edit `config/settings.py`:

```python
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'analyze-new-conversations': {
        'task': 'analysis.tasks.analyze_new_conversations',
        'schedule': crontab(hour=2, minute=0),  # 2 AM UTC daily
    },
}
```

### Switch to PostgreSQL (Production)

Edit `config/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'conversation_analysis',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

Then run:
```bash
pip install psycopg2-binary
python manage.py migrate
```


---

## 📚 Technologies Used

| Technology | Purpose |
|-----------|---------|
| **Django 4.2** | Web framework |
| **Django REST Framework** | REST API |
| **Celery 5.3** | Background tasks |
| **NLTK** | NLP & sentiment analysis |
| **SQLite** | Database |
| **SQLAlchemy** | Database ORM |

---

## 🎓 Learning Resources

- Django Docs: https://docs.djangoproject.com/
- REST Framework: https://www.django-rest-framework.org/
- Celery: https://docs.celeryproject.org/
- VADER Sentiment: https://github.com/cjhutto/vaderSentiment
- REST API Design: https://restfulapi.net/

---

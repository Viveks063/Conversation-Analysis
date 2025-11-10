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

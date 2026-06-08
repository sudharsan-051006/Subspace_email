# AI Outreach Agent 🚀

AI Outreach Agent is a Django-based lead generation and cold outreach platform that automates the process of finding potential customers, generating personalized emails, and sending outreach campaigns.

---

## Features

### Lead Discovery

* Search using a seed company domain.
* Find lookalike companies using Ocean.io.
* Fetch company details such as:

  * Company Name
  * Industry
  * Employee Count
  * Domain

### Decision Maker Discovery

* Search decision makers using Prospeo.
* Filter leadership roles such as:

  * CEO
  * Founder
  * CTO
  * CFO
  * COO
  * CMO
  * VP
  * Head of Department

### Email Enrichment

* Retrieve verified work emails using Prospeo Enrichment API.
* Display LinkedIn profiles alongside contact information.

### AI Email Generation

* Generate personalized cold outreach emails using Groq AI.
* Create custom email subjects.
* Generate HTML-formatted outreach messages.

### Email Preview

* Review generated emails before sending.
* Edit subject and email content.
* Preview bulk outreach campaigns.

### Email Sending

* Send emails using Brevo.
* Bulk email selected leads.
* Send emails to custom recipients.

---

## Tech Stack

### Backend

* Django
* Python

### APIs

* Ocean.io
* Prospeo
* Groq
* Brevo

### Frontend

* HTML
* CSS
* Django Templates

---

## Project Workflow

Seed Domain
↓
Ocean.io
↓
Lookalike Companies
↓
Prospeo Search
↓
Decision Makers
↓
Prospeo Enrichment
↓
Verified Emails
↓
Groq AI
↓
Personalized Outreach Email
↓
Brevo
↓
Email Delivery

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd project-folder
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux / Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
OCEAN_API_KEY=your_ocean_api_key

PROSPEO_API_KEY=your_prospeo_api_key

GROQ_API_KEY=your_groq_api_key

BREVO_API_KEY=your_brevo_api_key
```

---

## Run Project

Apply migrations:

```bash
python manage.py migrate
```

Start server:

```bash
python manage.py runserver
```

Visit:

```text
http://127.0.0.1:8000
```

---

## Deployment

### Render

Build Command:

```bash
pip install -r requirements.txt && python manage.py migrate
```

Start Command:

```bash
gunicorn subspace.wsgi:application
```

Add environment variables in Render Dashboard.

---

## Future Improvements

* Email open tracking
* Click tracking
* Campaign analytics dashboard
* CRM integration
* Automated follow-up sequences
* AI personalization using company data
* CSV export of leads
* Lead scoring system

---

## Author

Sudharsan Reddy

Built to automate prospect discovery and outbound outreach using AI.

```
```

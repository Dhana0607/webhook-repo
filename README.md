# 🔔 Webhook Receiver Service

This repository is created as part of the **TechStaX Developer Assessment**.  
It implements a webhook receiver service that listens to GitHub events, stores them in MongoDB, and displays them via a polling-based UI.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-green)](https://flask.palletsprojects.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-brightgreen)](https://www.mongodb.com/cloud/atlas)

---

## 📋 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Application](#-running-the-application)
- [API Documentation](#-api-documentation)
- [GitHub Webhook Setup](#-github-webhook-setup)
- [Testing](#-testing)
- [Project Structure](#-project-structure)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)

---

## 🚀 Features

- ✅ Receives GitHub **Push**, **Pull Request**, and **Merge** webhook events
- ✅ Stores events in **MongoDB Atlas** with duplicate prevention
- ✅ RESTful API to fetch latest events
- ✅ Simple, responsive UI that **polls every 15 seconds** for updates
- ✅ Real-time event display with timestamp and event details
- ✅ Clean, minimal implementation following best practices

---

## 🛠 Tech Stack

| Technology | Purpose |
|------------|---------|
| **Python 3.8+** | Backend language |
| **Flask** | Web framework |
| **MongoDB Atlas** | Cloud database |
| **GitHub Webhooks** | Event source |
| **HTML + JavaScript** | Frontend UI with polling |
| **ngrok** | Local tunnel for testing |

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher** ([Download](https://www.python.org/downloads/))
- **pip** (Python package manager)
- **Git** ([Download](https://git-scm.com/downloads))
- **MongoDB Atlas Account** ([Sign up free](https://www.mongodb.com/cloud/atlas/register))
- **GitHub Account** with a repository for testing webhooks
- **ngrok** (for local testing) ([Download](https://ngrok.com/download))

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Dhana0607/webhook-repo.git
cd webhook-repo
```

### 2️⃣ Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected packages:**
- Flask
- pymongo
- python-dotenv
- dnspython (for MongoDB Atlas)

---

## 🔐 Configuration

### Step 1: Set Up MongoDB Atlas

1. **Create a MongoDB Atlas Account**
   - Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register)
   - Sign up for a free account

2. **Create a Cluster**
   - Click "Build a Cluster" → Choose "Free Shared Cluster"
   - Select a cloud provider and region (closest to you)
   - Click "Create Cluster" (takes 3-5 minutes)

3. **Create Database User**
   - Go to "Database Access" → "Add New Database User"
   - Choose "Password" authentication
   - Username: `webhook_user` (or your choice)
   - Password: Generate a secure password
   - User Privileges: "Read and write to any database"
   - Click "Add User"

4. **Whitelist IP Address**
   - Go to "Network Access" → "Add IP Address"
   - Click "Allow Access from Anywhere" (0.0.0.0/0)
   - Or add your specific IP for better security
   - Click "Confirm"

5. **Get Connection String**
   - Go to "Clusters" → Click "Connect"
   - Choose "Connect your application"
   - Select "Python" and version "3.6 or later"
   - Copy the connection string:
   ```
   mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```

### Step 2: Create Environment File

Create a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# MongoDB Atlas Connection String
# Replace <username>, <password>, and <cluster-url> with your actual values
MONGO_URI=mongodb+srv://webhook_user:your_password@cluster0.xxxxx.mongodb.net/webhook_db?retryWrites=true&w=majority

# GitHub Webhook Secret (optional but recommended)
# Generate a random secret: python -c "import secrets; print(secrets.token_hex(32))"
WEBHOOK_SECRET=your_secret_key_here

# Flask Configuration
DEBUG=True
PORT=5000
```

**⚠️ Security Note:** Never commit `.env` to version control. It's already in `.gitignore`.

---

## ▶️ Running the Application

### Local Development

```bash
python app.py
```

The application will start on:
```
http://127.0.0.1:5000
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Access the UI

Open your browser and navigate to:
```
http://127.0.0.1:5000
```

You'll see the webhook events dashboard.

---

## 📡 API Documentation

### 1. Webhook Endpoint

**Receives GitHub webhook events**

```http
POST /webhook
Content-Type: application/json
X-GitHub-Event: push | pull_request
X-Hub-Signature-256: sha256=xxxxx (if secret configured)
```

**Supported Events:**
- `push` - Code pushed to repository
- `pull_request` (opened) - New pull request created
- `pull_request` (closed + merged) - Pull request merged

**Example Payload (Push Event):**
```json
{
  "ref": "refs/heads/main",
  "repository": {
    "name": "action-repo",
    "full_name": "Dhana0607/action-repo"
  },
  "pusher": {
    "name": "Dhana0607"
  },
  "commits": [
    {
      "id": "abc123...",
      "message": "Update README",
      "timestamp": "2025-01-30T10:30:00Z"
    }
  ]
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Event received"
}
```

### 2. Events API

**Fetch stored webhook events**

```http
GET /events
```

**Response:**
```json
[
  {
    "_id": "65b9c8f...",
    "event_id": "12345-67890-abcdef",
    "event_type": "push",
    "repository": "Dhana0607/action-repo",
    "author": "Dhana0607",
    "timestamp": "2025-01-30T10:30:00Z",
    "details": {
      "commits": 3,
      "branch": "main",
      "message": "Update README"
    }
  },
  {
    "_id": "65b9c8e...",
    "event_type": "pull_request",
    "repository": "Dhana0607/action-repo",
    "author": "Dhana0607",
    "timestamp": "2025-01-30T09:15:00Z",
    "details": {
      "action": "opened",
      "pr_number": 42,
      "title": "Add new feature",
      "from_branch": "feature-branch",
      "to_branch": "main"
    }
  }
]
```

**Query Parameters (optional):**
- `limit` - Number of events to return (default: 50, max: 100)
  ```
  GET /events?limit=10
  ```

### 3. Health Check

**Check if service is running**

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-01-30T10:30:00Z"
}
```

---

## 🔗 GitHub Webhook Setup

### Step 1: Expose Local Server (for testing)

Use **ngrok** to create a public URL for your local server:

```bash
# Start your Flask app first
python app.py

# In a new terminal, run ngrok
ngrok http 5000
```

You'll see output like:
```
Forwarding    https://abc123.ngrok-free.app -> http://localhost:5000
```

Copy the `https://` URL (e.g., `https://abc123.ngrok-free.app`)

### Step 2: Configure GitHub Webhook

1. **Go to Your Repository**
   - Navigate to your `action-repo` on GitHub
   - Example: `https://github.com/Dhana0607/action-repo`

2. **Open Webhook Settings**
   - Click "Settings" tab
   - Click "Webhooks" in the left sidebar
   - Click "Add webhook"

3. **Configure Webhook**
   
   | Field | Value |
   |-------|-------|
   | **Payload URL** | `https://abc123.ngrok-free.app/webhook` |
   | **Content type** | `application/json` |
   | **Secret** | (Your `WEBHOOK_SECRET` from `.env`) |
   | **SSL verification** | Enable SSL verification |
   | **Which events?** | Let me select individual events |
   
   Select these events:
   - ✅ Pushes
   - ✅ Pull requests

4. **Save Webhook**
   - Click "Add webhook"
   - GitHub will send a test ping event
   - Check that you see a green ✓ next to the webhook

### Step 3: Verify Webhook

GitHub will show recent deliveries at the bottom of the webhook settings page:
- Green checkmark = successful delivery
- Red X = failed delivery (click to see error details)

---

## 🧪 Testing

### Test Push Event

```bash
# In your action-repo
echo "Test webhook" >> README.md
git add .
git commit -m "Test push event"
git push origin main
```

**Expected Result:**
- Event appears in MongoDB
- UI shows the push event after next poll (max 15 seconds)

### Test Pull Request Event

```bash
# Create a new branch
git checkout -b test-webhook
echo "Test PR" >> test.txt
git add .
git commit -m "Test PR event"
git push origin test-webhook

# Go to GitHub and create a Pull Request from test-webhook to main
```

**Expected Result:**
- PR opened event appears in the UI

### Test Merge Event

```bash
# On GitHub, merge the Pull Request you just created
```

**Expected Result:**
- PR merged event appears in the UI

### Verify in MongoDB Atlas

1. Go to MongoDB Atlas → Clusters → Browse Collections
2. Database: `webhook_db` (or your database name)
3. Collection: `events`
4. You should see your webhook events stored as documents

---

## 📁 Project Structure

```
webhook-repo/
│
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not in git)
├── .env.example           # Template for .env
├── .gitignore             # Git ignore rules
├── README.md              # This file
│
├── templates/             # HTML templates (if using)
│   └── index.html        # UI dashboard
│
├── static/               # Static files (if using)
│   ├── css/
│   │   └── style.css    # Custom styles
│   └── js/
│       └── app.js       # Polling logic
│
└── venv/                 # Virtual environment (not in git)
```

---

## 🐛 Troubleshooting

### Issue: MongoDB Connection Failed

**Error:** `ServerSelectionTimeoutError` or `Authentication failed`

**Solutions:**
1. Check your `MONGO_URI` in `.env` is correct
2. Verify username and password are URL-encoded
   - Special characters like `@`, `#`, `!` need encoding
   - Use [URL Encoder](https://www.urlencoder.org/)
3. Check IP whitelist in MongoDB Atlas (Network Access)
4. Ensure database user has correct permissions

### Issue: Webhook Not Receiving Events

**Symptoms:** GitHub shows webhook sent, but nothing in database

**Solutions:**
1. Check ngrok is running: `curl https://your-url.ngrok-free.app/health`
2. Verify webhook URL in GitHub ends with `/webhook`
3. Check Flask console for error messages
4. Verify GitHub webhook shows green checkmark (successful delivery)
5. Check webhook signature if using `WEBHOOK_SECRET`

### Issue: Events Not Showing in UI

**Symptoms:** Database has events, but UI is empty

**Solutions:**
1. Check browser console for JavaScript errors (F12)
2. Verify `/events` endpoint returns data:
   ```bash
   curl http://localhost:5000/events
   ```
3. Check if polling is working (should update every 15 seconds)
4. Clear browser cache and refresh

### Issue: Duplicate Events

**Symptoms:** Same event appears multiple times

**Solutions:**
1. Check `event_id` field is being set correctly
2. Verify MongoDB unique index on `event_id`
3. GitHub may retry failed webhooks (check delivery history)

### Issue: ngrok URL Changes

**Symptoms:** Webhook stops working after restarting ngrok

**Solutions:**
1. Free ngrok URLs change every restart
2. Update GitHub webhook URL with new ngrok URL
3. Consider ngrok paid plan for fixed URLs
4. Or deploy to a permanent server (Heroku, Railway, etc.)

---

## 🚀 Deployment (Optional)

### Deploy to Railway

1. Create account at [Railway.app](https://railway.app/)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select `webhook-repo`
4. Add environment variables in Railway dashboard
5. Railway provides a permanent URL
6. Update GitHub webhook with Railway URL

### Deploy to Heroku

```bash
# Install Heroku CLI
# Create Procfile
echo "web: python app.py" > Procfile

# Deploy
heroku create webhook-receiver-app
heroku config:set MONGO_URI="your_connection_string"
git push heroku main
```

---

## 📊 Database Schema

### Events Collection

```javascript
{
  _id: ObjectId("..."),
  event_id: "12345-67890-abcdef",      // Unique event identifier
  event_type: "push" | "pull_request",  // Type of GitHub event
  repository: "username/repo-name",     // Full repository name
  author: "username",                   // User who triggered event
  timestamp: ISODate("2025-01-30T10:30:00Z"),
  details: {
    // Event-specific data
    // For push: commits, branch, message
    // For PR: action, pr_number, title, branches
  }
}
```

**Indexes:**
- `event_id` (unique) - Prevents duplicate events
- `timestamp` (descending) - Fast sorting for latest events

---

## 🤝 Contributing

This is an assessment project, but suggestions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -m 'Add improvement'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open a Pull Request

---

## 📝 Assessment Notes

This project was created following these requirements:
- ✅ Webhook receiver for GitHub events
- ✅ MongoDB storage with duplicate prevention
- ✅ RESTful API for event retrieval
- ✅ Polling-based UI (15-second intervals)
- ✅ Clean, minimal implementation
- ✅ Proper documentation

**Design Decisions:**
- Used Flask for simplicity and quick setup
- MongoDB for flexible schema and easy querying
- Polling over WebSockets to meet assessment requirements
- Minimal UI focusing on functionality over aesthetics

---

## 📄 License

This project is created for the TechStaX Developer Assessment.

---

## 📧 Contact

**Developer:** Dhana0607  
**Repository:** [webhook-repo](https://github.com/Dhana0607/webhook-repo)  
**Action Repository:** [action-repo](https://github.com/Dhana0607/action-repo)

---

## 🙏 Acknowledgments

- **TechStaX** for the assessment opportunity
- **GitHub** for webhook infrastructure
- **MongoDB** for database service
- **ngrok** for local testing tunnel

---

**Happy Coding! 🎉**

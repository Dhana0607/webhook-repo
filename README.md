# Webhook Receiver Service

This repository is created as part of the **TechStaX Developer Assessment**.  
It implements a webhook receiver service that listens to GitHub events, stores them in MongoDB, and displays them via a polling-based UI.

---

## 🚀 Features

- Receives GitHub **Push**, **Pull Request**, and **Merge** webhook events
- Stores events in **MongoDB Atlas**
- Exposes an API to fetch latest events
- Simple UI that **polls every 15 seconds**
- Prevents duplicate event inserts
- Clean, minimal implementation as per requirements

---

## 🛠 Tech Stack

- **Python**
- **Flask**
- **MongoDB Atlas**
- **GitHub Webhooks**
- **HTML + JavaScript (Polling UI)**

---
---
## ⚙️ Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Dhana0607/webhook-repo
cd webhook-repo

### 2️⃣ Create and activate virtual environment
```bash
python -m venv venv
venv\Scripts\activate   # Windows

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt

### 4️⃣ Configure environment variables

- Create a .env file in the project root:
```bash
MONGO_URI=mongodb+srv://<username>:<password>@<cluster-url>/
.env is intentionally excluded from version control.

### ▶️ Run the Application
```bash
python app.py
The application runs on:
http://127.0.0.1:5000

### Webhook Endpoint
POST /webhook
This endpoint listens to GitHub webhook events.
Supported Events
- Push
- Pull Request (opened)
- Merge (closed + merged)
### 📊 Events API
```bash
GET /events

Returns the latest stored events in JSON format.
Used by the UI for polling.

### Testing Webhooks Locally
Expose local server using ngrok:
```bash
ngrok http 5000

Add the ngrok URL to GitHub Webhooks in action-repo:
https://<ngrok-id>.ngrok-free.app/webhook

Trigger events:
- Push commits
- Open Pull Requests
- Merge Pull Requests
---

## Application Flow
1. GitHub events are triggered from the `action-repo`
2. GitHub sends webhook payloads to the Flask endpoint
3. Relevant event data is extracted and stored in MongoDB
4. The UI periodically fetches and displays the latest events

This repository focuses on clarity, correctness, and minimalism, following the guidelines provided in the assessment.

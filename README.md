# webhook-repo

This repository is created as part of the TechStaX developer assessment.

It contains a Flask-based webhook receiver that listens to GitHub webhook events sent from the `action-repo`. The application processes **Push**, **Pull Request**, and **Merge** events, extracts only the required fields from the payload, and stores them in MongoDB.

A minimal UI is included to display the latest repository activities. The UI polls the backend every 15 seconds and renders only new events in a clean and readable format, as specified in the assignment.

## Features
- GitHub webhook endpoint implemented using Flask
- Handles Push and Pull Request events and also merge. 
- Stores minimal required data in MongoDB
- Prevents duplicate event entries
- Simple UI that polls MongoDB every 15 seconds

## Tech Stack
- Python
- Flask
- MongoDB
- HTML, CSS, JavaScript

## Application Flow
1. GitHub events are triggered from the `action-repo`
2. GitHub sends webhook payloads to the Flask endpoint
3. Relevant event data is extracted and stored in MongoDB
4. The UI periodically fetches and displays the latest events

This repository focuses on clarity, correctness, and minimalism, following the guidelines provided in the assessment.

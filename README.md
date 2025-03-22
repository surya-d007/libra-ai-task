# Project Setup Guide

## Installation

### Step 1: Navigate to the Backend Directory

First, move to the backend directory using the following command:

```bash
cd Back-end
Step 2: Install Required Dependencies
Ensure you have Python installed, then install all necessary dependencies using:

bash
Copy
Edit
pip install -r requirements.txt
Step 3: Create a .env File
Create a .env file in the Back-end directory and add the following environment variables:

ini
Copy
Edit
SCOPES=scope access for the google oauth
OPEN_AI=open ai api key
PIPECONE=pipe cone api key
PIPECONE_REGION=us-east-1
INDEX_NAME=dense-index
Note: Replace the placeholder values with your actual API keys and configuration.

Step 4: Run the Application
Start the FastAPI server using Uvicorn:

bash
Copy
Edit
uvicorn main:app --reload
This will run the server in development mode with automatic reloading.

Usage
Once the server is running, access the API documentation at:

Swagger UI: http://127.0.0.1:8000/docs

Redoc: http://127.0.0.1:8000/redoc
```

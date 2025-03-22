# Project Setup Guide

## Installation for Back End

### Step 1: Navigate to the Backend Directory

First, move to the backend directory using the following command:

```bash
cd Back-end

Step 2: Install Required Dependencies
Ensure you have Python installed, then install all necessary dependencies using:

pip install -r requirements.txt

Step 3: Create a .env File

Create a .env file in the Back-end directory and add the following environment variables:


SCOPES=scope access for the google oauth
OPEN_AI=open ai api key
PIPECONE=pipe cone api key
PIPECONE_REGION=us-east-1
INDEX_NAME=dense-index

Note: Replace the placeholder values with your actual API keys and configuration.


Step 4: Run the Application
Start the FastAPI server using Uvicorn:

uvicorn main:app --reload

This will run the server in development mode with automatic reloading.

Usage
Once the server is running, access the API documentation at:

Swagger UI: http://127.0.0.1:8000/docs

Redoc: http://127.0.0.1:8000/redoc
```

## Installation for Front End


```

Requirements : pnpm 
Installation for Front End
Step 1: Navigate to the Frontend Directory
First, move to the frontend directory using the following command:


cd Front-end

Step 2: Install Required Dependencies
Ensure you have Node.js installed, then install all necessary dependencies using:

pnpm install

To run locally
pnpm run dev
```



from fastapi import FastAPI, HTTPException, Query
from google_auth_oauthlib.flow import Flow
from pinecone import Pinecone, ServerlessSpec
import os
from googleapiclient.http import MediaIoBaseDownload
import io
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (you can restrict to specific URLs)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


import json

from dotenv import load_dotenv, dotenv_values 
# loading variables from .env file
load_dotenv() 
import openai

openai.api_key = os.getenv("OPEN_AI")

SCOPES = ['https://www.googleapis.com/auth/drive']
REDIRECT_URI = 'http://localhost:5173/home'  # Update this based on your frontend URL



def make_file_public(creds, file_id):
    """Make a Google Drive file publicly accessible."""
    try:
        service = build('drive', 'v3', credentials=creds)
        permission = {
            'type': 'anyone',
            'role': 'reader'
        }
        service.permissions().create(
            fileId=file_id,
            body=permission
        ).execute()
        print(f"File with ID: {file_id} is now public.")
    except HttpError as error:
        print(f"An error occurred: {error}")



@app.get('/auth-url')
def get_auth_url():
    try:
        flow = Flow.from_client_secrets_file(
            'client_secret.json',
            scopes=SCOPES,
            redirect_uri=REDIRECT_URI
        )
        auth_url, _ = flow.authorization_url(prompt='consent', access_type='offline')
        return {'auth_url': auth_url}
    except Exception as e:
        return {'error': str(e)}


pinecone_api_key = os.getenv("PIPECONE")
pinecone_environment = os.getenv('PIPECONE_REGION')


pc = Pinecone(
    api_key=pinecone_api_key
)

# Now do stuff
# Create a dense index with integrated embedding
index_name = "dense-index"
if not pc.has_index("dense-index"):
    pc.create_index(
        name="dense-index",
        dimension=1536,
        metric='euclidean',
        spec=ServerlessSpec(
            cloud='aws',
            region=pinecone_environment
        )
    )
dense_index = pc.Index("dense-index")


@app.post('/ingest')
def ingest_files(auth_code: str = Query(...)):
    try:
        # Exchange the auth code for tokens
        flow = Flow.from_client_secrets_file(
            'client_secret.json',
            scopes=SCOPES,
            redirect_uri='http://localhost:5173/home'
        )
        flow.fetch_token(code=auth_code)
        creds = flow.credentials

        # Initialize Google Drive API
        service = build('drive', 'v3', credentials=creds)
        
        # Search for .txt and .md files
        query = "(mimeType='text/plain' or mimeType='text/markdown' or mimeType='text/x-markdown') and trashed=false"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            raise HTTPException(status_code=404, detail="No .txt or .md files found.")

        file_data = []
        for item in items:
            file_id = item['id']
            make_file_public(creds, file_id)
            file_name = item['name']

            # Read the file content
            request = service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                _, done = downloader.next_chunk()

            content = fh.getvalue().decode('utf-8')

            # Generate embeddings using OpenAI
            response = openai.Embedding.create(input=content, model='text-embedding-ada-002')
            embedding = response['data'][0]['embedding']

            # Upload to Pinecone
            metadata = {
                'name': file_name,
                'id': file_id,
                'downloadLink': f"https://drive.google.com/uc?id={file_id}&export=download",
                'text' : content
            }
            dense_index.upsert([(file_id, embedding, metadata)])

            file_data.append({'name': file_name, 'id': file_id, 'link': metadata['downloadLink']})

        return {'files': file_data , 'pinecone' : 'success'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    





# Endpoint to search data
@app.post('/search')
def search_files(query :  str = Query(...)):
    try:
        # Generate embedding for the query
        response = openai.Embedding.create(
            input=query,
            model='text-embedding-ada-002'
        )
        query_embedding = response['data'][0]['embedding']

        # Query Pinecone for similar embeddings
        search_results = dense_index.query(vector=query_embedding, top_k=3, include_metadata=True)

        search_results_dict = search_results.to_dict()  # Convert to dictionary
        
        # Extract and return metadata of the top matches
        matches = [
            {
                'name': match['metadata']['name'],
                'id': match['metadata']['id'],
                'downloadLink': match['metadata']['downloadLink'],
                'score': match['score']
            }
            for match in search_results['matches']
        ]

        relevant_docs = [
            f"{match['metadata']['text']}\n"
            for match in search_results['matches']
        ]

        # Form a prompt for OpenAI
        context = "\n\n".join(relevant_docs)
        
        prompt = f"Based on the following documents, answer the query: '{query}'\n\n{context}\nAnswer:"

        # Generate answer using GPT
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )
        answer = response.choices[0].message['content'].strip()

        return {
            'query': query,
            'answer': answer,
            'matches': [
                {
                    'name': match['metadata']['name'],
                    'id': match['metadata']['id'],
                    'downloadLink': match['metadata']['downloadLink'],
                    'score': match['score']
                }
                for match in search_results['matches']
            ]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    





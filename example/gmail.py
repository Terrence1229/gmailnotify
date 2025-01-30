import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pickle
import os
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect
from google_auth_oauthlib.flow import Flow
from django.shortcuts import redirect, render

# Global variables
CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), '../credentials.json')
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.modify']
REDIRECT_URI = 'http://localhost:8088/authcallback'
PICKLE_FILE = os.path.join(os.path.dirname(__file__), 'token.pickle')
# Create your views here.


class MAPIView:
    # Google OAuth Example
    def google_auth(request):
        flow = Flow.from_client_secrets_file(
            'credentials.json',
            scopes = SCOPES,
            redirect_uri = REDIRECT_URI
        )
        authorization_url, state = flow.authorization_url(prompt='consent')
        return HttpResponseRedirect(authorization_url)
    
    # Google OAuth Callback
    def authcallback(request):
        if request.method == 'GET':
            # Access query parameters from the GET request

            code = request.GET.get('code')
            if not code:
                return JsonResponse({"error": "Authorization code not provided"}, status=400)
            
             # Set up the OAuth flow
            flow = Flow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            flow.redirect_uri = REDIRECT_URI  # Set your redirect URI

            # Fetch the token using the authorization code
            flow.fetch_token(code=code)

            # Get the credentials
            credentials = flow.credentials
            
            # Save the credentials to a pickle file
            with open(PICKLE_FILE, 'wb') as token:
                pickle.dump(credentials, token)

            return redirect('/')

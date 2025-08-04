from django.shortcuts import redirect
from django.shortcuts import render
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from datetime import datetime, timedelta
import base64
import json

EBAY_AUTH_URL = "https://auth.ebay.com/oauth2/authorize"
EBAY_TOKEN_URL = "https://api.ebay.com/identity/v1/oauth2/token"

# Create your views here.
@api_view(['GET'])
def initiate_auth(request):
    scopes = [
        "https://api.ebay.com/oauth/api_scope",
        "https://api.ebay.com/oauth/api_scope/sell.inventory",
        "https://api.ebay.com/oauth/api_scope/sell.analytics",
        "https://api.ebay.com/oauth/api_scope/sell.fulfillment",
        "https://api.ebay.com/oauth/api_scope/sell.marketing",
        "https://api.ebay.com/oauth/api_scope/sell.marketing.readonly",
        "https://api.ebay.com/oauth/api_scope/sell.marketplace.insights.readonly",
        "https://api.ebay.com/oauth/api_scope/commerce.catalog.readonly",
        "https://api.ebay.com/oauth/api_scope/sell.finances",
        "https://api.ebay.com/oauth/api_scope/sell.payment.dispute",
        "https://api.ebay.com/oauth/api_scope/sell.item.draft",
        "https://api.ebay.com/oauth/api_scope/sell.item",
        "https://api.ebay.com/oauth/api_scope/sell.item.reputation",        
    ]
    
    auth_url = f"{EBAY_AUTH_URL}?client_id={settings.EBAY_APP_ID}&response_type=code&redirect_uri={settings.EBAY_REDIRECT_URI}&scope={' '.join(scopes)}"
    return Response({"auth_url": auth_url})

@api_view(['GET'])
def auth_callback(request):
    code = request.GET.get('code')
    if not code:
        return Response({"error": "Authorization code not provided"}, status=400)

    credentials = base64.b64encode(
        f"{settings.EBAY_APP_ID}:{settings.EBAY_CLIENT_SECRET}".encode()
    ).decode()
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {credentials}"
    }

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.EBAY_REDIRECT_URI
    }

    response = requests.post(EBAY_TOKEN_URL, headers=headers, data=data)
    tokens = response.json()

    if response.status_code == 200:
        # Save tokens to database
        seller = Seller.objects.create(
            access_token=tokens['access_token'],
            refresh_token=tokens['refresh_token'],
            expires_at=datetime.now() + timedelta(seconds=tokens['expires_in'])
        )
        return redirect('http://localhost:5173/dashboard')
    else:
        return Response({"error": "Failed to obtain tokens"}, status=400)


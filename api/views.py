from rest_framework.decorators import api_view, permission_classes 
from rest_framework.permissions import IsAuthenticated 
from rest_framework.response import Response
from rest_framework import status
from dotenv import load_dotenv
import os
import requests
import logging
from django.contrib.auth.models import User 

# Get an instance of a logger
logger = logging.getLogger(__name__)

load_dotenv()

EC2_PREDICT_URL = os.environ.get("EC2_PREDICT_URL")

@api_view(['POST'])
def register_user(request):
    """
    Handles new user registration.
    """
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)
    
    return Response({"message": f"User '{username}' created successfully."}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def predict_image(request):
    print(f"Prediction requested by user: {request.user.username}")
    if 'image' not in request.FILES:
        return Response({"error": "No image file provided"}, status=status.HTTP_400_BAD_REQUEST)
    
    image_file = request.FILES['image']
    
    files = {'file': (image_file.name, image_file.read(), image_file.content_type)}
    
    try:
        response = requests.post(EC2_PREDICT_URL, files=files, timeout=15)
        
        response.raise_for_status()
        
        return Response(response.json(), status=status.HTTP_200_OK)

    except requests.exceptions.RequestException as e:
        logger.error(f"External API Error: Could not connect to model service at {EC2_PREDICT_URL}. Details: {e}")

        user_friendly_message = {
            "error": "The plant analysis service is temporarily unavailable. Our team has been notified. Please try again in a few moments."
        }
        return Response(user_friendly_message, status=status.HTTP_503_SERVICE_UNAVAILABLE)
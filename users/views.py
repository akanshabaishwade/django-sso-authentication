from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from datetime import timedelta
from .serializers import CustomUserSerializer
from .models import CustomUser

class RegisterAPIView(APIView):
    def post(self, request):
        # Validate and create user
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Save the user without any session or token
            
            # Manually set session expiration to avoid the NOT NULL constraint error
            session = request.session
            session.set_expiry(timedelta(days=7))  # Set expiration (7 days, can be adjusted)
            session.save()  # Save the session after setting expiration
            
            return Response({
                'user': serializer.data,
                'message': 'User successfully registered. Please log in to obtain access token.'
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta
from .models import ValidSessionToken

class LoginAPIView(APIView):
    def post(self, request):
        # Retrieve login credentials from request
        email = request.data.get("email")
        password = request.data.get("password")
        
        # Authenticate the user
        user = authenticate(email=email, password=password)
        
        if user is not None:
            # Check if there's already an active session in ValidSessionToken
            existing_session = ValidSessionToken.objects.filter(user=user).first()

            if existing_session:
                # If session exists, return error, asking user to use continue login API
                return Response({
                    "detail": "User has already logged in. Please use 'Continue Login' API to refresh session."
                }, status=status.HTTP_400_BAD_REQUEST)

            # Generate JWT tokens for the user
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Create session using Django's session management
            session = request.session
            session.create()  # Let Django handle session creation
            
            # Manually set session expiration to avoid the NOT NULL constraint error
            session.set_expiry(timedelta(days=7))  # Set expiration (7 days, can be adjusted)
            session.save()  # Save the session after setting expiration
            
            session_key = session.session_key  # Retrieve the session key

            # Create the ValidSessionToken object
            ValidSessionToken.objects.create(
                user=user,
                session_key=session_key,
                access_token=access_token,
            )

            return Response({
                'user': {'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name},
                'access_token': access_token,
                'refresh_token': str(refresh),
                'session_key': session_key,  # Include session_key in the response
            }, status=status.HTTP_200_OK)

        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import ValidSessionToken  # Import the ValidSessionToken model

class ContinueLoginAPIView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        
        # Authenticate the user
        user = authenticate(email=email, password=password)
        
        if user is not None:
            # Check if there is an existing ValidSessionToken
            existing_session = ValidSessionToken.objects.filter(user=user).first()

            if not existing_session:
                # If there's no existing session, return an error
                return Response({
                    "detail": "No previous login found. Please log in first."
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Delete the old session and token
            existing_session.delete()

            # Generate new JWT tokens for the user
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # Create a new session using Django's session management
            request.session.create()  # Let Django handle session creation
            session_key = request.session.session_key  # Retrieve the session key

            # Create a new ValidSessionToken object
            ValidSessionToken.objects.create(
                user=user,
                session_key=session_key,
                access_token=access_token,
            )

            return Response({
                'user': {'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name},
                'access_token': access_token,
                'refresh_token': str(refresh),
                'session_key': session_key,  # Include session_key in the response
            }, status=status.HTTP_200_OK)

        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

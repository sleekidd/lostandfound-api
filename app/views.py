from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets, permissions, status
from .models import CustomUser, LostItem, FoundItem
from .serializers import UserSerializer, LostItemSerializer , FoundItemSerializer
from rest_framework.authentication import TokenAuthentication
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .serializers import UserSerializer
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required

class UserViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = CustomUser.objects.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data['last_name'],
                phone_number=serializer.validated_data['phone_number'],
                gender=serializer.validated_data['gender'],
            )
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        user = None
        if '@' in username:
            try:
                user = CustomUser.objects.get(email=username)
            except ObjectDoesNotExist:
                pass

        if not user:
            user = authenticate(username=username, password=password)


        if user:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    def logout(self, request):
        if request.user.is_authenticated:
            logout(request)
            return Response({'message': 'Logged out successfully'})
        else:
            return Response({'error': 'User not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_details(request):
    user = request.user
    user_data = {
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'phone_number': user.phone_number,
        'gender': user.gender,
        # Add other user details as needed
    }
    return JsonResponse(user_data)



class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class LostItemViewSet(viewsets.ModelViewSet):
    queryset = LostItem.objects.all()
    serializer_class = LostItemSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save the new Lost Item
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    authentication_classes = [TokenAuthentication]  # Example: Use your preferred authentication class
    permission_classes = [permissions.IsAuthenticated]  # Ensure user is authenticated

    # Implement authentication and permissions if needed

class FoundItemViewSet(viewsets.ModelViewSet):
    queryset = FoundItem.objects.all()
    serializer_class = FoundItemSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save the new Found Item
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    authentication_classes = [TokenAuthentication]  # Example: Use your preferred authentication class
    permission_classes = [permissions.IsAuthenticated]  # Ensure user is authenticated

    # Implement authentication and permissions if needed

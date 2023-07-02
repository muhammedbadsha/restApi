from django.shortcuts import render
from django.http import JsonResponse
from .models import User
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView,Response
from .serializers import UserSerializer
from cryptography.hazmat.primitives import serialization
import  jwt,datetime

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.data)
        
    def get(self, request):
        query_set = User.objects.all()
        serializer = UserSerializer(query_set,many = True)
        return Response(serializer.data) 

class LoginView(APIView):
    def get(self,request):
        query_set = User.objects.all()
        serializer = UserSerializer(query_set,many = True)
        return Response(serializer.data) 

    def post(self, request):
        email = request.data['email']
        password = request.data['password']    

        user = User.objects.filter(email = email).first()
        if user is None:
            raise AuthenticationFailed("User not found")
        if not user.check_password(password):
            raise AuthenticationFailed("incorrect password")
        
        payload = {
            'id': user.id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        print(payload)
        # new_token = jwt.encode(payload)
        token = jwt.encode(payload, 'secret', algorithm='HS384')
        
        response = Response()

        response.set_cookie(key='jwt',value = token,httponly=True)

        response.data = {
            'jwt': token

        }

        return response

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        # ...

        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
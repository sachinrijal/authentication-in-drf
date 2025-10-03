from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserRegistration,LoginSerializer,UserprofileSerializer,ChangepasswordSerializer,ResetpasswordSerializer,UserpasswordresetSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from account.models import User
from django.utils.encoding import  smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

# Create your views here.

def get_tokens_for_user(user):
    if not user.is_active:
      raise AuthenticationFailed("User is not active")

    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request):
        data = request.data
        serializer = UserRegistration(data=data)
        if serializer.is_valid():
            user= serializer.save()
            token = get_tokens_for_user(user)
            return Response(
                {
                'token':token,
                'message':'user created successfully',
                'user':serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request):
        data = request.data
        serializer = LoginSerializer(data=data)

        if serializer.is_valid(raise_exception=True):

            email= serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            user = authenticate(email=email,password = password)

            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token,'message':'successfully login '},status=status.HTTP_200_OK)
            else:
                return Response({'message':'email or password doesnot match '},status=status.HTTP_404_NOT_FOUND)
            
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UserprofileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        serializer = UserprofileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class ChangepasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def put(self,request):
        serializer = ChangepasswordSerializer(data=request.data,context= {'user':request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'message':'password change succesfully '
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ResetemailView(APIView):
    renderer_classes = [UserRenderer]
    
    def post(self,request):
        serializer = ResetpasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            email = serializer.validated_data['email']
            user = User.objects.get(email = email)

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)
            reset_link = f"http://127.0.0.1:8000/api/v1/user/{uid}/{token}"

            return Response(
                            {
                                'message':'password reset email has been sent',
                                'token':token,
                                'uid':uid
                            }
                            ,status=status.HTTP_200_OK
                            )
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class UserpasswordresetView(APIView):
    renderer_classes = [UserRenderer]
    
    def post(self,request,uid,token):
        try:
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)            
        except (DjangoUnicodeDecodeError, User.DoesNotExist):
            return Response({'message':'Invalid uid'},status=status.HTTP_400_BAD_REQUEST)
        
        if not PasswordResetTokenGenerator().check_token(user,token):
            return Response({'message':'Invalid or expired token'},status=status.HTTP_400_BAD_REQUEST)

        serializer = UserpasswordresetSerializer(data=request.data,context={'user':user})

        if serializer.is_valid(raise_exception= True):
            serializer.save()
            return Response({'message':'password change successfully'},status=status.HTTP_200_OK)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        




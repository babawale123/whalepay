from django.shortcuts import render
from django.shortcuts import get_object_or_404

from api.models import User
from api.serializers import UserSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.authtoken.models import Token


@api_view(['POST'])
def SignUp(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(email=request.data['email'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({'token':token.key, 'user':serializer.data})
    return Response(serializer.errors)

@api_view(['POST'])
def Login(request):
    user = get_object_or_404(User, email = request.data['email'])
    if not user.check_password(request.data['password']):
        return Response({'error':'invalid_password'})
    token,created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance = user)
    return Response({'token':token.key, 'user':serializer.data})

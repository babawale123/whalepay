from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import NoteSerializer
from note.models import Note

from rest_framework.decorators import authentication_classes,permission_classes
from rest_framework import permissions,authentication


class CreateAndGetNote(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        note = Note.objects.filter(user=request.user)
        serializer = NoteSerializer(note, many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = NoteSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors)

class details(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_ayomi(self,pk):
        try:
            return Note.objects.get(pk=pk, user= self.request.user)
        except Note.DoesNotExist:
            return None
    
    def put(self,request,pk):
        note = self.get_ayomi(pk)
        if note:
            serializer = NoteSerializer(note,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        return Response({'error':"note was not found"})
    
    def get(self, request,pk):
        note = self.get_ayomi(pk)
        if note:
            serializer = NoteSerializer(note)
            return Response(serializer.data)
        return Response({'note can not be found'})

    def delete(self,request,pk):
        note = self.get_ayomi(pk)
        if note:
            note.delete()
            return Response({'note deleted successfully'})
        return Response({'note not found'})
        
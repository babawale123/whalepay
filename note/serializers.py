from rest_framework import serializers
from note.models import Note


class NoteSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.email")
    class Meta:
        model = Note
        fields = '__all__'
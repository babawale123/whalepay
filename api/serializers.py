from rest_framework import serializers
from api.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id','email','name','password']
        extra_kwargs = {'password':{'write_only':True, "required":True}}
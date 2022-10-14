from dataclasses import fields
from rest_framework import serializers 
from .models import *
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['id','name','email','password']
        extra_kwargs = {
            'password':{'write_only':True}
        }
    def create(self,validted_data):
        password = validted_data.pop('password',None)
        instance = self.Meta.model(**validted_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


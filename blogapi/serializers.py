from rest_framework import serializers
from .models import Profile, ContentModel
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
      class Meta:
        model = User
        fields = ( 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}
# Register Serializerd

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    class Meta:
        model = Profile
        fields = ( 'user', 'phone', 'address', 'city', 'state', 'country', 'zip_code')

    def create(self, validated_data):
        #user_data = validated_data.pop('user')
        #user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        #Create a user account
        user = User.objects.create_user(validated_data['user']['username'], validated_data['user']['email'],
                                        validated_data['user']['password'])
        #Update the profile details
        profile = user.profile
        profile.phone = validated_data['phone']
        profile.address =  validated_data['address']
        profile.city =  validated_data['city']
        profile.state =  validated_data['state']
        profile.country =  validated_data['country']
        profile.zip_code =  validated_data['zip_code']
        profile.save()
        return profile
    
class PostCreateUpdateSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = ContentModel
        fields = ('author', 'title', 'body', 'summary', 'categories')
        #exclude =['document']
       
    def validate_title(self, value):
        if len(value) > 100:
            return serializers.ValidationError("Max title length is 100 characters")
        return value

    def validate_body(self, value):
        if len(value) > 300:
            return serializers.ValidationError(
                "Max description length is 300 characters"
            )
        return value    
    
    def validate_summary(self, value):
        if len(value) > 60:
            return serializers.ValidationError("Max title length is 60 characters")
        return value
    

    
class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentModel
        exclude =['document']
        fields = ('author', 'title', 'body', 'summary', 'categories')
 


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentModel
        fields =['title','body','summary','categories']      
        

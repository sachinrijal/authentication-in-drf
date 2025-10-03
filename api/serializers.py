from rest_framework import serializers
from account.models import User


class UserRegistration(serializers.ModelSerializer):

    password = serializers.CharField(write_only= True, required = True)
    password2 = serializers.CharField(write_only= True, required = True)

    class Meta:
        model = User
        fields = ['email','password','password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Password doesnot match')
        return data
    
    def create(self,validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            email= validated_data['email'],
            password = validated_data['password']
        )
        return user
        
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length = 255,required = True)
    password = serializers.CharField(write_only = True,required= True)


class UserprofileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']

class ChangepasswordSerializer(serializers.Serializer):
    Old_password = serializers.CharField(write_only = True,required = True,style={'input':'password'})
    New_password = serializers.CharField(write_only = True,required = True,style={'input':'password'})
    Confirm_password = serializers.CharField(write_only = True,required = True,style={'input':'password'})
    
    
    def validate(self, attrs):
        user = self.context.get('user')
        if not user.check_password(attrs['Old_password']):
            raise serializers.ValidationError("old password doesnot match ")
        
        if attrs['New_password'] != attrs['Confirm_password']:
            raise serializers.ValidationError(" new password and confirm password doesnot match.")
        
        return attrs
        
    def save(self, **kwargs):
        user = self.context.get('user')
        user.set_password(self.validated_data['New_password'])
        user.save()
        return user
    
class ResetpasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length = 255,required = True)

    def validate(self, attrs):
        email = attrs['email']
        if not User.objects.filter(email = email).exists():
            raise serializers.ValidationError("Email is not register")
        
        return attrs
    
class UserpasswordresetSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True,required= True,style = {'input':'password'})
    password2 = serializers.CharField(write_only=True,required= True,style = {'input':'password'})

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("The password doesnot match")
        
        return attrs
    
    def save(self, **kwargs):
        password = self.validated_data['password']
        user = self.context['user']
        user.set_password(password)
        user.save()
        return user
    
        
    
    




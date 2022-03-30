from wsgiref.validate import validator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Account, Choice, Question, Category, Answer
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from django.contrib.auth.password_validation import validate_password


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Customizes JWT default Serializer to add more information about user"""
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['is_superuser'] = user.is_superuser
        token['is_staff'] = user.is_staff

        return token
    

class AnswerSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = ['response', 'is_correct', 'id']
    
class QuestionSerializer(ModelSerializer):
    
    answers = AnswerSerializer(source='answer_set', many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['statement', 'id', 'answers']
    
    def create(self, validated_data):
        tracks_data = validated_data.pop('answers') #not ok
        album = Answer.objects.create(**validated_data)
        for track_data in tracks_data:
            Answer.objects.create(album=album, **track_data)
        return album

class ChoiceSerializer(ModelSerializer):
    
    class Meta:
        model = Choice
        fields = ['is_correct', 'account', 'question']
        
class ChoiceCompleteSerializer(ModelSerializer):
    
    class Meta:
        model = Choice
        fields = '__all__'
        
class RegisterSerializer(ModelSerializer):
    
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    class Meta:
        model = Account
        fields = ['username', 'password', 'email']
        validators = [
            UniqueTogetherValidator(
                queryset=Account.objects.all(),
                fields=['username', 'email']
            )
        ]
        
    def create(self, validated_data):
        
        user = Account.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
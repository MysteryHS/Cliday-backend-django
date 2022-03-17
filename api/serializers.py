from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Choice, Question, Category, Answer


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
        
        extra_kwargs = {
            'question': {'required': True},
        }

class ChoiceCompleteSerializer(ModelSerializer):
    
    class Meta:
        model = Choice
        fields = '__all__'
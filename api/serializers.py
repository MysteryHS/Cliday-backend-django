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
        answers_data = validated_data.pop('answers')
        answer = Answer.objects.create(**validated_data)
        for answer_data in answers_data:
            Answer.objects.create(answer=answer, **answer_data)
        return answer

class ChoiceSerializer(ModelSerializer):
    
    class Meta:
        model = Choice
        fields = ['is_correct', 'account', 'question']
        
        extra_kwargs = {
            'question': {'required': True},
        }

class ChoiceCompleteSerializer(ModelSerializer):
    category = serializers.CharField('get_category')
    class Meta:
        model = Choice
        fields = '__all__'
        
    def get_category(self, choice):
        return choice.question.category.text
        
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
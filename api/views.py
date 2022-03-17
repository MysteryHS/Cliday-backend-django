import random
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from api.serializers import AnswerSerializer, ChoiceCompleteSerializer, ChoiceSerializer, QuestionSerializer
from .models import Account, Answer, Choice, Question
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
JWT_authenticator = JWTAuthentication()

def get_user(request):
    response = JWT_authenticator.authenticate(request)
    if response is not None:
        # unpacking
        user , token = response
        return user
    return None

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/account',
        'GET /api/account/:id'
    ]
    return Response(routes)

class ListUsers(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        user = get_user(request)
        content = {
            'user': str(user.username)
        }
        return Response(content)
    
class GetQuestionsOfTheDay(APIView):
    
    def get(self, request, format=None):
        questions = Question.objects.order_by('-date_selected')[:10]
        serializer = QuestionSerializer(questions, many=True)
        for question in questions:
            answersQS = Answer.objects.filter(question_id=question.id)
            answers = AnswerSerializer(answersQS, many=True)
        return Response(serializer.data)
    
class AnswerQuestion(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = get_user(request)
        updated_request = request.POST.copy()
        updated_request.update({'account': user.id})
        choice = ChoiceSerializer(data=updated_request)
        if choice.is_valid():
            result = choice.save()
            return Response(ChoiceCompleteSerializer(result).data)
        return Response(choice.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GetAnswers(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = get_user(request)
        choiceQS = Choice.objects.filter(account=user.id)
        choice = ChoiceCompleteSerializer(choiceQS, many=True)
        return Response(choice.data)
    
class GetRandomQuestions(APIView):
    authentication_classes = [JWTAuthentication]
    
    def get(self, request):
        user = get_user(request)
        if(user):
            inner_qs = Choice.objects.filter(account=user.id).values('question')
            questions = Question.objects.exclude(id__in=inner_qs).order_by('?')[:20]
            serializer = QuestionSerializer(questions, many=True)
            for question in questions:
                answersQS = Answer.objects.filter(question_id=question.id)
                answers = AnswerSerializer(answersQS, many=True)
            return Response(serializer.data)
        else:
            questions = Question.objects.order_by('?')[:20]
            serializer = QuestionSerializer(questions, many=True)
            for question in questions:
                answersQS = Answer.objects.filter(question_id=question.id)
                answers = AnswerSerializer(answersQS, many=True)
            return Response(serializer.data)
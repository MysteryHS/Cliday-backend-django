from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from . import serializers
class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = serializers.CustomTokenObtainPairSerializer

urlpatterns = [
    path('',  views.getRoutes),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('users/', views.ListUsers.as_view()),
    path('get_questions_of_the_day/', views.GetQuestionsOfTheDay.as_view()),
    path('answer_question/', views.AnswerQuestion.as_view()),
    path('get_answers/', views.GetAnswers.as_view()),
    path('get_random_questions/', views.GetRandomQuestions.as_view())
]

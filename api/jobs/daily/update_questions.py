from django_extensions.management.jobs import DailyJob
from ...models import Question
from django.utils import timezone

class Job(DailyJob):
    help = "Django Daily Job"

    def execute(self):
        Question.objects.order_by('-date_selected')[:10].update(date_selected=timezone.now())
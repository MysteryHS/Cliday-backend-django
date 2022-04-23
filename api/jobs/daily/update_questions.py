from django.core.management.base import BaseCommand
from ...models import Question
from django.utils import timezone

class Job(BaseCommand):
    help = "Django Daily Job"

    def handle(self):
        Question.objects.order_by('-date_selected')[:5].update(date_selected=timezone.now())
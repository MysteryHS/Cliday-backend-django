from django.core.management.base import BaseCommand
from ...models import Question
from django.utils import timezone

class Command(BaseCommand):
    help = "Django Daily Job"

    def handle(self, *args, **options):
        Question.objects.order_by('-date_selected')[:5].update(date_selected=timezone.now()) 
        #default timezone is utc in heroku
        
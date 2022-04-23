from django.core.management.base import BaseCommand
from ...models import Question
from django.utils import timezone

class Command(BaseCommand):
    help = "Django Daily Job"

    def handle(self, *args, **options):
        inner_q = Question.objects.order_by('date_selected').values('pk')[:5]
        Question.objects.filter(pk__in=inner_q).update(date_selected=timezone.now())
        
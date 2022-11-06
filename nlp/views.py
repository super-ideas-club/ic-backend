from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from django.http import JsonResponse
import json

from .models import TextAnalyzer
from ideasLogic.models import Idea, IdeaTheme

analyzer = TextAnalyzer()

for idea in Idea.objects.all():
    analyzer.train(idea.description)


@csrf_exempt
def get_tags(request):
    if request.method == 'POST':
        form_data = json.loads(request.body.decode())
        text = form_data['text']
        tags = analyzer.analyze(text)
        return JsonResponse(status=status.HTTP_201_CREATED,
                            data={
                                'tags': tags
                            },
                            safe=False,
                            json_dumps_params={
                                'ensure_ascii': False
                            })


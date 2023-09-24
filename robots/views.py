from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Robot

@csrf_exempt
def robot_endpoint(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # Валидация данных 
        if not all(key in data for key in ['model', 'version', 'created']):
            return JsonResponse({"error": "Некорректные входные данные"}, status=400)

        # Создание записи в базе данных
        robot = Robot.objects.create(
            model=data['model'],
            version=data['version'],
            created=data['created']
        )
        return JsonResponse({"message": "Успешно создано!"})
    return JsonResponse({"error": "Метод не поддерживается"}, status=405)

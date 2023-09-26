from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Robot
import openpyxl
from django.http import HttpResponse
import datetime
from django.utils import timezone

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

def generate_excel(request):
    # Создание новой книги Excel
    wb = openpyxl.Workbook()
    # Вычисляем дату, начиная с которой будем фильтровать записи (7 дней назад от текущей даты)
    week_ago = timezone.now() - datetime.timedelta(days=7)
    
    # Получаем уникальные модели роботов, произведенные за последние 7 дней
    models = Robot.objects.filter(created__gte=week_ago).values_list('model', flat=True).distinct()
    
    # Для каждой уникальной модели создаем новую страницу в Excel
    for model in models:
        ws = wb.create_sheet(title=model) # Создание новой страницы с названием модели
        ws.append(['Модель', 'Версия', 'Количество за неделю']) # Добавление заголовков
        
        # Добавление данных о каждом роботе данной модели
        for robot in Robot.objects.filter(model=model,created__gte=week_ago):
            ws.append([robot.model, robot.version, robot.quantity])

    # Подготовка HTTP-ответа с файлом Excel
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="robots_summary.xlsx"'

    # Сохранение книги Excel в ответ
    wb.save(response)
    return response
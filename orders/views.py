from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Order,Robot,Customer,WaitlistOrder
from django.core.mail import send_mail

@csrf_exempt
#End-point заказа робота заказчиком
def order_robot_endpoint(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Валидация данных 
        if not all(key in data for key in ['model', 'version','customer_name', 'customer_email']):
            return JsonResponse({"error": "Некорректные входные данные"}, status=400)
        
        # Получение или создание клиента
        customer, created = Customer.objects.get_or_create(
            name=data['customer_name'],
            email=data['customer_email']
        )

        # Проверка наличия робота
        try:
            robot = Robot.objects.get(model=data['model'], version=data['version'])
            # Создание заказа
            order = Order.objects.create(
                customer=customer,
                robot=robot
            )
            return JsonResponse({"message": "Успешно создано!"})
        except Robot.DoesNotExist:
             # Создание списка ожидания, если робота не существует
             waitlist = WaitlistOrder.objects.create(
                customer=customer,
                model=data['model'],
                version=data['version'],
                is_backordered=True
            )
             return JsonResponse({"error": "Робот не найден, но ваш заказ добавлен в список ожидания"}, status=404)
                 
    return JsonResponse({"error": "Метод не поддерживается"}, status=405)

@csrf_exempt
#Функция,вызываемая при появлении робота
def robot_appear(request):
    # Получаем все заказы, которые находятся в режиме ожидания
    waitlist_orders = WaitlistOrder.objects.filter(is_backordered=True)

    for order in waitlist_orders:
         # Проверяем наличие робота
        robot_available = Robot.objects.filter(model=order.model, version=order.version).exists()

        if robot_available:
            # Отправляем уведомление клиенту
            send_mail(
        'Робот в наличии!',
        f'Добрый день!\nНедавно вы интересовались нашим роботом модели {order.model}, версии {order.version}.\nЭтот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами.',
        'alexej.ivanov1084736@gmail.com',
        [order.customer.email],
        fail_silently=False,
    )
        # Обновляем статус заказа
            order.is_backordered = False
            order.save()

        else:
            return JsonResponse({"error": "Робот опять не найден"}, status=404)

    return JsonResponse({"message": "Уведомления отправлены"})
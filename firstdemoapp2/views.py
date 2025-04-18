from django.http import JsonResponse
from .models import MyUser
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if MyUser.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'message': 'Username already exists'})
        MyUser.objects.create(username=username, password=password)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = MyUser.objects.filter(username=username, password=password).first()
        if user:
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': 'Invalid credentials'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

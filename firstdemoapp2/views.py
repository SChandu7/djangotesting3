import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import MyUser, ExternalData
from django.contrib import messages


@csrf_exempt
def signup_view(request):
    if request.method == 'GET':
        return render(request, 'signup.html')  # Show signup form

    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if MyUser.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'message': 'Username already exists'})

        MyUser.objects.create(username=username, password=password)
        return JsonResponse({'status': 'success', 'message': 'Account created successfully'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@csrf_exempt
def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html')  # Show login form

    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = MyUser.objects.filter(username=username, password=password).first()
        if user:
            return JsonResponse({'status': 'success', 'message': 'Login successful'})

        return JsonResponse({'status': 'error', 'message': 'Invalid credentials'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@csrf_exempt
def external_data(request):
    if request.method == 'GET':
        return render(request, 'external_data.html')

    elif request.method == 'POST':
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST

            title = data.get('title')
            description = data.get('description')
            value = data.get('value')

            if not all([title, description, value]):
                messages.error(request, 'All fields are required.')
                return redirect('external_data')

            ExternalData.objects.create(title=title, description=description, value=value)
            messages.success(request, 'External data saved successfully!')
            return redirect('external_data')

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('external_data')

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
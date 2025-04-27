import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import MyUser, ExternalData
from django.contrib import messages
import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ExternalData
import tempfile
from django.conf import settings

client_id = settings.IMGUR_CLIENT_ID
client_secret = settings.IMGUR_CLIENT_SECRET




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
    image_url = None

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        value = request.POST.get('value')

        if not all([title, description, value]):
            messages.error(request, 'All fields are required.')
            return redirect('external_data')

        # Handle image upload
        if request.FILES.get('image'):
            uploaded_file = request.FILES['image']
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                for chunk in uploaded_file.chunks():
                    tmp.write(chunk)
                tmp_path = tmp.name
            try:
                image_url = upload_image_to_imgur(tmp_path)
                messages.info(request, f'Image uploaded: {image_url}')
            except Exception as e:
                messages.error(request, f'Image upload failed: {str(e)}')

        # Save to database (now with image_url)
        ExternalData.objects.create(
            title=title,
            description=description,
            value=value,
            image_url=image_url
        )
        messages.success(request, 'External data saved successfully!')
        return redirect('external_images')  # You can redirect to image listing

    return render(request, 'external_data.html', {'image_url': image_url})


IMGUR_CLIENT_ID = '127e9eec8880f63'  # Replace with your actual client ID

def upload_image_to_imgur(image_path):
    url = "https://api.imgur.com/3/image"
    
    headers = {
        "Authorization": f"Client-ID {IMGUR_CLIENT_ID}"
    }

    with open(image_path, "rb") as img:
        payload = {
            'image': img.read(),
            'type': 'file'
        }
        response = requests.post(url, headers=headers, files=payload)

    if response.status_code == 200:
        return response.json()['data']['link']  # Returns the image URL
    else:
        raise Exception(f"Failed to upload image: {response.content}")
    

    import tempfile


def external_data_view(request):
    image_url = None
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        value = request.POST.get('value')

        if request.FILES.get('image'):
            uploaded_file = request.FILES['image']
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                for chunk in uploaded_file.chunks():
                    tmp.write(chunk)
                tmp_path = tmp.name
            try:
                image_url = upload_image_to_imgur(tmp_path)
                messages.info(request, f'Image uploaded successfully: {image_url}')
            except Exception as e:
                messages.error(request, f'Image upload failed: {e}')
        
        # Now you can save title, description, value, and image_url in your DB if needed

    return render(request, 'external_data.html', {'image_url': image_url})




def external_images_view(request):
    data = ExternalData.objects.all().order_by('-id')
    return render(request, 'external_images.html', {'data': data})

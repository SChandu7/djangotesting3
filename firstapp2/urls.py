from django.contrib import admin
from django.urls import path
from .views import home, demo, demo2, nothing
from firstdemoapp2.views import signup_view, login_view, external_data, external_images_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('demo/', demo),
    path('demo/demo/', demo2),
    path('nothing/', nothing),
    path('signup/', signup_view),
    path('login/', login_view),
    path('external/', external_data, name='external_data'),
    path('all-images/', external_images_view, name='external_images'),
]

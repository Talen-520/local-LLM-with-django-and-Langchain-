from django.urls import path
from . import views
#from django.conf.urls.static import static

urlpatterns = [
    # website render
    # path('', views.home, name='home'),
    # path('about/', views.about, name='about'),

    # function call
    path('api/openai/', views.openai),
    path('api/qwen/', views.qwen),
    path('api/llama3/', views.llama3),
    path('api/secret/',views.secret,name='secret'),
]

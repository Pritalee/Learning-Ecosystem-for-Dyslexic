from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from mysite.core import views


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('upload/', views.upload, name='upload'),
    path('correction/', views.correction, name='correction'),
    
    path('dictionary/', views.dictionary, name='dictionary'),
    path('texttoimage/', views.texttoimage, name='texttoimage'),
    
    path('speech/', views.speech, name='speech'),
    path('3DScene/', views.Scene, name='Scene'),
    path('stop/', views.stop, name='stop'),
    #path('class/books/media/', views.UploadBookView.as_view(), name='class_upload_book'),
    #path('<language>/<text>', gTTs),

    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

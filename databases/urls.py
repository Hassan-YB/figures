from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('db/', views.database, name='database'),
    path('releases/', views.releases, name='releases'),
    path('entries/', views.entries, name='entries'),
    path('details/<int:id>/',views.details,name='details'),
    path('update/<int:id>/',views.update,name='update')
]

if settings.DEBUG: 
        urlpatterns += static(settings.MEDIA_URL, 
                              document_root=settings.MEDIA_ROOT) 
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.welcome, name='welcome'),
    path("news/", views.index, name="index"),
    path("news/<int:link>/", views.get_article, name="news"),
    path("news/create/", views.create, name="create"),
]

urlpatterns += static(settings.STATIC_URL)

from django.urls import path

from .views import async_test, sync_test


urlpatterns = [
    path('async_test', async_test),
    path('sync_test', sync_test),
]

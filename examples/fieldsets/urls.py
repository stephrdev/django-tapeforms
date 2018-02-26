from django.contrib import admin
from django.urls import include, path

from .views import ManualFieldsetsView, PropertyFieldsetsView


urlpatterns = [
    path('manual/', ManualFieldsetsView.as_view()),
    path('property/', PropertyFieldsetsView.as_view()),
]

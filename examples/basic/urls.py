from django.contrib import admin
from django.urls import include, path

from .views import (
    SimpleBootstrapView, SimpleFoundationView, SimpleMultiWidgetView,
    SimpleView, SimpleWithOverridesView)


urlpatterns = [
    path('simple/', SimpleView.as_view()),
    path('overrides/', SimpleWithOverridesView.as_view()),
    path('bootstrap/', SimpleBootstrapView.as_view()),
    path('foundation/', SimpleFoundationView.as_view()),
    path('multiwidget/', SimpleMultiWidgetView.as_view()),
]

from django.urls import path

from .views import (
    SimpleBootstrap4View,
    SimpleBootstrap5View,
    SimpleFoundationView,
    SimpleMultiWidgetView,
    SimpleView,
    SimpleWithOverridesView,
)

urlpatterns = [
    path("simple/", SimpleView.as_view()),
    path("overrides/", SimpleWithOverridesView.as_view()),
    path("bootstrap4/", SimpleBootstrap4View.as_view()),
    path("bootstrap5/", SimpleBootstrap5View.as_view()),
    path("foundation/", SimpleFoundationView.as_view()),
    path("multiwidget/", SimpleMultiWidgetView.as_view()),
]

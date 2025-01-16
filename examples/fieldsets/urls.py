from django.urls import path

from .views import BootstrapFieldsetsView, ManualFieldsetsView, PropertyFieldsetsView

urlpatterns = [
    path("manual/", ManualFieldsetsView.as_view()),
    path("property/", PropertyFieldsetsView.as_view()),
    path("bootstrap/", BootstrapFieldsetsView.as_view()),
]

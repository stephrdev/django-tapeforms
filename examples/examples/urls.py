from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("basic/", include("basic.urls")),
    path("fieldsets/", include("fieldsets.urls")),
]

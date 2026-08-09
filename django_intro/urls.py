from django.contrib import admin
from django.urls import include, path

from ehlo.views import carnet, index, mentions_legales

urlpatterns = [
    path("admin/", admin.site.urls),
    path("ai/", include("ai.urls")),
    path("map/", include("map.urls")),
    path("carnet/", carnet, name="carnet"),
    path("mentions-legales/", mentions_legales, name="mentions_legales"),
    path("", index, name="ehlo"),
]

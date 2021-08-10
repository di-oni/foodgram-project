from django.conf import settings
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import views


handler404 = "foodgram.views.page_not_found"
handler500 = "foodgram.views.server_error"

urlpatterns = [
    path("administration/", admin.site.urls),
    path("", include("recipes.urls")),
    path("api/", include("api.urls")),
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path("about-foodgram/", views.about_foodgram, name="about_foodgram"),
    path("about-author/", views.about_author, name="about_author"),
    path("about-tech/", views.about_tech, name="about_tech"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

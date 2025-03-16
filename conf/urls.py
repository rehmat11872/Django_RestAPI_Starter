"""
URL configuration for conf project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.shortcuts import render
from django.conf import settings
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView



# TODO 🚫 Delete the index view, route and template.
def index(request):
    base_url = (
        "https://github.com/wilfredinni/django-starter-template?tab=readme-ov-file"
    )
    context = {}
    context["version"] = "0.2.5"
    context["buttons"] = [
        {"title": "🚀 Features", "url": f"{base_url}#key-features"},
        {"title": "📋 Requirements", "url": f"{base_url}#requirements"},
        {"title": "🛠️ API Schema", "url": "/api/schema/swagger-ui/"},
    ]
    return render(request, "index.html", context)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    # import debug_toolbar

    urlpatterns += [
        path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
        path(
            "api/schema/swagger-ui/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        ),
        path("", index),
        # path("__debug__/", include(debug_toolbar.urls)),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('appcfp/', include('appcfp.urls')),
    path('appbi/', include('appbi.urls')),
]

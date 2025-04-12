from django.contrib import admin
from django.urls import (
    path,
    include
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('komply_api/task_management/', include('task_management.urls')),
    path('komply_api/system_management/', include('system_management.urls')),
]

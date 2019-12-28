from django.urls.conf import path
from apps.data.views import KeyValAPIView
urlpatterns = [
    path('values', KeyValAPIView.as_view(), name="values_list")
]

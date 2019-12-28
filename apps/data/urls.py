from django.urls.conf import path
from apps.data.views import KeyValListCreateView, KeyValUpdateView
urlpatterns = [
    path('values', KeyValListCreateView.as_view(), name='create_list'),
    path('values1', KeyValUpdateView.as_view(), name='update')
]
